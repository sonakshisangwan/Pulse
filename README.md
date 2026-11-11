# Pulse – Student Quiz & Academic Performance System

A lightweight, beginner-friendly web application developed as a **First-Year B.Tech Computer Science Mini Project**. 

Pulse enables students to register, attempt randomized multiple-choice subject quizzes, receive instant academic grades, and view class-wide performance analytics powered by Python data science libraries (**Pandas**, **NumPy**, and **Matplotlib**). The application stores all data transparently in CSV files without requiring complex SQL databases or heavy web frameworks.

---

## 📌 Project Overview

- **Project Title:** Pulse – Student Quiz & Academic Performance System
- **Academic Level:** 1st Year B.Tech Computer Science & Engineering
- **Domain:** Web Development & Python Data Analytics
- **Architecture:** Procedural Flask Backend + CSV Persistence + Vanilla HTML/CSS/JS

---

## 🚀 Key Features

### 1. Student Portal
- **Registration:** Students register with Full Name, Username, and Password. Passwords are encrypted using SHA-256 (`hashlib`) before being stored in `users.csv`.
- **Authentication:** Session-based authentication with duplicate username detection and input validation.
- **Randomized Quiz Engine:** Randomly selects 10 questions from the central question bank on every attempt.
- **Single-Page Quiz Interface:** All 10 questions are presented with intuitive radio buttons without restrictive timers.
- **Instant Evaluation:** Automatically grades answers against answer keys upon submission.
- **Detailed Result Summary:** Displays total questions, correct answers, wrong answers, final score, percentage, and assigned academic grade.

### 2. Academic Grading Criteria
The system automatically maps percentage scores to standard college letter grades:
- **Grade A:** 90% and above
- **Grade B:** 75% to 89%
- **Grade C:** 60% to 74%
- **Grade D:** 40% to 59%
- **Grade F:** Below 40%

### 3. Faculty & Admin Dashboard
- **Admin Authentication:** Simple administrative login (`admin` / `admin123`).
- **Question Management:** Add new questions with Subject, Question Statement, 4 Options (A, B, C, D), Correct Answer, and Marks.
- **Auto-Generated Question IDs:** Automatically increments and assigns IDs (e.g., `Q101`, `Q102`, ...).
- **Question Bank Inspection:** View all questions in a clean table and delete obsolete questions with single-click confirmation.

### 4. Data Analytics & Visualization
- **Pandas & NumPy Aggregations:** Computes highest score, lowest score, average class percentage, and total quiz attempts directly from `results.csv`.
- **Dynamic Matplotlib Visualization:** Generates and displays a bar chart comparing recent student quiz performances with the batch average score.

---

## 🛠️ Technologies Used

### Backend
- **Python 3.x**
- **Flask** (Micro web framework & session management)
- **Pandas** (Data manipulation and statistics)
- **NumPy** (Mathematical and numerical operations)
- **Matplotlib** (Static bar chart generation)
- **hashlib** (SHA-256 password hashing)
- **csv** (Tabular data storage)
- **random** (Randomized question sampling)
- **datetime** (Timestamp logging)

### Frontend
- **HTML5** (Clean semantic structure)
- **CSS3** (Custom responsive design with Flexbox, clean soft-blue `#3B82F6` accent, no external UI frameworks)
- **Vanilla JavaScript** (Form validation and quiz submission confirmation)

### Data Persistence
- `data/users.csv` – Stores registered student credentials and hashed passwords.
- `data/questions.csv` – Stores the question bank (ID, subject, question, options, correct answer, marks).
- `data/results.csv` – Stores historical quiz attempt logs and scores.

---

## 📁 Folder Structure

```text
Pulse/
├── app.py                      # Main Flask application and routing logic
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/                       # CSV database directory (auto-created if missing)
│   ├── users.csv               # Student user records
│   ├── questions.csv           # Question bank records
│   └── results.csv             # Quiz attempts and performance logs
├── templates/                  # Jinja2 HTML templates
│   ├── index.html              # Home landing page
│   ├── register.html           # Student registration page
│   ├── login.html              # Student login page
│   ├── admin_login.html        # Faculty/admin login page
│   ├── admin_dashboard.html    # Question bank management dashboard
│   ├── quiz.html               # 10-question quiz interface
│   ├── result.html             # Quiz score and grade report card
│   └── analytics.html          # Performance analytics and chart page
└── static/                     # Static assets
    ├── style.css               # Clean custom styling sheet
    ├── script.js               # Vanilla JavaScript client logic
    └── images/
        └── analytics_chart.png # Matplotlib generated chart
```

---

## ⚙️ Installation & Setup

### Prerequisites
Make sure **Python 3.8+** and `pip` are installed on your computer.

### Step 1: Open Terminal in Project Directory
Open your command prompt or terminal in the project folder:
```bash
cd "c:\Users\Sonakshi Sangwan\Desktop\1st sem\cp\mini project"
```

### Step 2: Install Required Libraries
Install Flask, Pandas, NumPy, and Matplotlib using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Credentials for Evaluation & Testing

### 1. Faculty / Admin Login
- **URL:** `http://127.0.0.1:5000/admin-login`
- **Username:** `admin`
- **Password:** `admin123`

### 2. Pre-Configured Sample Student
- **URL:** `http://127.0.0.1:5000/login`
- **Username:** `student1`
- **Password:** `student123`

*(You can also register any new student directly via the **Register** page).*

---

## 🛡️ Error Handling Implemented

- **Empty Field Validation:** Form inputs are verified on both the frontend and backend.
- **Duplicate Usernames:** Rejects registration if a username already exists in `users.csv`.
- **Invalid Credentials:** Displays user-friendly error banners if passwords or usernames do not match.
- **Question Availability:** Gracefully alerts the student if the question bank contains no questions.
- **Unanswered Quiz Warning:** Prompts students via JavaScript before submitting if questions remain unanswered.
- **Admin Access Control:** Restricts access to `/admin-dashboard` and question deletion endpoints to active admin sessions.

---

## 🔮 Future Improvements

1. **Subject-Specific Quizzes:** Allow students to select a specific category (e.g., C Programming only or Data Structures only).
2. **Timer Option:** Add an optional countdown timer for timed examinations.
3. **PDF Certificate Download:** Generate a downloadable PDF report card upon completing the quiz.
4. **Leaderboard:** Display top-ranking students across college batches.
5. **Student Profile History:** Dedicated page showing an individual student's score progression over multiple attempts.
