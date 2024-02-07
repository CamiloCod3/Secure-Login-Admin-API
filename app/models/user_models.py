from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base 

from ..auth.password_utils import pwd_context


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)  # Adjusted length
    password_hash = Column(String(60))  # Specified length for bcrypt
    name = Column(String(255))  # Matched with SQL definition
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Create an alias for email as username
    @property
    def username(self):
        return self.email

    @username.setter
    def username(self, value):
        self.email = value