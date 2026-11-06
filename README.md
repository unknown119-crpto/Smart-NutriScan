# 🥗 Smart Nutrition Analyzer

A full-stack web application for tracking and analyzing daily nutrition. Built with **Python Flask + SQLite + HTML/CSS/JS**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 User accounts | Register, login, logout with hashed passwords |
| 📊 Dashboard | Daily calorie ring, macro bars, quick food log |
| 🔍 Nutrition Analyzer | Build a meal, get full macro breakdown with health tips |
| 📅 History | Browse past logs, 7-day calorie chart |
| 👤 Profile | BMI calculator, TDEE calculator, calorie goal |
| 🍎 Food Database | 55+ verified foods across 7 categories |
| ➕ Custom Foods | Add your own foods with per-100g nutrition values |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Flask
- **Database:** SQLite (auto-created on first run)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **No external JS libraries** – pure vanilla JS

---

## 🚀 Setup & Run (Windows)

### Step 1 – Install Python
Download from https://python.org  
During install: ✅ **Add Python to PATH**

### Step 2 – Open project in VS Code
```
File > Open Folder > Smart-Nutrition-Analyzer
```

### Step 3 – Open Terminal in VS Code
```
Terminal > New Terminal
```

### Step 4 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 – Run the app
```bash
python app.py
```

### Step 6 – Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
Smart-Nutrition-Analyzer/
│
├── app.py               ← Flask application (routes + API)
├── schema.sql           ← Database structure
├── requirements.txt     ← Python packages
├── README.md            ← This file
│
├── instance/
│   └── nutrition.db     ← SQLite database (auto-created)
│
├── templates/
│   ├── base.html        ← Shared layout (sidebar, nav)
│   ├── login.html       ← Login page
│   ├── register.html    ← Registration page
│   ├── dashboard.html   ← Main dashboard
│   ├── analyze.html     ← Nutrition analyzer
│   ├── history.html     ← Food history & charts
│   └── profile.html     ← User profile & BMI/TDEE
│
└── static/
    ├── css/
    │   └── style.css    ← All styles (dark theme)
    └── js/
        └── main.js      ← Sidebar toggle, animations
```

---

## 🗄️ Database

The SQLite database is **automatically created** when you first run `python app.py`.  
It includes:
- 55+ pre-loaded food records
- 7 categories: Fruits, Vegetables, Proteins, Grains, Dairy, Nuts & Seeds, Oils

---

## 🎓 Built For
BSIT coursework – University of Education, Pakistan  
Demonstrates: REST APIs, CRUD operations, session auth, responsive UI

---

## 📸 Pages

1. **Login / Register** – Auth with TDEE auto-calculation
2. **Dashboard** – Calorie ring + macro progress bars + food log
3. **Analyze** – Build a meal, see full nutrition breakdown
4. **History** – Date picker + 7-day bar chart
5. **Profile** – BMI + TDEE calculator + edit health data
