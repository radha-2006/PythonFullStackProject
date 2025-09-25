import kociemba
from typing import List

# Standard color scheme mapping for centers:
# U(White), F(Green), R(Red), D(Yellow), L(Orange), B(Blue)
# This mapping needs to be determined based on the solved state of the input cube.

def solve_cube(cube_state_array: List[str], user_id: str = "anonymous") -> (List[str], float, int):
    """
    Converts the cube state, runs the Kociemba solver, and returns the solution.
    
    The cube_state_array is a 54-element list/array of colors 
    ordered: [U, L, F, R, B, D] faces (9 stickers each).
    """
    from src.db import log_solve # Import locally to avoid circular dependency
    import time
    
    # --- 1. Conversion to Kociemba string (UFRDLB order) ---
    try:
        # Assuming the input state array follows: 
        # [U0-8, L9-17, F18-26, R27-35, B36-44, D45-53]
        
        # Determine the map by looking at the center piece of each face (indices 4, 13, 22, 31, 40, 49)
        color_to_face = {
            cube_state_array[4]: 'U',   # U Face Center
            cube_state_array[22]: 'F',  # F Face Center
            cube_state_array[31]: 'R',  # R Face Center
            cube_state_array[49]: 'D',  # D Face Center
            cube_state_array[13]: 'L',  # L Face Center
            cube_state_array[40]: 'B',  # B Face Center
        }

        # Order the sticker array as U, F, R, D, L, B (Kociemba standard)
        ordered_stickers = (
            cube_state_array[0:9] +    # U
            cube_state_array[18:27] +  # F
            cube_state_array[27:36] +  # R
            cube_state_array[45:54] +  # D
            cube_state_array[9:18] +   # L
            cube_state_array[36:45]    # B
        )
        
        kociemba_state = "".join(color_to_face[sticker] for sticker in ordered_stickers)
        
    except KeyError:
        raise ValueError("Invalid state: Not all 6 unique center colors are present.")
    except IndexError:
        raise ValueError("Invalid state: Cube state array must contain 54 stickers.")

    # --- 2. Solve Algorithm Execution ---
    start_time = time.time()
    try:
        solution_string = kociemba.solve(kociemba_state)
        solution_steps = solution_string.split()
        
    except ValueError as e:
        raise ValueError(f"Solver Error: Cube state is invalid/impossible. {e}")
    
    solve_time = round(time.time() - start_time, 3)
    moves_count = len(solution_steps)
    
    # --- 3. Database Logging ---
    if user_id != "anonymous":
        log_solve(user_id, cube_state_array, solution_steps, solve_time, moves_count)
        
    return solution_steps, solve_time, moves_count