# Data Mining Assignment 1

A multi-page Streamlit application showcasing SQL, ORMs, and interactive data analysis through four distinct tasks.

## 🌐 Live App

**[View on Streamlit Cloud](https://amitng2000-data-mining-assignment-1-app-awappc.streamlit.app/SQL_Learning_Game)**


## 📋 Tasks Details

- **[Task 1: Baby Names Explorer](task1/README_task1.md)** - SQLite-based interactive name popularity analysis
- **[Task 2: Oscar Actor Explorer](task2/README_task2.md)** - ORM-powered actor profiles with Wikipedia integration
- **[Task 3: Pokémon Battle Arena](task3/README_task3.md)** - Database-driven battle game with cheat codes
- **[Task 4: SQL Learning Game](task4/README_task4.md)** - Interactive platform for learning SQL



## 🤠 Understanding Requirement
Written explanation without LLM assistance: [no_llm_explanation](no_llm_explanation.md)



## 🗂️ Project Structure

```
├── app.py                      # Main Streamlit app entry point
├── pages/                      # Streamlit pages (one per task)
│   ├── 1_👶_Baby_Names_Explorer.py
│   ├── 2_🎬_Oscar_Actor_Explorer.py
│   ├── 3_⚔️_Pokémon_Battle_Arena.py
│   └── 4_🎮_SQL_Learning_Game.py
├── task1/                      # Baby Names task code & data
├── task2/                      # Oscar Actors task code & data
├── task3/                      # Pokémon Battle task code & data
├── task4/                      # SQL Learning Game code & data
├── requirements.txt            # Python dependencies
└── utils.py                    # Shared utilities
```

## 🚀 Local Installation

### Python Requirement

- **Python 3.14.2**

### 1. Clone the repository

```bash
git clone https://github.com/AmitNG2000/data_mining_assignment_1.git
cd data_mining_assignment_1
```

### 2. Create and activate virtual environment

**Windows PowerShell:**
```bash
py -m venv dm1_env
& .\dm1_env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv dm1_env
source dm1_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser to **http://localhost:8501**

## 🛠️ Technologies Used

- **Streamlit** - Web framework
- **SQLite** - Database (Tasks 1, 3, 4)
- **PonyORM** - ORM (Task 2)
- **Plotly** - Interactive visualizations
- **Wikipedia API** - External data integration (Task 2)


## 💻 Code (Github)
[data_mining_assignment_1](https://github.com/AmitNG2000/data_mining_assignment_1.git)
