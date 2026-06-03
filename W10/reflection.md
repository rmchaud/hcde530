# Reflection — Open-ended survey theme report

**Student:** Riya Chaudhari

---

### 1. What did you build?

I built a **Python CLI** and a **companion Jupyter notebook** that ingest a **survey CSV** and write a **second CSV**: a **frequency-ranked theme table** for open-ended answers. The program either **auto-detects** which headers behave like long text (mixed survey grids are common) or accepts **`--columns`** explicitly. Each analyzed column is vectorized with **TF–IDF**, clustered with **K-means**, and summarized into rows with a **centroid-derived label**, **counts**, **within-question percentages**, **keywords**, up to **three representative quotes** (nearest the cluster center in vector space), and a **global rank** by frequency. The artifact is meant for **workshop triage**—not a replacement for a full codebook. **README**, **requirements**, a **sample CSV**, and the notebook are enough for a collaborator to reproduce a run without any course context. This tool is meant to automate the manually tedious act of coding/grouping open-ended survey responses so that UX designers and researchers can effectively synthesize the insights from their feedback to use on their next iteration.

---

### 2. What decisions did you make?

I chose a **file-first** workflow (**CSV on disk**) instead of making the core path depend on a live survey API. Exports are what teams already pass around; **`--input` / `--output`** keep scope bounded and avoid API keys in the main story. For **clustering**, I picked **TF–IDF + K-means** in **`scikit-learn`** over heavier or opaque stacks because it runs **offline**, is explainable to stakeholders, and behaves predictably on **small *n***. I used the public **Food Choices** file as a **shape-realistic** stress test (numeric + text columns), not for topical fit, and to avoid sharing sensitive participant text. Compared with my earlier MP2a direction, I **cut scope** to one shippable artifact—the ranked report—and deferred a durable public web app until hosting decisions were concrete.

---

### 3. What would you do differently?

First, I would add a **small hosted UI** (e.g. Streamlit or Hugging Face Spaces) **in addition to** the notebook. Colab is workable, but a single **upload → download** page would match how non-developer researchers actually want to try a tool and would make “share a link” unambiguous. Second, I would expose **cluster quality and language controls** in the CLI: e.g. optional **silhouette-driven *K*** or a capped grid search, and a flag to **disable English stop words** or load a custom list so short multilingual pilots do not silently misfire. Those are concrete product changes—not timeline advice—and they directly address false confidence when *K* is wrong or the corpus is not English-dominant.

---

### 4. What does this work demonstrate?

The repo shows **robust file handling** in **`read_survey_csv`** and **`_cell_as_text`**: multiple **encodings** and **line terminators**, plus treating string placeholders as missing—real survey exports are messy. It shows **pandas-backed synthesis** in **`build_report`**: assembling cluster outputs, **`sort_values`** for a legible ranking, and **`to_csv`** as the communication surface. **`c4_api_example.py`** adds a small, documented **HTTP + JSON** pattern with **`.gitignore`** for **`.env`**, signaling how keyed acquisition would be isolated even though the main tool is CSV-first. Finally, **`README.md`**, **`mp2.md`**, and **inline comments** document intent and **limits** of statistical themes, and **`--columns`** encodes when to **override** the model—documentation plus **professional judgment** about what not to ship unchecked.
