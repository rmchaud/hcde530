# Week 3 - C2: Code Literacy and Documentation

To address C2 for this assignment, I practiced understanding what existing code does, changing logic safely, and leaving a clear trail of documentation for future use. For this script, code literacy means I can:
- read each block and explain its purpose in plain language
- identify bugs by running the program and interpreting error messages
- update code behavior without breaking the rest of the script
- document the "why" behind changes so someone else can follow decisions

I added inline comments around the main operations, especially where decisions matter:
- role normalization to group differently capitalized job titles together
- experience parsing logic to safely handle messy values (numeric and word-based)
- descending sort for satisfaction scores so "top 5" actually means highest

These comments improve readability and make the intent of each operation easier to follow while debugging. Additionally, my Week 3 commit history documents both bug fixes and documentation work using specific messages. The most important C2 skill this week was connecting runtime errors to code decisions. Running the script, tracing the failure (`ValueError`), and then documenting the logic change made the code easier to trust and maintain.
