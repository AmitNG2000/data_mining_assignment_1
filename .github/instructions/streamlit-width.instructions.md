---
description: "Use when editing Streamlit UI code in this project. Enforce replacing deprecated use_container_width with width='stretch' or width='content'."
name: "Streamlit Width Parameter Rules"
---
# Streamlit Width Parameter Rules

Apply these rules when writing or updating Streamlit UI calls.

- Do not use `use_container_width`.
- For previous `use_container_width=True`, use `width='stretch'`.
- For previous `use_container_width=False`, use `width='content'`.
- If code examples or docs include `use_container_width`, update them to `width`.
- Treat `use_container_width` as removed for this codebase.
