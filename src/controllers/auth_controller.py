"""
Authentication controller for managing user login and session.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session
from models.user import User, Shift, ShiftStatus
import datetime

class AuthController:
    """Controller for handling authentication operations."""
    
    def __init__(self):
        """Initialize the authentication controller."""
        self.session = Session()
        self.current_user = None
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a user with username and password.
        
        Args:
            username: The username to authenticate
            password: The password to verify
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            user = self.session.query(User).filter_by(username=username, active=1).one()
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                self.current_user = user
                return True
        except NoResultFound:
            pass
        return False
    
    def logout(self):
        """Log out the current user."""
        self.current_user = None
    
    def get_current_user(self) -> User:
        """
        Get the currently logged-in user.
        
        Returns:
            User: The current user object or None if no user is logged in
        """
        return self.current_user

    def open_shift(self, user, opening_amount):
        """Open a new shift for the given user with the opening amount."""
        # Close any previous open shift for this user
        open_shift = self.session.query(Shift).filter_by(user_id=user.id, status=ShiftStatus.OPEN).first()
        if open_shift:
            open_shift.status = ShiftStatus.CLOSED
            open_shift.close_time = datetime.datetime.utcnow()
            open_shift.closing_amount = opening_amount  # Fallback: close with new opening amount
            self.session.commit()
        shift = Shift(user_id=user.id, opening_amount=opening_amount, status=ShiftStatus.OPEN)
        self.session.add(shift)
        self.session.commit()
        return shift

    def get_open_shift(self, user):
        """Get the current open shift for the user, if any."""
        return self.session.query(Shift).filter_by(user_id=user.id, status=ShiftStatus.OPEN).first()

    def close_shift(self, user, closing_amount):
        """Close the current open shift for the user with the closing amount."""
        shift = self.get_open_shift(user)
        if shift:
            shift.status = ShiftStatus.CLOSED
            shift.close_time = datetime.datetime.utcnow()
            shift.closing_amount = closing_amount
            self.session.commit()
            return shift
        return None
