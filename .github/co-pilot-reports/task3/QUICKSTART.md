# Task 3: Quick Start Guide

## 🎮 How to Use the Pokémon Battle Arena

### Starting the App
```bash
# From project root directory
streamlit run app.py
```

Then click on **"⚔️ Pokémon Battle Arena"** in the left sidebar.

### Playing a Battle

#### Step 1: Select Teams
1. Go to the **"👥 Team Selection"** tab
2. **Player 1 (Blue)**: Check boxes next to 1-3 Pokémon
3. **Player 2 (Red)**: Check boxes next to 1-3 Pokémon
4. Use the search box to find specific Pokémon quickly

#### Step 2: Start Battle
1. Go to the **"🎮 Battle"** tab
2. Review both teams
3. Click **"⚔️ Start Battle!"**

#### Step 3: Execute Turns
- **Execute Turn**: Advance one turn at a time
- **Auto Battle**: Run the entire battle automatically
- **Reset**: Clear and start over

### Using Cheat Codes

#### Step 1: Go to Cheat Codes Tab
1. Click on **"🎲 Cheat Codes"** tab
2. Select which player to apply the cheat to
3. Enter a cheat code

#### Available Cheat Codes:
- `UPUPDOWNDOWN` - Double your Pokémon's HP
- `GODMODE` - Set Defense and Sp.Def to 999
- `MAXPOWER` - Set all stats to 255
- `STEAL` - Copy opponent's strongest Pokémon to your team
- `LEGENDARY` - Create a custom overpowered Pokémon
- `NERF` - Reduce all opponent Pokémon stats by 50%

#### Step 2: Activate
Click **"🚀 Activate Cheat"** button

⚠️ **Warning**: Cheats modify the actual database!

### Detecting Cheats

#### Go to Cheat Detection Tab
1. Click on **"🔍 Cheat Detection"** tab
2. Click **"🔎 Scan for Anomalies"** to find abnormal stats
3. Click **"📜 View Cheat Log"** to see all logged cheats

#### Reset Database
If the database gets too modified:
1. Scroll to bottom of Cheat Detection tab
2. Click **"🔄 Reset Database"** to restore original state

### Viewing Analysis

#### Go to Analysis Tab
1. Click on **"📊 Analysis"** tab
2. See:
   - Most overpowered type combinations
   - Power creep across generations (with chart)
   - Weakest legendary Pokémon
   - SQL queries used for analysis

## 🎯 Example Battle

### Suggested Teams for Testing

**Team 1 (Starters)**:
- Charizard (Fire/Flying)
- Blastoise (Water)
- Venusaur (Grass/Poison)

**Team 2 (Legendaries)**:
- Mewtwo (Psychic)
- Articuno (Ice/Flying)
- Zapdos (Electric/Flying)

### Expected Result
Legendaries have higher stats, so Team 2 will likely win. But type effectiveness matters!

## 🔧 Troubleshooting

### Problem: "No Pokémon available to steal"
**Solution**: This happens if all Pokémon are already in teams. Try resetting the database or using different cheats.

### Problem: Battle freezes or doesn't advance
**Solution**: Click "Reset" and start a new battle. Make sure both teams have at least 1 Pokémon.

### Problem: Database file not found
**Solution**: The database is auto-created on first run. If missing, it will regenerate automatically.

### Problem: Import errors
**Solution**: Make sure you're in the project root directory and the virtual environment is activated:
```bash
.\dm1_env\Scripts\Activate.ps1
```

## 📊 Understanding Battle Mechanics

### Turn Order
- Faster Pokémon attacks first (based on Speed stat)
- Each turn, both Pokémon attack once

### Damage Calculation
```
Base Damage = (Attack × 50 / Defense) × 0.4
Type Multiplier = effectiveness from database
Random Factor = 0.85 to 1.0
Final Damage = Base × Type Multiplier × Random Factor
```

### Type Effectiveness Examples
- Water attacking Fire: **2x damage** (super effective!)
- Fire attacking Water: **0.5x damage** (not very effective)
- Electric attacking Ground: **0x damage** (immune!)

### HP Bars
- 🟩 Green: > 50% HP
- 🟨 Yellow: 25-50% HP
- 🟥 Red: < 25% HP

## 💡 Tips

1. **Use Search**: With 1025 Pokémon, search is your friend!
2. **Check Total Stats**: Higher total = generally stronger
3. **Type Advantage**: A weaker Pokémon with type advantage can win
4. **Cheat Responsibly**: Some cheats break the game balance
5. **Reset Often**: Database modifications persist, so reset when done testing

## 🎓 Assignment Context

This is **Task 3** of the Data Mining Assignment:
- **Database**: SQLite with raw SQL (no ORM)
- **All stats**: Loaded from database (no hardcoded values)
- **Cheat codes**: Real SQL operations (UPDATE/INSERT/DELETE)
- **Audit**: SQL queries detect anomalies
- **Analysis**: 3 statistical insights from dataset

## 📚 For More Information

See `task3/README.md` for complete documentation including:
- Database schema details
- Battle mechanics formulas
- Cheat code SQL queries
- Analysis findings
- Technology stack

---

**Have fun battling!** 🎮⚔️
