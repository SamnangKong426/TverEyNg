from fastapi import APIRouter, HTTPException

from config.db import supabase
from models import UserSignup

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(user: UserSignup):
    try:
        response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        if response.user is None:
            raise HTTPException(
                status_code=400, detail="Signup failed: No user returned"
            )

        return {"message": "User created!", "user_id": response.user.id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signup error: {str(e)}")


@router.post("/login")
async def login(user: UserSignup):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        if not response.session or not response.user:
            raise HTTPException(status_code=401, detail="Invalid login credentials")

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": response.user.email,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")
