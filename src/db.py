import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# --- Supabase Initialization ---
try:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    supabase = None

# --- Database Functions ---

def log_solve(user_id: str, start_state: list, solution_steps: list, solve_time: float, moves: int):
    """Logs a successful cube solve attempt to the 'solves' table."""
    if not supabase:
        print("Database not connected. Skipping log.")
        return

    data = {
        "user_id": user_id,
        "start_state": start_state,
        "solution_steps": solution_steps,
        "solve_time": solve_time,
        "moves_count": moves,
    }
    
    try:
        # Assuming you have a table named 'solves' configured in Supabase
        response = supabase.table("solves").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Supabase log error: {e}")
        return None

def fetch_analytics(user_id: str):
    """Fetches solve history for the analytics dashboard."""
    if not supabase:
        return []
    
    try:
        # Fetch up to 100 recent solves for the user
        response = supabase.table("solves").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(100).execute()
        return response.data
    except Exception as e:
        print(f"Supabase fetch error: {e}")
        return []