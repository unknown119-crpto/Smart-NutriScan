from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os
import json
from datetime import datetime, date
import hashlib

app = Flask(__name__)
app.secret_key = 'smart-nutrition-secret-key-2024'

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'nutrition.db')

# ─────────────────────────────────────────
# Database helpers
# ─────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with get_db() as conn:
        conn.executescript(open(os.path.join(os.path.dirname(__file__), 'schema.sql')).read())
        seed_foods(conn)
    print("✅ Database initialized.")


def seed_foods(conn):
    existing = conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
    if existing >= 50:
        return

    foods = [
        # name, category, calories, protein, carbs, fat, fiber, sugar, sodium, serving_size, serving_unit
        ("Apple", "Fruits", 95, 0.5, 25.1, 0.3, 4.4, 19.0, 2, 182, "g"),
        ("Banana", "Fruits", 105, 1.3, 27.0, 0.4, 3.1, 14.4, 1, 118, "g"),
        ("Orange", "Fruits", 62, 1.2, 15.4, 0.2, 3.1, 12.2, 0, 131, "g"),
        ("Strawberries", "Fruits", 49, 1.0, 11.7, 0.5, 3.0, 7.4, 1, 152, "g"),
        ("Grapes", "Fruits", 104, 1.1, 27.3, 0.2, 1.4, 23.4, 3, 151, "g"),
        ("Watermelon", "Fruits", 86, 1.7, 21.6, 0.4, 1.1, 17.7, 3, 286, "g"),
        ("Mango", "Fruits", 202, 2.8, 50.0, 1.3, 5.4, 46.1, 4, 336, "g"),
        ("Pineapple", "Fruits", 82, 0.9, 21.6, 0.2, 2.3, 16.3, 2, 165, "g"),

        ("Broccoli", "Vegetables", 55, 3.7, 11.2, 0.6, 5.1, 2.6, 64, 148, "g"),
        ("Spinach", "Vegetables", 7, 0.9, 1.1, 0.1, 0.7, 0.1, 24, 30, "g"),
        ("Carrot", "Vegetables", 52, 1.2, 12.3, 0.3, 3.6, 6.1, 88, 128, "g"),
        ("Tomato", "Vegetables", 35, 1.7, 7.6, 0.4, 2.3, 5.1, 10, 182, "g"),
        ("Cucumber", "Vegetables", 16, 0.7, 3.8, 0.1, 0.5, 1.7, 2, 119, "g"),
        ("Sweet Potato", "Vegetables", 103, 2.3, 23.6, 0.1, 3.8, 4.7, 41, 130, "g"),
        ("Corn", "Vegetables", 132, 4.9, 29.0, 1.8, 3.6, 5.0, 23, 154, "g"),
        ("Potato", "Vegetables", 163, 4.3, 36.6, 0.2, 3.8, 1.7, 17, 213, "g"),
        ("Onion", "Vegetables", 44, 1.2, 10.3, 0.1, 1.9, 4.7, 4, 110, "g"),
        ("Garlic", "Vegetables", 42, 1.8, 9.4, 0.1, 0.6, 0.3, 5, 136, "g"),

        ("Chicken Breast", "Proteins", 165, 31.0, 0.0, 3.6, 0.0, 0.0, 74, 100, "g"),
        ("Egg", "Proteins", 78, 6.3, 0.6, 5.3, 0.0, 0.6, 62, 50, "g"),
        ("Tuna (canned)", "Proteins", 109, 24.4, 0.0, 0.8, 0.0, 0.0, 303, 85, "g"),
        ("Salmon", "Proteins", 208, 20.1, 0.0, 13.4, 0.0, 0.0, 59, 100, "g"),
        ("Ground Beef (lean)", "Proteins", 218, 26.1, 0.0, 12.0, 0.0, 0.0, 76, 100, "g"),
        ("Lentils (cooked)", "Proteins", 230, 17.9, 39.9, 0.8, 15.6, 3.6, 4, 198, "g"),
        ("Chickpeas (cooked)", "Proteins", 269, 14.5, 44.7, 4.2, 12.5, 7.9, 11, 164, "g"),
        ("Black Beans (cooked)", "Proteins", 227, 15.2, 40.8, 0.9, 15.0, 0.6, 2, 172, "g"),
        ("Tofu (firm)", "Proteins", 94, 10.0, 2.3, 4.8, 0.3, 0.6, 9, 126, "g"),
        ("Shrimp", "Proteins", 84, 17.8, 0.0, 0.9, 0.0, 0.0, 190, 100, "g"),

        ("Whole Milk", "Dairy", 149, 8.0, 11.7, 8.0, 0.0, 12.3, 105, 244, "ml"),
        ("Greek Yogurt (plain)", "Dairy", 100, 17.3, 6.1, 0.7, 0.0, 6.1, 56, 170, "g"),
        ("Cheddar Cheese", "Dairy", 113, 7.0, 0.4, 9.3, 0.0, 0.1, 174, 28, "g"),
        ("Cottage Cheese", "Dairy", 206, 25.0, 8.2, 9.0, 0.0, 6.2, 764, 226, "g"),
        ("Butter", "Dairy", 102, 0.1, 0.0, 11.5, 0.0, 0.0, 82, 14, "g"),

        ("White Rice (cooked)", "Grains", 206, 4.3, 44.5, 0.4, 0.6, 0.1, 1, 186, "g"),
        ("Brown Rice (cooked)", "Grains", 216, 5.0, 44.8, 1.8, 3.5, 0.7, 10, 195, "g"),
        ("Oats (dry)", "Grains", 307, 10.7, 55.0, 5.3, 8.2, 1.1, 2, 80, "g"),
        ("Whole Wheat Bread", "Grains", 69, 3.6, 11.6, 1.1, 1.9, 1.4, 132, 28, "g"),
        ("White Bread", "Grains", 79, 2.7, 15.1, 1.0, 0.6, 1.4, 142, 28, "g"),
        ("Pasta (cooked)", "Grains", 220, 8.1, 43.2, 1.3, 2.5, 0.6, 1, 140, "g"),
        ("Quinoa (cooked)", "Grains", 222, 8.1, 39.4, 3.6, 5.2, 1.6, 13, 185, "g"),
        ("Corn Tortilla", "Grains", 52, 1.4, 10.7, 0.7, 1.4, 0.2, 11, 26, "g"),

        ("Almonds", "Nuts & Seeds", 164, 6.0, 6.1, 14.2, 3.5, 1.2, 0, 28, "g"),
        ("Walnuts", "Nuts & Seeds", 185, 4.3, 3.9, 18.5, 1.9, 0.7, 1, 28, "g"),
        ("Peanut Butter", "Nuts & Seeds", 188, 8.0, 6.9, 16.1, 1.9, 2.5, 136, 32, "g"),
        ("Chia Seeds", "Nuts & Seeds", 138, 4.7, 11.9, 8.7, 9.8, 0.0, 5, 28, "g"),
        ("Sunflower Seeds", "Nuts & Seeds", 165, 5.5, 6.8, 14.4, 2.4, 1.4, 1, 28, "g"),
        ("Flaxseeds", "Nuts & Seeds", 150, 5.2, 8.1, 12.0, 7.6, 0.4, 9, 28, "g"),
        ("Cashews", "Nuts & Seeds", 157, 5.2, 8.6, 12.4, 0.9, 1.7, 3, 28, "g"),
        ("Pumpkin Seeds", "Nuts & Seeds", 151, 7.0, 5.0, 13.0, 1.1, 0.4, 5, 28, "g"),

        ("Olive Oil", "Oils & Fats", 119, 0.0, 0.0, 13.5, 0.0, 0.0, 0, 13, "ml"),
        ("Avocado", "Fruits", 234, 2.9, 12.5, 21.4, 9.8, 0.4, 11, 150, "g"),
        ("Coconut Oil", "Oils & Fats", 117, 0.0, 0.0, 13.6, 0.0, 0.0, 0, 13, "ml"),

        ("Orange Juice", "Beverages", 112, 1.7, 25.8, 0.5, 0.5, 20.8, 2, 240, "ml"),
        ("Green Tea", "Beverages", 2, 0.0, 0.5, 0.0, 0.0, 0.0, 2, 240, "ml"),
        ("Black Coffee", "Beverages", 2, 0.3, 0.0, 0.0, 0.0, 0.0, 5, 240, "ml"),
        ("Protein Shake (vanilla)", "Supplements", 130, 25.0, 6.0, 1.5, 1.0, 3.0, 160, 300, "ml"),
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO foods
        (name, category, calories, protein, carbs, fat, fiber, sugar, sodium, serving_size, serving_unit)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, foods)
    conn.commit()


