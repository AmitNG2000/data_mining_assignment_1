# Data Mining Assignment 1

Multi-page Streamlit app for Assignment 1.

## What is in this project

- One shared Streamlit app entry point
- Four task pages under the pages folder
- Task-specific code and data under task folders

## Quick start

### 1) Activate environment

Windows PowerShell:

```bash
& .\dm1_env\Scripts\Activate.ps1
```

If you do not have the environment yet:

```bash
py -m venv dm1_env
& .\dm1_env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501
```

## Project layout

```text
app.py
pages/
task1/
task2/
task3/
task4/
data/
requirements.txt
README.md
```
