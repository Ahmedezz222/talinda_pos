"""
Authentication controller for managing user login and session.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session, safe_commit, get_fresh_session
from models.user import User, Shift, ShiftStatus
import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

class AuthController:
    """Controller for handling authentication operations."""
    
    def __init__(self):
        """Initialize the authentication controller."""
        self.session = get_fresh_session()
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
                logger.info(f"Successful login for user: {username}")
                return True
        except NoResultFound:
            logger.warning(f"Login failed for user: {username} - user not found")
        except Exception as e:
            logger.error(f"Login error for user {username}: {e}")
        return False
    
    def logout(self):
        """Log out the current user."""
        if self.current_user:
            logger.info(f"User logged out: {self.current_user.username}")
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
        try:
            # Close any previous open shift for this user
            open_shift = self.session.query(Shift).filter_by(user_id=user.id, status=ShiftStatus.OPEN).first()
            if open_shift:
                open_shift.status = ShiftStatus.CLOSED
                open_shift.close_time = datetime.datetime.utcnow()
                open_shift.closing_amount = opening_amount  # Fallback: close with new opening amount
                safe_commit(self.session)
            
            shift = Shift(user_id=user.id, opening_amount=opening_amount, status=ShiftStatus.OPEN)
            self.session.add(shift)
            
            if safe_commit(self.session):
                logger.info(f"Shift opened for user {user.username} with amount {opening_amount}")
                return shift
            else:
                logger.error("Failed to commit shift opening")
                return None
        except Exception as e:
            logger.error(f"Error opening shift: {e}")
            self.session.rollback()
            return None

    def get_open_shift(self, user):
        """Get the current open shift for the user, if any."""
        try:
            return self.session.query(Shift).filter_by(user_id=user.id, status=ShiftStatus.OPEN).first()
        except Exception as e:
            logger.error(f"Error getting open shift for user {user.username}: {e}")
            return None


    
    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")
