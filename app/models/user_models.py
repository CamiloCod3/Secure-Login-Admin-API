from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base
from ..auth.password_utils import pwd_context

class UserModel(Base):
    """
    Represents a user within the application, storing authentication and profile information.
    """
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(255), unique=True, index=True)
    password_hash: str = Column(String(60))  # Bcrypt hash length
    name: str = Column(String(255))
    is_admin: bool = Column(Boolean, default=False)

    def verify_password(self, password: str) -> bool:
        """
        Verify a password against the stored password hash.

        :param password: Plain text password to verify.
        :return: True if the password is correct, False otherwise.
        """
        return pwd_context.verify(password, self.password_hash)

    @property
    def username(self) -> str:
        """Alias for email as username."""
        return self.email

    @username.setter
    def username(self, value: str) -> None:
        self.email = value