import streamlit as st
import requests
import json
import numpy as np
from src.db import fetch_analytics # Import DB functions for analytics

# --- Configuration ---
# Set the API URL based on where your FastAPI app is running
API_URL = "http://localhost:8000" 
FASTAPI_SOLVE_ENDPOINT = f"{API_URL}/solve"

# Standard 6 Rubik's colors for the UI (Matches the description/logic)
COLORS = {
    'W': '#FFFFFF', # White
    'Y': '#FFFF00', # Yellow
    'R': '#FF0000', # Red
    'O': '#FFA500', # Orange
    'G': '#00FF00', # Green
    'B': '#0000FF', # Blue
}
FACE_NAMES = ['Up (U)', 'Left (L)', 'Front (F)', 'Right (R)', 'Back (B)', 'Down (D)']

# Initial solved state (W, O, G, R, B, Y)
INITIAL_STATE = ['W'] * 9 + ['O'] * 9 + ['G'] * 9 + ['R'] * 9 + ['B'] * 9 + ['Y'] * 9

# --- Streamlit Session State Management ---

def initialize_session():
    """Initializes necessary variables in Streamlit's session state."""
    if 'cube_state' not in st.session_state:
        st.session_state['cube_state'] = INITIAL_STATE
    if 'current_color' not in st.session_state:
        st.session_state['current_color'] = 'W' # Default color picker
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = 'anonymous' # Placeholder for auth
    if 'solution' not in st.session_state:
        st.session_state['solution'] = None

# --- UI Components ---

