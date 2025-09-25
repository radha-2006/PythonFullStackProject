# src/db.py (CubeLogic Database Manager - Organized by Table)

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# --- Supabase Initialization ---
# Get connection details from the environment variables
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Create the Supabase client object
supabase: Client = create_client(url, key)


# =========================================================================
# 1. SOLVES TABLE FUNCTIONS (Core Data & Metrics)
#
# This table stores the details of every cube solution generated, 
# including the moves, time taken, and the initial state.
# =========================================================================

def log_solve(user_id: str, start_state: List[str], solution_steps: List[str], solve_time: float, moves: int):
    """Logs a successful solve attempt to the 'solves' table."""
    # Convert 'anonymous' to None for database storage if the column is nullable
    log_user_id = user_id if user_id != 'anonymous' else None
    
    return supabase.table("solves").insert({
        "user_id": log_user_id,          # UUID (or None) linking to the user
        "start_state": start_state,      # The 54-element scrambled state
        "solution_steps": solution_steps, # The list of moves (R, U', F2, etc.)
        "solve_time": solve_time,        # Time taken by the solver algorithm
        "moves_count": moves,            # Total number of moves
    }).execute()

def get_user_solves(user_id: str, limit: int = 100):
    """Fetches solve history for a specific user ID for the analytics dashboard."""
    return (
        supabase.table("solves")
        .select("solve_time, moves_count, created_at, solution_steps")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

def delete_solve(solve_id: str):
    """Deletes a specific solve record by its ID (for cleanup/admin)."""
    return supabase.table("solves").delete().eq("id", solve_id).execute()


# =========================================================================
# 2. USERS TABLE FUNCTIONS (Profile Data)
#
# This table stores public user metadata (like usernames) linked to the 
# Supabase auth.users table via the 'id' column.
# =========================================================================

def get_user_profile(user_id: str):
    """Fetches a user's profile metadata (username, join_date) from the 'users' table."""
    return supabase.table("users").select("username, join_date").eq("id", user_id).single().execute()


# =========================================================================
# 3. ANALYTICS / LEADERBOARD FUNCTIONS (Aggregation)
#
# These functions pull aggregated or calculated data, often relying on 
# PostgreSQL Views or Remote Procedure Calls (RPCs).
# =========================================================================

def get_overall_leaderboard(limit: int = 10):
    """
    Fetches the top N users based on average moves (efficiency) 
    by calling a PostgreSQL stored function.
    """
    # Requires a PostgreSQL RPC function named 'get_leaderboard' defined in your Supabase project
    return supabase.rpc('get_leaderboard', {}).limit(limit).execute()