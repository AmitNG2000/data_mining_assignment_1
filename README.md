# Data Mining Assignment 1

Interactive multi-page Streamlit application for exploring and analyzing data using SQL, ORMs, and visualization techniques.

**Student**: Amit  
**Course**: The Art of Analyzing Big Data - The Data Scientist's Toolbox  
**Instructor**: Dr. Michael Fire  
**Institution**: Ben-Gurion University (BGU)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

#### 1. Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv dm1_env

# Activate virtual environment
dm1_env\Scripts\activate

# You should see (dm1_env) in your terminal prompt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv dm1_env

# Activate virtual environment
source dm1_env/bin/activate

# You should see (dm1_env) in your terminal prompt
```

#### 2. Install Dependencies

```bash
# With virtual environment activated
pip install -r requirements.txt
```

#### 3. Set Up Task 1 Database (One-Time Setup)

```bash
cd task1
python database.py
cd ..
```

#### 4. Run the Multi-Page App

```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

---

## 📋 Assignment Tasks

### ✅ Task 1: Baby Names Explorer (COMPLETED)
**Status**: ✅ Complete  
**Points**: 30/30 expected

Interactive exploration of US baby name trends (1880-2014) with:
- 📈 Name Popularity Over Time (count/percentage toggle)
- 🔍 Custom SQL Query Panel (safe execution + examples)
- 🏆 Peak Decade Finder

**Database**: 1,825,433 records in SQLite with optimized indexes  
**Tech**: Streamlit, SQLite3, Plotly Express, Pandas

[View Task 1 Documentation →](task1/README.md)

---

### 🔲 Task 2: Oscar Actor Explorer (Coming Soon)
**Status**: 📝 Planned  
**Points**: 25

ORM-based actor profile app with:
- Actor search and profile cards
- Wikipedia API integration
- Win rates and statistics
- Pattern discovery

**Tech**: PonyORM/SQLAlchemy/Peewee, Wikipedia API

---

### 🔲 Task 3: Pokémon Battle Arena (Coming Soon)
**Status**: 📝 Planned  
**Points**: 25

Database-driven battle game with:
- Team selection from database
- Battle mechanics based on stats
- Cheat code system (database modifications)
- Type effectiveness

**Tech**: SQLite/ORM, Interactive UI

---

### 🔲 Task 4: SQL Learning Game (Coming Soon)
**Status**: 📝 Planned  
**Points**: 25 + bonus

Interactive platform teaching SQL to beginners:
- Progressive challenges (SELECT → JOIN)
- Real SQLite database
- Feedback system
- Gamification elements

**Tech**: Streamlit, Creative UX design

---

## 🏗️ Project Structure

```
data_mining_assignment_1/
├── app.py                          # Main multi-page app entry point
├── pages/                          # Streamlit pages (one per task)
│   ├── 1_👶_Baby_Names_Explorer.py
│   ├── 2_🎬_Oscar_Actor_Explorer.py
│   ├── 3_⚔️_Pokémon_Battle_Arena.py
│   └── 4_🎮_SQL_Learning_Game.py
├── task1/                          # Task 1: Baby Names
│   ├── database.py                 # Database setup
│   ├── utils.py                    # SQL utilities
│   ├── babynames.db                # SQLite database (98 MB)
│   └── README.md                   # Task 1 documentation
├── task2/                          # Task 2: Oscar Actors (TBD)
├── task3/                          # Task 3: Pokémon Battle (TBD)
├── task4/                          # Task 4: SQL Learning (TBD)
├── data/                           # Datasets
├── .github/                        # GitHub configuration
│   ├── copilot-instructions.md     # Copilot AI instructions
│   └── co-pilot-reports/           # Development reports
│       ├── task1/                  # Task 1 completion reports
│       └── RESTRUCTURE_SUMMARY.md
├── dm1_env/                        # Virtual environment (gitignored)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 📦 Dependencies

All tasks share the same dependencies (see `requirements.txt`):

- **streamlit** - Multi-page web framework
- **pandas** - Data manipulation
- **plotly** - Interactive visualizations
- *(Additional dependencies will be added for Tasks 2-4)*

---

## 🎯 Usage

### Running the Application

```bash
# 1. Activate virtual environment
# Windows:
dm1_env\Scripts\activate
# macOS/Linux:
source dm1_env/bin/activate

# 2. Start the multi-page app
streamlit run app.py
```

Navigate between tasks using the **sidebar** (←).

### Setting Up Individual Tasks

Each task may require one-time setup (e.g., database creation):

**Task 1 Setup:**
```bash
# With dm1_env activated
cd task1
python database.py  # Loads 1.8M rows from CSV
cd ..
```

**Tasks 2-4:** Setup instructions will be added as tasks are completed.

---

## 🧪 Testing

### Task 1 Tests
```bash
# Activate dm1_env first
dm1_env\Scripts\activate  # Windows
# source dm1_env/bin/activate  # macOS/Linux

cd task1
python utils.py  # Test utilities
python discover_patterns.py  # Run pattern discovery
cd ..
```

---

## 📚 Documentation

- **Main App**: This README
- **Task 1**: [task1/README.md](task1/README.md) - Complete Baby Names documentation
- **Task 2-4**: Documentation will be added as tasks are completed
- **Assignment**: [HW1_instructions.pdf](HW1_instructions.pdf) - Full requirements

---

## 🎓 Assignment Guidelines

### LLM Usage Policy
- ✅ **Code**: LLM assistance encouraged for code generation
- ❌ **Explanations**: Must write in your own words (no LLM)
- ⚠️ **Understanding**: Must be able to explain solutions in person

### Submission Requirements
Each task needs:
- Deployed app OR notebook OR screen recording
- Written report (1-2 pages) with personal explanations
- Code with README and screenshots

---

## 🚢 Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy `app.py`
5. Share public URL

### Option 2: Local Hosting
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

---

## 📊 Progress Tracker

| Task | Status | Features | Points | Due Date |
|------|--------|----------|--------|----------|
| Task 1: Baby Names | ✅ Complete | 3/3 | 30/30 | TBD |
| Task 2: Oscar Actors | 📝 Planned | 0/3 | 0/25 | TBD |
| Task 3: Pokémon Battle | 📝 Planned | 0/4 | 0/25 | TBD |
| Task 4: SQL Learning | 📝 Planned | 0/5 | 0/25 | TBD |
| **Total** | **25%** | **3/15** | **30/105** | |

---

## 🤝 Contributing

This is an academic assignment. Code is for educational purposes only.

---

## 📄 License

Created for BGU Data Mining course - Academic use only.

---

## 👤 Author

**Amit**  
Ben-Gurion University  
Data Mining Course
