#!/usr/bin/env python3
"""
CLI: open-ended survey CSV → frequency-ranked theme report (CSV).

Clustering method: TF–IDF (word + bigram) + K-means in scikit-learn.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_survey_csv(path: Path) -> pd.DataFrame:
    """Load CSV; tolerate classic Mac CR line endings and common encodings."""
    # Real survey exports differ by tool: try common encodings and line terminators until one parses.
    last_err: Exception | None = None
    for encoding in ("utf-8", "latin-1", "cp1252"):
        for lt in ("\r", "\n", "\r\n"):
            try:
                return pd.read_csv(
                    path,
                    encoding=encoding,
                    low_memory=False,
                    lineterminator=lt,
                )
            except Exception as e:  # noqa: BLE001 — try next combo
                last_err = e
                continue
    raise RuntimeError(f"Could not read {path}: {last_err}")


def _cell_as_text(val: object) -> str | None:
    # Turn one table cell into clean text, or None if it is missing / placeholder.
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    s = str(val).strip()
    if not s or s.lower() in {"nan", "none", "null"}:
        return None
    return s


def _numeric_fraction(series: pd.Series) -> float:
    """Share of non-null values that parse as finite numbers."""
    # Used to drop columns that are mostly numeric scales, not prose answers.
    non_null = series.dropna()
    if non_null.empty:
        return 1.0
    coerced = pd.to_numeric(non_null, errors="coerce")
    return float(coerced.notna().sum() / len(non_null))


def detect_open_ended_columns(
    df: pd.DataFrame,
    *,
    min_rows: int,
    min_avg_len: float = 18.0,
    min_p90_len: float = 28.0,
    max_numeric_fraction: float = 0.82,
) -> list[str]:
    """
    Heuristic: longish, fairly diverse text; mostly not pure numeric codes.

    UX surveys often mix Likert numbers with a few long-answer columns — we bias
    toward *length* and *uniqueness* over perfect NLP classification.
    """
    candidates: list[str] = []
    for col in df.columns:
        # Collect non-empty string answers for this column only.
        texts: list[str] = []
        for v in df[col].tolist():
            t = _cell_as_text(v)
            if t is not None:
                texts.append(t)
        n = len(texts)
        if n < min_rows:
            continue
        if _numeric_fraction(df[col]) > max_numeric_fraction:
            continue
        lengths = np.array([len(t) for t in texts], dtype=float)
        avg_len = float(lengths.mean())
        p90_len = float(np.percentile(lengths, 90))
        unique_ratio = len(set(texts)) / n
        # Require reasonably long answers (open-ended) and some variety (not one repeated code).
        if avg_len < min_avg_len and p90_len < min_p90_len:
            continue
        if unique_ratio < 0.06 and avg_len < 35:
            continue
        candidates.append(str(col))
    return candidates


def _default_k(n_samples: int) -> int:
    if n_samples < 8:
        return 2
    # Sublinear K: enough themes to be useful, not so many that every row is its own cluster.
    return int(max(2, min(10, round(np.sqrt(n_samples)))))


def min_rows_for_clustering(cli_min_rows: int) -> int:
    # K-means needs enough points; never go below a small floor even if CLI min is tiny.
    return max(8, cli_min_rows)


def _sanitize_label_chunk(s: str) -> str:
    # One keyword snippet for the human-readable theme title (single line, bounded length).
    s = re.sub(r"\s+", " ", s).strip()
    return s[:80]


def cluster_column_themes(
    column_name: str,
    texts: list[str],
    *,
    n_clusters: int | None,
    random_state: int,
) -> list[dict]:
    """Return one dict per cluster with frequencies, keywords, quotes."""
    n_samples = len(texts)
    if n_samples < 8:
        return []

    # Choose K: user override, else a small sqrt-based default; never exceed one cluster per row.
    k = n_clusters if n_clusters is not None else _default_k(n_samples)
    k = int(max(2, min(k, n_samples - 1)))

    # TF–IDF hyperparameters scaled to dataset size so rare typos and ultra-common words behave sensibly.
    min_df = max(1, min(2, max(1, n_samples // 40)))
    max_df = min(0.95, max(0.5, 1.0 - (3 / n_samples)))

    # Sparse matrix X: one row per response, columns = word/bigram importance weights.
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=min_df,
        max_df=max_df,
        max_features=8000,
        sublinear_tf=True,
    )
    try:
        X = vectorizer.fit_transform(texts)
    except ValueError:
        # e.g. empty vocabulary after min_df / max_df filtering — skip this column quietly.
        return []

    if X.shape[1] < 2:
        return []

    # Assign each response row to one of k theme buckets (cluster ids 0 .. k-1).
    km = KMeans(
        n_clusters=k,
        n_init="auto",
        random_state=random_state,
        max_iter=300,
    )
    labels = km.fit_predict(X)
    feature_names = np.array(vectorizer.get_feature_names_out())
    centers = km.cluster_centers_

    rows_out: list[dict] = []
    for cid in range(k):
        mask = labels == cid
        freq = int(mask.sum())
        if freq == 0:
            continue

        # Theme wording: strongest positive weights in this cluster’s centroid = keyword list + short title.
        centroid = centers[cid : cid + 1]
        top_idx = np.argsort(centroid.ravel())[-15:][::-1]
        keywords = ", ".join(feature_names[i] for i in top_idx if centroid[0, i] > 0)
        top_kw = [feature_names[i] for i in top_idx if centroid[0, i] > 0][:4]
        label_bits = " · ".join(_sanitize_label_chunk(w) for w in top_kw if w)
        theme_label = f"[{column_name}] {label_bits}" if label_bits else f"[{column_name}] theme {cid + 1}"

        # Representative quotes: real answers whose TF–IDF vectors sit closest to this cluster center.
        X_c = X[mask]
        idx_c = np.where(mask)[0]
        sims = cosine_similarity(X_c, centroid).ravel()
        order = np.argsort(-sims)
        quotes: list[str] = []
        for j in order[:3]:
            # j is a row index into X_c; idx_c maps that row to the same-index entry in `texts`.
            raw = texts[int(idx_c[int(j)])]
            q = re.sub(r"\s+", " ", raw).strip()
            if len(q) > 200:
                q = q[:197] + "..."
            if q and q not in quotes:
                quotes.append(q)
        rep = " | ".join(quotes)

        rows_out.append(
            {
                # percent_of_total is share of non-empty answers in *this column only*.
                "theme_label": theme_label[:500],
                "frequency": freq,
                "percent_of_total": round(100.0 * freq / n_samples, 2),
                "representative_quotes": rep,
                "keywords": keywords[:2000],
                "_column": column_name,
                "_cid": cid,
            }
        )
    return rows_out


def build_report(
    df: pd.DataFrame,
    columns: list[str],
    *,
    min_rows: int,
    n_clusters: int | None,
    random_state: int,
) -> pd.DataFrame:
    # One pass per survey question (column): cluster that column’s texts, append theme rows.
    all_rows: list[dict] = []
    for col in columns:
        texts: list[str] = []
        for v in df[col].tolist():
            t = _cell_as_text(v)
            if t is not None:
                texts.append(t)
        if len(texts) < min_rows_for_clustering(min_rows):
            print(f"Skipping column {col!r}: only {len(texts)} non-empty text cells.", file=sys.stderr)
            continue
        clusters = cluster_column_themes(
            col,
            texts,
            n_clusters=n_clusters,
            random_state=random_state,
        )
        all_rows.extend(clusters)

    # No analyzable text columns (or vectorizer failed everywhere): emit an empty report shell.
    if not all_rows:
        return pd.DataFrame(
            columns=[
                "theme_label",
                "frequency",
                "percent_of_total",
                "representative_quotes",
                "keywords",
                "rank",
            ]
        )

    out = pd.DataFrame(all_rows)
    # Global ranking: most common themes first; drop internal sort keys from the CSV.
    out = out.sort_values(
        by=["frequency", "_column", "theme_label"],
        ascending=[False, True, True],
    ).reset_index(drop=True)
    out["rank"] = np.arange(1, len(out) + 1)
    return out[
        [
            "theme_label",
            "frequency",
            "percent_of_total",
            "representative_quotes",
            "keywords",
            "rank",
        ]
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    # Wire CLI flags to paths and optional overrides (fixed K, explicit columns).
    p = argparse.ArgumentParser(
        description="Cluster open-ended CSV columns (TF–IDF + K-means) and write a ranked theme CSV.",
    )
    p.add_argument("--input", "-i", type=Path, required=True, help="Input CSV path")
    p.add_argument("--output", "-o", type=Path, required=True, help="Output CSV path")
    p.add_argument(
        "--columns",
        type=str,
        default="",
        help="Comma-separated column names to analyze (default: auto-detect)",
    )
    p.add_argument(
        "--n-clusters",
        type=int,
        default=None,
        help="Fixed K for K-means per column (default: heuristic from row count)",
    )
    p.add_argument("--min-rows", type=int, default=10, help="Min non-empty cells to consider a column")
    p.add_argument("--random-state", type=int, default=42, help="K-means random seed")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.input.is_file():
        print(f"Input not found: {args.input}", file=sys.stderr)
        return 1

    df = read_survey_csv(args.input)
    if args.columns.strip():
        # Researcher picked exact headers to treat as open-ended.
        use_cols = [c.strip() for c in args.columns.split(",") if c.strip()]
        missing = [c for c in use_cols if c not in df.columns]
        if missing:
            print(f"Unknown columns: {missing}", file=sys.stderr)
            return 1
    else:
        # Guess prose columns from length / uniqueness so “any CSV” works without manual config.
        use_cols = detect_open_ended_columns(df, min_rows=args.min_rows)
        if not use_cols:
            print(
                "No open-ended columns auto-detected. "
                "Try lowering --min-rows or pass explicit --columns.",
                file=sys.stderr,
            )
            return 1
        print("Auto-detected open-ended columns:", ", ".join(use_cols), file=sys.stderr)

    report = build_report(
        df,
        use_cols,
        min_rows=args.min_rows,
        n_clusters=args.n_clusters,
        random_state=args.random_state,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Final artifact for spreadsheets / synthesis tools: one row per theme cluster.
    report.to_csv(args.output, index=False)
    print(f"Wrote {len(report)} theme rows to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
