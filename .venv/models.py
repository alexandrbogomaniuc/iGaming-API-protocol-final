from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime  # Import DECIMAL
from sqlalchemy.orm import relationship
import logging
from database import Base

class Player(Base):
    __tablename__ = "players"

    userId = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), unique=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    language_code = Column(String(10), nullable=True, default='en')  # Default to 'en'    registration_date = Column(DateTime)
    status = Column(String(20))
    date_of_birth = Column(DateTime, nullable=True)
    phone_number = Column(String(20), nullable=True)
    country = Column(String(50), nullable=True)
    # models.py
    ext_user_id = Column(String(255), unique=True, nullable=True)

    wallets = relationship("Wallet", back_populates="player")

 # Log successful model load
    logging.info("Player model loaded successfully")

class Wallet(Base):
    __tablename__ = "wallets"

    wallet_id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("players.userId"))
    wallet_type = Column(String(10))
    balance = Column(DECIMAL(15, 2), default=0.00)
    currency_code = Column(String(3), default='USD')
    # ... other columns ...
    player = relationship("Player", back_populates="wallets")

    logging.info("Wallet model loaded successfully")