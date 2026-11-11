"""
Pulse - Student Quiz & Academic Performance System
First-Year B.Tech Computer Science Mini Project
Backend: Flask (Python)
Storage: CSV Files (users.csv, questions.csv, results.csv)
Libraries: Flask, Pandas, NumPy, Matplotlib, hashlib, csv, random, datetime, os
"""

import os
import csv
import random
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

# Import Pandas, NumPy, and Matplotlib for analytics
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend safe for Flask
import matplotlib.pyplot as plt

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'pulse_student_quiz_system_secret_key_2026'

# Define directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.csv')
RESULTS_FILE = os.path.join(DATA_DIR, 'results.csv')
CHART_FILE = os.path.join(IMAGES_DIR, 'analytics_chart.png')

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)


# =====================================================================
# HELPER FUNCTIONS (CSV & Password Operations)
# =====================================================================

def hash_password(password):
    """Hash password using SHA-256 for secure student credential storage."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def init_csv_files():
    """Create CSV files with headers if they do not already exist."""
    # 1. Users CSV
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'name', 'password', 'registered_date'])
            # Add one default sample student
            writer.writerow([
                'student1',
                'Rahul Sharma',
                hash_password('student123'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])

    # 2. Questions CSV
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'subject', 'question', 'option_a', 'option_b',
                'option_c', 'option_d', 'correct_answer', 'marks'
            ])
            # Seed beginner-friendly sample questions for C and Python
            sample_questions = [
                ['Q101', 'C Programming', 'What is the correct format specifier for printing an integer in C?', '%d', '%f', '%c', '%s', 'A', '1'],
                ['Q102', 'C Programming', 'Which of the following is NOT a valid C variable name?', 'my_var', '2count', '_count', 'total_sum', 'B', '1'],
                ['Q103', 'C Programming', 'Which operator is used to access the value at an address stored in a pointer?', '&', '*', '->', '.', 'B', '1'],
                ['Q104', 'Python', 'Which keyword is used to define a function in Python?', 'func', 'def', 'function', 'define', 'B', '1'],
                ['Q105', 'Python', 'Which of the following data types in Python is immutable?', 'List', 'Dictionary', 'Tuple', 'Set', 'C', '1'],
                ['Q106', 'Computer Basics', 'What does CPU stand for?', 'Central Processing Unit', 'Central Program Unit', 'Computer Personal Unit', 'Control Processing Utility', 'A', '1'],
                ['Q107', 'Computer Basics', 'Which type of computer memory is volatile?', 'ROM', 'RAM', 'Hard Disk', 'Flash Drive', 'B', '1'],
                ['Q108', 'Data Structures', 'Which data structure follows the Last-In-First-Out (LIFO) principle?', 'Queue', 'Stack', 'Array', 'Linked List', 'B', '1'],
                ['Q109', 'C Programming', 'Which header file is required to use printf() and scanf() in C?', '<stdlib.h>', '<math.h>', '<stdio.h>', '<string.h>', 'C', '1'],
                ['Q110', 'Python', 'What will be the output of print(2 ** 3) in Python?', '6', '8', '9', '5', 'B', '1'],
                ['Q111', 'Data Structures', 'What is the time complexity to access an element by index in an array?', 'O(1)', 'O(n)', 'O(log n)', 'O(n^2)', 'A', '1'],
                ['Q112', 'Computer Basics', 'How many bits make up 1 Byte?', '4 bits', '8 bits', '16 bits', '32 bits', 'B', '1'],
                ['Q113', 'C Programming', 'Which loop is guaranteed to execute at least once in C?', 'for', 'while', 'do-while', 'none of these', 'C', '1'],
                ['Q114', 'Python', 'Which built-in Python function returns the number of items in a list?', 'count()', 'size()', 'len()', 'length()', 'C', '1'],
                ['Q115', 'Computer Basics', 'What does HTTP stand for in computer networking?', 'HyperText Transfer Protocol', 'Hyper Transfer Tech Protocol', 'High Text Transfer Program', 'Hyperlink Text Transfer Package', 'A', '1']
            ]
            for row in sample_questions:
                writer.writerow(row)

    # 3. Results CSV
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'result_id', 'username', 'name', 'total_questions',
                'correct_answers', 'wrong_answers', 'score', 'total_marks',
                'percentage', 'grade', 'date_time'
            ])
            # Pre-fill sample records for analytics showcase
            sample_results = [
                ['R1001', 'student1', 'Rahul Sharma', '10', '8', '2', '8', '10', '80.0', 'B', '2026-11-10 11:30:22'],
                ['R1002', 'student1', 'Rahul Sharma', '10', '9', '1', '9', '10', '90.0', 'A', '2026-11-10 14:15:10'],
                ['R1003', 'priya_k', 'Priya Kapoor', '10', '7', '3', '7', '10', '70.0', 'C', '2026-11-10 16:45:00'],
                ['R1004', 'amit_v', 'Amit Verma', '10', '5', '5', '5', '10', '50.0', 'D', '2026-11-11 09:20:15']
            ]
            for row in sample_results:
                writer.writerow(row)


def read_users():
    """Read all users from users.csv into a list of dictionaries."""
    init_csv_files()
    users = []
    with open(USERS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users


def read_questions():
    """Read all questions from questions.csv into a list of dictionaries."""
    init_csv_files()
    questions = []
    with open(QUESTIONS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions


def read_results():
    """Read all quiz results from results.csv into a list of dictionaries."""
    init_csv_files()
    results = []
    with open(RESULTS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    return results


def calculate_grade(percentage):
    """
    Determine grade based on percentage:
    A : 90+
    B : 75+
    C : 60+
    D : 40+
    F : Below 40
    """
    if percentage >= 90:
        return 'A'
    elif percentage >= 75:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'


def generate_analytics_chart(df):
    """Generate a clean Matplotlib bar chart showing student quiz performance."""
    try:
        if df.empty:
            return False

        # Take up to the last 10 quiz attempts
        recent_df = df.tail(8).copy()
        recent_df['percentage'] = recent_df['percentage'].astype(float)

        # Plot labels (Student Name or Result ID)
        labels = [f"{row['name'].split()[0]}\n({row['result_id']})" for _, row in recent_df.iterrows()]
        scores = recent_df['percentage'].tolist()

        # Set figure size and bar colors
        plt.figure(figsize=(8, 4.5))
        bars = plt.bar(labels, scores, color='#3B82F6', width=0.55, edgecolor='#1D4ED8', linewidth=1)

        # Draw a benchmark average line
        avg_score = float(np.mean(scores))
        plt.axhline(avg_score, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Recent Avg: {avg_score:.1f}%')

        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1.5,
                     f'{int(height)}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

        # Aesthetics
        plt.title('Recent Student Quiz Performance', fontsize=13, fontweight='bold', pad=15, color='#0F172A')
        plt.xlabel('Student Quiz Attempts', fontsize=10, labelpad=8, color='#334155')
        plt.ylabel('Percentage Scored (%)', fontsize=10, labelpad=8, color='#334155')
        plt.ylim(0, 115)
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        plt.legend(loc='upper right', framealpha=0.9)
        plt.tight_layout()

        # Save to static image directory
        plt.savefig(CHART_FILE, dpi=120)
        plt.close()
        return True
    except Exception as e:
        print(f"Error generating chart: {e}")
        plt.close()
        return False


# Initialize data files on application startup
init_csv_files()


# =====================================================================
# FLASK ROUTES
# =====================================================================

@app.route('/')
def home():
    """Home page route displaying welcome banner and portal navigation."""
    total_questions = len(read_questions())
    return render_template('index.html', total_questions=total_questions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration: handles form submission, duplicate checks, and password hashing."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()

        # Validation: Check for empty fields
        if not username or not name or not password:
            flash('All fields are required. Please fill in all details.', 'error')
            return render_template('register.html')

        # Validation: Check if username already exists
        users = read_users()
        for user in users:
            if user['username'].lower() == username.lower():
                flash('This username is already taken. Please choose another.', 'error')
                return render_template('register.html')

        # Hash password and save new student record
        hashed_pwd = hash_password(password)
        reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(USERS_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, name, hashed_pwd, reg_date])

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Student login: verifies credentials from users.csv and sets Flask session."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        # Read users and match hashed password
        users = read_users()
        hashed_pwd = hash_password(password)
        matched_user = None

        for user in users:
            if user['username'].lower() == username.lower() and user['password'] == hashed_pwd:
                matched_user = user
                break

        if matched_user:
            # Set session variables
            session['logged_in'] = True
            session['username'] = matched_user['username']
            session['name'] = matched_user['name']
            session['role'] = 'student'
            flash(f"Welcome back, {matched_user['name']}!", 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out current user or admin and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login: validates hardcoded admin credentials (admin / admin123)."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Hardcoded admin credentials as requested
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = 'admin'
            session['name'] = 'Administrator'
            session['role'] = 'admin'
            flash('Admin authentication successful.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials. Access denied.', 'error')
            return render_template('admin_login.html')

    return render_template('admin_login.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    """Admin dashboard: view, manage questions, and see overall question bank stats."""
    if session.get('role') != 'admin':
        flash('Unauthorized access! Please login as administrator.', 'error')
        return redirect(url_for('admin_login'))

    questions = read_questions()
    total_q = len(questions)
    subjects = list(set(q.get('subject', 'General') for q in questions))

    return render_template('admin_dashboard.html',
                           questions=questions,
                           total_questions=total_q,
                           subjects=subjects)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    """Admin route to create and append a new question to questions.csv."""
    if session.get('role') != 'admin':
        flash('Unauthorized access! Please login as administrator.', 'error')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        question_text = request.form.get('question', '').strip()
        opt_a = request.form.get('option_a', '').strip()
        opt_b = request.form.get('option_b', '').strip()
        opt_c = request.form.get('option_c', '').strip()
        opt_d = request.form.get('option_d', '').strip()
        correct_answer = request.form.get('correct_answer', '').strip().upper()
        marks = request.form.get('marks', '1').strip()

        # Form validation
        if not (subject and question_text and opt_a and opt_b and opt_c and opt_d and correct_answer):
            flash('All question fields and options are required.', 'error')
            return redirect(url_for('admin_dashboard'))

        if correct_answer not in ['A', 'B', 'C', 'D']:
            flash('Correct answer must be one of A, B, C, or D.', 'error')
            return redirect(url_for('admin_dashboard'))

        # Automatically generate next Question ID
        questions = read_questions()
        numeric_ids = []
        for q in questions:
            raw_id = q.get('id', '')
            digits = ''.join(c for c in raw_id if c.isdigit())
            if digits:
                numeric_ids.append(int(digits))
        next_id_num = max(numeric_ids) + 1 if numeric_ids else 101
        new_id = f"Q{next_id_num}"

        # Write to questions.csv
        with open(QUESTIONS_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                new_id, subject, question_text, opt_a, opt_b, opt_c, opt_d, correct_answer, marks or '1'
            ])

        flash(f'Question {new_id} added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return redirect(url_for('admin_dashboard'))


@app.route('/delete-question/<id>', methods=['GET', 'POST'])
def delete_question(id):
    """Admin route to delete a question by its Question ID."""
    if session.get('role') != 'admin':
        flash('Unauthorized access! Please login as administrator.', 'error')
        return redirect(url_for('admin_login'))

    questions = read_questions()
    filtered = [q for q in questions if q.get('id') != id]

    if len(filtered) == len(questions):
        flash(f'Question {id} not found.', 'error')
    else:
        # Rewrite questions.csv with remaining questions
        with open(QUESTIONS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'subject', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'marks'])
            for q in filtered:
                writer.writerow([
                    q['id'], q['subject'], q['question'],
                    q['option_a'], q['option_b'], q['option_c'],
                    q['option_d'], q['correct_answer'], q['marks']
                ])
        flash(f'Question {id} has been deleted.', 'info')

    return redirect(url_for('admin_dashboard'))


@app.route('/quiz')
def quiz():
    """Student Quiz: randomly selects 10 questions and displays them on one page without timer."""
    # Check student login
    if not session.get('logged_in') or session.get('role') != 'student':
        flash('Please login as a student to attempt the quiz.', 'error')
        return redirect(url_for('login'))

    all_questions = read_questions()
    if not all_questions:
        flash('No questions are currently available. Please contact administrator.', 'error')
        return render_template('quiz.html', questions=[])

    # Randomly select 10 questions (or all if fewer than 10 available)
    count = min(10, len(all_questions))
    selected_questions = random.sample(all_questions, count)

    # Store selected question IDs in session so evaluation is exact
    session['quiz_question_ids'] = [q['id'] for q in selected_questions]

    return render_template('quiz.html', questions=selected_questions)


@app.route('/submit', methods=['POST'])
def submit():
    """Processes submitted quiz answers, calculates score & grade, and saves to results.csv."""
    if not session.get('logged_in') or session.get('role') != 'student':
        flash('Session expired or unauthorized. Please login again.', 'error')
        return redirect(url_for('login'))

    question_ids = session.get('quiz_question_ids', [])
    if not question_ids:
        flash('No active quiz session found. Please start a new quiz.', 'error')
        return redirect(url_for('quiz'))

    all_questions = read_questions()
    question_dict = {q['id']: q for q in all_questions}

    total_questions = len(question_ids)
    correct_count = 0
    wrong_count = 0
    earned_score = 0
    total_marks = 0

    # Evaluate each question
    for qid in question_ids:
        q = question_dict.get(qid)
        if not q:
            continue

        q_marks = int(q.get('marks', 1))
        total_marks += q_marks

        # Student's selected answer from radio button (name="q_<id>")
        selected_option = request.form.get(f"q_{qid}")
        correct_option = q.get('correct_answer', '').strip().upper()

        if selected_option and selected_option.strip().upper() == correct_option:
            correct_count += 1
            earned_score += q_marks
        else:
            wrong_count += 1

    # Calculate percentage and grade
    if total_marks > 0:
        percentage = round((earned_score / total_marks) * 100, 2)
    else:
        percentage = 0.0

    grade = calculate_grade(percentage)

    # Generate unique Result ID
    results = read_results()
    result_id = f"R{1001 + len(results)}"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to results.csv
    username = session.get('username', 'anonymous')
    student_name = session.get('name', 'Student')

    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            result_id, username, student_name, total_questions,
            correct_count, wrong_count, earned_score, total_marks,
            percentage, grade, current_time
        ])

    # Store result details in session to render on result page
    session['last_result'] = {
        'result_id': result_id,
        'student_name': student_name,
        'username': username,
        'total_questions': total_questions,
        'correct_answers': correct_count,
        'wrong_answers': wrong_count,
        'score': earned_score,
        'total_marks': total_marks,
        'percentage': percentage,
        'grade': grade,
        'date_time': current_time
    }

    # Clear active quiz question list from session
    session.pop('quiz_question_ids', None)

    return redirect(url_for('result'))


@app.route('/result')
def result():
    """Result page: displays latest quiz result with score, percentage, and grade."""
    result_data = session.get('last_result')
    if not result_data:
        flash('No recent quiz result found. Attempt a quiz first.', 'info')
        return redirect(url_for('quiz'))

    return render_template('result.html', result=result_data)


@app.route('/analytics')
def analytics():
    """Analytics page: uses Pandas & NumPy to calculate summary statistics and Matplotlib to render chart."""
    init_csv_files()

    try:
        df = pd.read_csv(RESULTS_FILE)
    except Exception as e:
        df = pd.DataFrame()

    has_data = not df.empty and len(df) > 0

    if has_data:
        # Convert numeric columns safely
        df['percentage'] = pd.to_numeric(df['percentage'], errors='coerce').fillna(0.0)
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['total_marks'] = pd.to_numeric(df['total_marks'], errors='coerce').fillna(0)

        # Calculations using Pandas and NumPy
        highest_score = float(df['percentage'].max())
        lowest_score = float(df['percentage'].min())
        average_score = float(np.round(np.mean(df['percentage'].values), 2))
        total_attempts = int(len(df))

        # Generate Matplotlib Chart
        generate_analytics_chart(df)

        # Convert records for recent attempts table
        recent_records = df.tail(10).to_dict(orient='records')
        recent_records.reverse()  # Newest first
    else:
        highest_score = 0.0
        lowest_score = 0.0
        average_score = 0.0
        total_attempts = 0
        recent_records = []

    # Timestamp to bust browser image cache
    cache_buster = int(datetime.now().timestamp())

    return render_template('analytics.html',
                           has_data=has_data,
                           highest_score=highest_score,
                           lowest_score=lowest_score,
                           average_score=average_score,
                           total_attempts=total_attempts,
                           recent_records=recent_records,
                           cache_buster=cache_buster)


# =====================================================================
# APP ENTRY POINT
# =====================================================================
if __name__ == '__main__':
    # Run development server locally
    app.run(debug=True, host='127.0.0.1', port=5000)
