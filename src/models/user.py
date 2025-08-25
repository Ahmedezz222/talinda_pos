"""
User model for authentication and authorization.
"""
from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, ForeignKey
from database.db_config import Base
import enum
import datetime
from sqlalchemy.orm import relationship
from utils.localization import get_current_local_time

class UserRole(enum.Enum):
    """Enum for user roles in the system."""
    ADMIN = "admin"
    CASHIER = "cashier"
    MANAGER = "manager"

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    full_name = Column(String)
    active = Column(Integer, default=1)  # 1 for active, 0 for inactive

    def __repr__(self):
        """String representation of the user."""
        return f"<User(username={self.username}, role={self.role.value})>"

class ShiftStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    open_time = Column(DateTime, default=get_current_local_time, nullable=False)
    close_time = Column(DateTime, nullable=True)
    opening_amount = Column(Float, nullable=False)
    status = Column(Enum(ShiftStatus), default=ShiftStatus.OPEN, nullable=False)

    user = relationship('User')

    def __repr__(self):
        return f"<Shift(user_id={self.user_id}, open_time={self.open_time}, status={self.status.value})>"
