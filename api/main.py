from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.logic import solve_cube

# --- Pydantic Schema for Input Validation ---
class CubeInput(BaseModel):
    state: List[str] # The 54-element cube state array
    user_id: str = "anonymous"

# --- FastAPI App Initialization ---
app = FastAPI(title="CubeLogic Solver API")

# --- API Routes ---

@app.get("/")
async def root():
    return {"message": "CubeLogic Solver API is running."}

@app.post("/solve")
async def get_solution(input_data: CubeInput):
    """
    Accepts the cube state and returns the optimal solution steps.
    """
    if len(input_data.state) != 54:
        raise HTTPException(status_code=400, detail="Cube state must contain exactly 54 stickers.")

    try:
        solution_steps, solve_time, moves_count = solve_cube(
            input_data.state, 
            input_data.user_id
        )
        
        return {
            "solution": solution_steps,
            "time": solve_time,
            "moves": moves_count,
            "message": f"Solved in {moves_count} moves and {solve_time} seconds using Kociemba."
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # General catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# To run the backend: uvicorn API.main:app --reload