from passlib.context import CryptContext

# Create a CryptContext object for handling password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify a password against a hash
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)