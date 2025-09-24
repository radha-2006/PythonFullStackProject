Project Title:

CubeLogic – A Full-Stack Rubik’s Cube Solver

Project Description:

CubeLogic is a full-stack web application that allows users to input the current state of a Rubik’s Cube and generates the step-by-step solution using core Python algorithms. The project integrates a React frontend, a Flask/Django backend, and a Supabase/PostgreSQL database for storing user accounts, cube states, solutions, and performance statistics.

This project demonstrates strong skills in algorithm design, data structures, backend API development, frontend visualization, and database integration — without using AI/ML.

Features:
Frontend (User Interface)

🎨 Interactive UI built with HTML/CSS/JS (or React).

🎛️ Manual cube state input through a color picker or GUI.

🔄 Optional 2D/3D cube visualization of the solving process.

📜 Display step-by-step moves in standard Rubik’s notation (R, R’, U, etc.).

Backend (Core Logic & API)

🧮 Core Python algorithms (Layer-by-Layer or Kociemba’s method).

🌀 Cube representation using Python lists/arrays.

🔧 Move and rotation functions to manipulate cube state.

📡 Flask/Django APIs to:

Accept cube input

Process solving algorithm

Return solution steps

Database (Supabase/PostgreSQL)

👤 User authentication (login, signup).

📂 Store cube states and corresponding solutions.

📊 Save performance stats such as number of moves, solve time, and attempt history.

Additional Features

⏱️ Timer tracking for each solution.

📈 Analytics dashboard (e.g., average moves, history of solves).

🏆 Gamification: Compare user solutions with solver’s efficiency.

## Project Structure

Productivity Management System/
|
|---src/ # core application logic
| |---logic.py #Business logic and task
operations
| |**db.py #Database operations
|
|----API/ #Backend API
| |**main.py #FastAPI endpoints
|
|----Frontend/ #Frontend application
| |\__app.py #Streamlit web interface
|
|\_requirements.txt #Python Dependencies
|
|\_README.md #Project decumentation
|
|_.env #Python Variables

## Quick start

## prerequisites

-Python 3.8 or higher
-A Supabase account
-Git(push,cloning)

### 1.clone or Download the project

# option 1:clone with Git

git clone https://github.com/radha-2006/PythonFullStackProject.git

# option 2:Download and extract the ZIP file

### 2.Install Dependencies

# Install all required python packages

pip install -r requirements.txt

### 3.Set Up Supabase Database

1.Create a Supabase Project:
2.Create the Task Table:

-Go to the SQL Edition in your Supabase dashboard
-Run this SQL command:
TABLES:

1. users

Stores user account details.

users (
user_id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);

2. cubes

Stores cube configurations submitted by users.

cubes (
cube_id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(user_id),
cube_state TEXT NOT NULL, -- serialized cube configuration
created_at TIMESTAMP DEFAULT NOW()
);

3. solutions

Stores solutions generated for cube states.

solutions (
solution_id SERIAL PRIMARY KEY,
cube_id INT REFERENCES cubes(cube_id),
moves TEXT NOT NULL, -- sequence of moves
move_count INT,
solve_time FLOAT, -- time taken to compute
created_at TIMESTAMP DEFAULT NOW()
);

4. leaderboard

Tracks best performances for gamification.

leaderboard (
leaderboard_id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(user_id),
fastest_time FLOAT,
least_moves INT,
updated_at TIMESTAMP DEFAULT NOW()
);

5. stats (optional)

Tracks user history and analytics.

stats (
stat_id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(user_id),
total_solves INT DEFAULT 0,
avg_moves FLOAT,
avg_time FLOAT,
last_solve TIMESTAMP
);

```
3. **Get your Creadentials:

### 4. Configure Environment variables

1. Create a `.env` file in the project root

2. Add your Supabase credentials to `.env`
SUPABASE_URL=your_project_url_here
SUPABSE_KEY=your_anon_key_here


**Example:**
SUPABASE_URL=https://yclkogjhzzctanzpnfpb.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InljbGtvZ2poenpjdGFuenBuZnBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwOTg4MTAsImV4cCI6MjA3MzY3NDgxMH0.HLRzz9Zy1zMWeqVtErI0Z-Wht9xKFE6edUbQ2mqTFSk

### 5.Run the application

## streamlit Frontend
streamlit run forward/app.py

The app will open in your browser at `http://localhost:3000`

## FASTAPI Backend

cd API
python main.py

The App will be available at `http://localhost:8000`


# How to Use
## Technical Details


### Technologies used


-**Frontend**:Streamlit(python web frameork)
-**Backend**:FASTAPI(python REST API framework)
-**Database**:supabase(postgreSQL-based backend-as-a-service)
-**Language**:python 3.8+

### key components

1. **`src/db.py`**:Database operations
    -Handles all CRUD opeartions with supabase

2. **`src/logic.py`**:Business logic
    -Task validation and processing


## TroubleShooting

## Common Issues

1. **"Module not Found" errors**
     -Make sure you've installed all dependencies:`pip install -r requirements.txt`
     -Check that you're running commands from the correct directory

#Future Enhancements

-Support more puzzles – 2×2, 4×4, Pyraminx, etc.
-3D cube visualization with step-by-step animations.
-Mobile/PWA support for on-the-go solving.
-Leaderboards & challenges for competitive solving.
-Analytics dashboard for move counts & efficiency.
-Learning mode with hints and tutorials.
-Cloud sync for saving solves and history.
-Public API to provide solving as a service.


# support

If you encounter any issues or have questions:
Mail Id:radhasivani06@gmail.com
phone:8309655338
```