# ─────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def logged_in():
    return 'user_id' in session


# ─────────────────────────────────────────
# Routes – Auth
# ─────────────────────────────────────────

@app.route('/')
def index():
    if logged_in():
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        age = data.get('age', 25)
        weight = data.get('weight', 70)
        height = data.get('height', 170)
        gender = data.get('gender', 'male')
        activity = data.get('activity_level', 'moderate')

        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'All fields are required.'})

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            return jsonify({'success': False, 'message': 'Email already registered.'})

        # Calculate BMR (Mifflin-St Jeor)
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
        tdee = round(bmr * multipliers.get(activity, 1.55))

        db.execute("""
            INSERT INTO users (name, email, password_hash, age, weight_kg, height_cm, gender, activity_level, daily_calorie_goal)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (name, email, hash_password(password), age, weight, height, gender, activity, tdee))
        db.commit()
        return jsonify({'success': True, 'message': 'Account created! Please login.'})
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password_hash=?",
                          (email, hash_password(password))).fetchone()
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid email or password.'})
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ─────────────────────────────────────────
# Routes – Main Pages
# ─────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()
    today = date.today().isoformat()
    logs = db.execute("""
        SELECT fl.*, f.name, f.category FROM food_logs fl
        JOIN foods f ON fl.food_id = f.id
        WHERE fl.user_id=? AND fl.log_date=?
        ORDER BY fl.created_at DESC
    """, (session['user_id'], today)).fetchall()

    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
    for log in logs:
        ratio = log['quantity_g'] / 100.0
        totals['calories'] += round(log['calories_per_100g'] * ratio)
        totals['protein'] += round(log['protein_per_100g'] * ratio, 1)
        totals['carbs'] += round(log['carbs_per_100g'] * ratio, 1)
        totals['fat'] += round(log['fat_per_100g'] * ratio, 1)
        totals['fiber'] += round(log['fiber_per_100g'] * ratio, 1)

    return render_template('dashboard.html', user=user, logs=logs, totals=totals, today=today)


@app.route('/analyze')
def analyze():
    if not logged_in():
        return redirect(url_for('login'))
    db = get_db()
    categories = db.execute("SELECT DISTINCT category FROM foods ORDER BY category").fetchall()
    return render_template('analyze.html', categories=categories)


@app.route('/history')
def history():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('history.html')


@app.route('/profile')
def profile():
    if not logged_in():
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()
    return render_template('profile.html', user=user)


# ─────────────────────────────────────────
# API – Foods
# ─────────────────────────────────────────

@app.route('/api/foods/search')
def search_foods():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    db = get_db()
    if category:
        foods = db.execute(
            "SELECT * FROM foods WHERE category=? ORDER BY name", (category,)
        ).fetchall()
    elif q:
        foods = db.execute(
            "SELECT * FROM foods WHERE name LIKE ? ORDER BY name", (f'%{q}%',)
        ).fetchall()
    else:
        foods = db.execute("SELECT * FROM foods ORDER BY category, name").fetchall()
    return jsonify([dict(f) for f in foods])


@app.route('/api/foods/<int:food_id>')
def get_food(food_id):
    db = get_db()
    food = db.execute("SELECT * FROM foods WHERE id=?", (food_id,)).fetchone()
    if food:
        return jsonify(dict(food))
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/foods/add', methods=['POST'])
def add_custom_food():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    db = get_db()
    db.execute("""
        INSERT INTO foods (name, category, calories, protein, carbs, fat, fiber, sugar, sodium, serving_size, serving_unit, created_by)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (data['name'], data.get('category','Custom'), data['calories'], data.get('protein',0),
          data.get('carbs',0), data.get('fat',0), data.get('fiber',0), data.get('sugar',0),
          data.get('sodium',0), data.get('serving_size',100), data.get('serving_unit','g'),
          session['user_id']))
    db.commit()
    return jsonify({'success': True})


