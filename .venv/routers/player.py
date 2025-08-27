from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from database import get_db
from models import Player, Wallet

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register-player/")
async def register_player(player_data: dict, db: Session = Depends(get_db)):
    try:
        logger.info('Register player function is running. Database session has been established.')

        # 1. Create a new player
        logger.info(
            f"Creating new player with user_name: {player_data['user_name']}, email: {player_data['email']}, and ext_user_id: {player_data['ext_user_id']}")

        new_player = Player(
            ext_user_id=player_data["ext_user_id"],
            first_name=player_data["user_name"],
            email=player_data["email"]
        )

        db.add(new_player)
        db.commit()
        db.refresh(new_player)  # Get the generated userId

        logger.info(f"Player created successfully with userId: {new_player.userId}")

        # 2. Create the associated wallets
        logger.info(f"Creating wallets for player userId: {new_player.userId}")
        vnd_wallet = Wallet(userId=new_player.userId, wallet_type="MAIN", currency_code="VND")
        usd_wallet = Wallet(userId=new_player.userId, wallet_type="MAIN", currency_code="USD")
        db.add_all([vnd_wallet, usd_wallet])
        db.commit()

        logger.info("Wallets created and committed successfully.")

        return {"status": "OK", "player_id": new_player.userId}

    except Exception as e:
        logger.error(f"An error occurred during player registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/test_registration")
async def test_registration():
    try:
        logger.info("Test registration endpoint reached")
        return {"message": "Registration test triggered"}
    except Exception as e:
        logger.error(f"An error occurred in test_registration: {e}")