def cube_sticker(index):
    """Generates an interactive sticker button for the cube input GUI."""
    
    def on_click():
        """Updates the sticker color on click."""
        new_state = list(st.session_state.cube_state)
        new_state[index] = st.session_state.current_color
        st.session_state.cube_state = new_state
    
    # Custom HTML for a colored square button
    st.markdown(
        f"""
        <style>
            .sticker-button-{index} {{
                background-color: {COLORS[st.session_state.cube_state[index]]};
                border: 1px solid #333;
                width: 30px;
                height: 30px;
                padding: 0;
                margin: 1px;
                cursor: pointer;
            }}
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Use a Streamlit button with custom styling
    st.button("", key=f"sticker_{index}", on_click=on_click, help=f"Set to {st.session_state.current_color}", 
              key=f"btn_{index}", disabled=st.session_state.solution is not None)

def render_cube_input():
    """Renders the 2D manual cube input interface."""
    
    st.header("1. Input Cube State")
    st.write("Click a color below, then click the cube stickers to set the state.")
    
    # Color Picker
    st.session_state.current_color = st.radio(
        "Select Color:",
        list(COLORS.keys()),
        format_func=lambda c: f"{c}",
        horizontal=True
    )
    
    st.markdown("---")
    
    # Layout the 6 faces in a common 2D net pattern (L, U, R, D, F, B is typical, but we use our array order)
    face_indices = np.arange(54).reshape(6, 9)
    cols = st.columns([1, 2, 2, 2, 1])

    # 1. Up Face (U) - Positioned in the second column
    with cols[2]:
        st.subheader(FACE_NAMES[0])
        for row in range(3):
            st.columns([1, 1, 1], gap="small")
            c = st.columns(3, gap="small")
            for col in range(3):
                idx = face_indices[0, row * 3 + col]
                with c[col]:
                    cube_sticker(idx)
    
    # 2. Left, Front, Right, Back Faces (L, F, R, B) - Horizontal belt
    st.markdown("---")
    belt_cols = st.columns(4, gap="large")

    # Order: L, F, R, B
    belt_faces = [1, 2, 3, 4] 
    
    for i, face_idx in enumerate(belt_faces):
        with belt_cols[i]:
            st.subheader(FACE_NAMES[face_idx])
            for row in range(3):
                c = st.columns(3, gap="small")
                for col in range(3):
                    idx = face_indices[face_idx, row * 3 + col]
                    with c[col]:
                        cube_sticker(idx)

    # 3. Down Face (D) - Positioned in the second column
    st.markdown("---")
    down_cols = st.columns([1, 2, 2, 2, 1])
    with down_cols[2]:
        st.subheader(FACE_NAMES[5])
        for row in range(3):
            c = st.columns(3, gap="small")
            for col in range(3):
                idx = face_indices[5, row * 3 + col]
                with c[col]:
                    cube_sticker(idx)


def render_solution_output():
    """Renders the solution steps and metrics."""
    solution_data = st.session_state.solution
    if not solution_data:
        return

    st.header("3. Solution & Analytics 🏆")

    col1, col2, col3 = st.columns(3)
    col1.metric("Solve Time", f"{solution_data['time']:.3f}s")
    col2.metric("Moves Count", f"{solution_data['moves']}")
    col3.metric("Algorithm", "Kociemba (Optimal)")

    st.subheader("Step-by-Step Moves (Standard Notation)")
    
    solution_steps = solution_data['solution']
    # Format steps: R U R' F2 L...
    solution_text = " ".join(solution_steps) 
    
    st.code(solution_text, language='text')

    # Add optional move-by-move visualization placeholder here (e.g., in a expander)
    with st.expander("Visualization Placeholder"):
        st.markdown(f"**Total Moves:** {len(solution_steps)}. Click a move to apply it to a 3D model (requires a separate library like `pythreejs` which is complex for Streamlit).")
        st.markdown("For this implementation, the solution is purely text-based.")


def render_analytics_dashboard():
    """Renders the user's solve history and statistics."""
    st.header("Analytics Dashboard 📈")
    
    user_id = st.session_state.user_id
    if user_id == 'anonymous':
        st.warning("Log in to see your personalized solve history and statistics.")
        st.text_input("Simulated User ID (for demo):", value=user_id, key="temp_user_id_input")
        if st.session_state.temp_user_id_input != 'anonymous' and st.session_state.temp_user_id_input:
             st.session_state.user_id = st.session_state.temp_user_id_input
        if st.session_state.user_id == 'anonymous':
            return
    
    data = fetch_analytics(st.session_state.user_id)
    
    if not data:
        st.info(f"No solve history found for User ID: **{st.session_state.user_id}**.")
        return

    # Calculate average stats
    moves = [d['moves_count'] for d in data]
    times = [d['solve_time'] for d in data]
    
    st.markdown(f"**Showing {len(data)} solves** for User ID: **{st.session_state.user_id}**")
    
    colA, colB = st.columns(2)
    colA.metric("Avg. Moves", f"{np.mean(moves):.1f}")
    colB.metric("Avg. Time", f"{np.mean(times):.3f}s")
    
    st.subheader("Solve History")
    # Clean up data for display
    display_data = [{
        'Time': item['solve_time'],
        'Moves': item['moves_count'],
        'Date': item['created_at'][:10],
        'Solution': " ".join(item['solution_steps'][:5]) + "..." # Truncate solution
    } for item in data]
    st.dataframe(display_data, use_container_width=True)


# --- Solver Function ---

def call_solver_api():
    """Handles the button click, calls the FastAPI endpoint, and updates state."""
    st.session_state.solution = None
    
    # 1. Prepare data
    payload = {
        "state": st.session_state.cube_state,
        "user_id": st.session_state.user_id
    }
    
    try:
        # 2. Send request to FastAPI
        response = requests.post(FASTAPI_SOLVE_ENDPOINT, json=payload, timeout=30)
        
        # 3. Handle response
        if response.status_code == 200:
            st.session_state.solution = response.json()
            st.success(st.session_state.solution.get("message", "Solution generated successfully!"))
        else:
            error_detail = response.json().get("detail", "Unknown error")
            st.error(f"Solver API Error ({response.status_code}): {error_detail}")

    except requests.exceptions.ConnectionError:
        st.error(f"Connection Error: Could not connect to the FastAPI backend at {API_URL}. Ensure the API is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


# --- Main Application Layout ---

def main():
    st.set_page_config(layout="wide", page_title="CubeLogic Solver")
    initialize_session()

    st.title("CubeLogic: Full-Stack Rubik's Cube Solver 🧩")
    st.markdown("A full-stack application demonstrating core algorithms and data handling (FastAPI, Streamlit, Supabase, Kociemba).")
    st.markdown("---")

    # Use tabs for a cleaner interface
    tab1, tab2 = st.tabs(["Solver", "Analytics"])

    with tab1:
        # --- Solver Interface ---
        
        render_cube_input()
        
        st.markdown("---")
        
        st.header("2. Generate Solution")
        
        col_solve, col_reset = st.columns([1, 4])
        
        with col_solve:
            st.button(
                "🚀 Solve Cube", 
                on_click=call_solver_api, 
                use_container_width=True, 
                type="primary",
                disabled=st.session_state.solution is not None
            )
            
        with col_reset:
            if st.button("🔄 Reset Input", use_container_width=False):
                st.session_state.cube_state = INITIAL_STATE
                st.session_state.solution = None
                st.experimental_rerun() 
        
        st.markdown("---")
        
        render_solution_output()

    with tab2:
        # --- Analytics Dashboard ---
        render_analytics_dashboard()


if __name__ == '__main__':
    main()