# ─────────────────────────────────────────
# API – Food Logs
# ─────────────────────────────────────────

@app.route('/api/log', methods=['POST'])
def log_food():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    db = get_db()
    food = db.execute("SELECT * FROM foods WHERE id=?", (data['food_id'],)).fetchone()
    if not food:
        return jsonify({'error': 'Food not found'}), 404

    ratio = data['quantity_g'] / 100.0
    db.execute("""
        INSERT INTO food_logs
        (user_id, food_id, quantity_g, meal_type, log_date,
         calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (session['user_id'], data['food_id'], data['quantity_g'],
          data.get('meal_type', 'lunch'), data.get('log_date', date.today().isoformat()),
          food['calories'], food['protein'], food['carbs'], food['fat'], food['fiber']))
    db.commit()
    return jsonify({'success': True})


@app.route('/api/log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    db.execute("DELETE FROM food_logs WHERE id=? AND user_id=?", (log_id, session['user_id']))
    db.commit()
    return jsonify({'success': True})


@app.route('/api/logs')
def get_logs():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    log_date = request.args.get('date', date.today().isoformat())
    db = get_db()
    logs = db.execute("""
        SELECT fl.*, f.name AS food_name, f.category FROM food_logs fl
        JOIN foods f ON fl.food_id = f.id
        WHERE fl.user_id=? AND fl.log_date=?
        ORDER BY fl.meal_type, fl.created_at
    """, (session['user_id'], log_date)).fetchall()
    return jsonify([dict(l) for l in logs])


@app.route('/api/logs/week')
def get_week_logs():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    rows = db.execute("""
        SELECT log_date,
               SUM(calories_per_100g * quantity_g / 100.0) AS total_cal,
               SUM(protein_per_100g * quantity_g / 100.0) AS total_protein,
               SUM(carbs_per_100g * quantity_g / 100.0) AS total_carbs,
               SUM(fat_per_100g * quantity_g / 100.0) AS total_fat
        FROM food_logs
        WHERE user_id=? AND log_date >= date('now','-6 days')
        GROUP BY log_date ORDER BY log_date
    """, (session['user_id'],)).fetchall()
    return jsonify([dict(r) for r in rows])


# ─────────────────────────────────────────
# API – Profile update
# ─────────────────────────────────────────

@app.route('/api/profile', methods=['POST'])
def update_profile():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    db = get_db()
    weight = float(data.get('weight_kg', 70))
    height = float(data.get('height_cm', 170))
    age = int(data.get('age', 25))
    gender = data.get('gender', 'male')
    activity = data.get('activity_level', 'moderate')
    goal_cal = int(data.get('daily_calorie_goal', 2000))

    db.execute("""
        UPDATE users SET weight_kg=?, height_cm=?, age=?, gender=?, activity_level=?, daily_calorie_goal=?
        WHERE id=?
    """, (weight, height, age, gender, activity, goal_cal, session['user_id']))
    db.commit()
    return jsonify({'success': True})


# ─────────────────────────────────────────
# API – Nutrition analysis
# ─────────────────────────────────────────

@app.route('/api/analyze', methods=['POST'])
def analyze_nutrition():
    data = request.get_json()
    foods_list = data.get('foods', [])  # [{food_id, quantity_g}, ...]
    db = get_db()
    result = {
        'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0,
        'fiber': 0, 'sugar': 0, 'sodium': 0,
        'foods': [], 'warnings': [], 'tips': []
    }

    for item in foods_list:
        food = db.execute("SELECT * FROM foods WHERE id=?", (item['food_id'],)).fetchone()
        if not food:
            continue
        ratio = item['quantity_g'] / 100.0
        cal = round(food['calories'] * ratio, 1)
        p = round(food['protein'] * ratio, 1)
        c = round(food['carbs'] * ratio, 1)
        f = round(food['fat'] * ratio, 1)
        fi = round(food['fiber'] * ratio, 1)
        s = round(food['sugar'] * ratio, 1)
        na = round(food['sodium'] * ratio, 1)

        result['calories'] += cal
        result['protein'] += p
        result['carbs'] += c
        result['fat'] += f
        result['fiber'] += fi
        result['sugar'] += s
        result['sodium'] += na

        result['foods'].append({
            'name': food['name'], 'category': food['category'],
            'quantity_g': item['quantity_g'],
            'calories': cal, 'protein': p, 'carbs': c, 'fat': f, 'fiber': fi
        })

    # Round totals
    for k in ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'sodium']:
        result[k] = round(result[k], 1)

    # Health tips
    if result['protein'] < 20:
        result['warnings'].append('⚠️ Low protein — consider adding chicken, eggs, or legumes.')
    if result['fiber'] < 5:
        result['warnings'].append('⚠️ Low fiber — add vegetables, fruits, or whole grains.')
    if result['sodium'] > 1000:
        result['warnings'].append('⚠️ High sodium content — be mindful of daily intake.')
    if result['sugar'] > 50:
        result['warnings'].append('⚠️ High sugar content in this meal.')

    if result['protein'] >= 20:
        result['tips'].append('✅ Good protein content!')
    if result['fiber'] >= 8:
        result['tips'].append('✅ Excellent fiber intake!')
    if result['calories'] < 500:
        result['tips'].append('✅ Light and balanced meal.')

    return jsonify(result)


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("🚀 Smart Nutrition Analyzer running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
