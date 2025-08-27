from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
import logging

from database import get_db
from models import Player, Wallet

router = APIRouter()
logger = logging.getLogger(__name__)


class PlayerCreate(BaseModel):
    """Schema for creating a player via FastAPI.  We only require a nickname, email and ext_user_id.
    The password for the Wix member should never be sent here.  """

    user_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    ext_user_id: constr(strip_whitespace=True, min_length=1)


@router.post("/register-player/", response_model=dict)
async def register_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    """
    Idempotent player registration endpoint.

    Checks whether a player already exists with the provided ext_user_id or email.
    If found, returns the existing player_id.  Otherwise, creates a new player and associated wallets.
    Note: the password must never be sent to this endpoint; Wix handles authentication separately.
    """
    try:
        logger.info("Register player function invoked.")

        # Normalize email to lowercase for uniqueness
        email = player_data.email.lower()
        nickname = player_data.user_name.strip()
        ext_user_id = player_data.ext_user_id.strip()

        # Check for existing player by external user ID or email
        existing_player = db.query(Player).filter(
            (Player.ext_user_id == ext_user_id) | (Player.email == email)
        ).first()
        if existing_player:
            logger.info(
                f"Found existing player for ext_user_id/email; returning player_id {existing_player.userId}"
            )
            return {"status": "OK", "player_id": existing_player.userId}

        # Create a new player record
        new_player = Player(
            ext_user_id=ext_user_id,
            first_name=nickname,
            email=email
        )
        db.add(new_player)
        db.commit()
        db.refresh(new_player)
        logger.info(f"Player created successfully with userId: {new_player.userId}")

        # Create wallets for VND and USD under one transaction
        vnd_wallet = Wallet(userId=new_player.userId, wallet_type="MAIN", currency_code="VND")
        usd_wallet = Wallet(userId=new_player.userId, wallet_type="MAIN", currency_code="USD")
        db.add_all([vnd_wallet, usd_wallet])
        db.commit()
        logger.info("Wallets created and committed successfully.")

        return {"status": "OK", "player_id": new_player.userId}
    except Exception as e:
        logger.exception("An unexpected error occurred during player registration")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/test_registration")
async def test_registration():
    try:
        logger.info("Test registration endpoint reached")
        return {"message": "Registration test triggered"}
    except Exception as e:
        logger.error(f"An error occurred in test_registration: {e}")

