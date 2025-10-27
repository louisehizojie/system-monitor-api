import jwt
import config
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# --- Configuration ---
SECRET_KEY = config.jwt_info.secret_key
ALGORITHM = config.jwt_info.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.jwt_info.token_expiry

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Defines the token URL for the client to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

# --- Password Hashing Functions ---

def verify_password(plain_password, hashed_password):
    """Checks if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Generation Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token using PyJWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiry time (exp) to the token payload
    to_encode.update({"exp": expire})
    
    # Use jwt.encode() from PyJWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- JWT Decoding/Validation (Security Dependency) ---

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodes and validates the JWT using PyJWT. 
    Raises an HTTPException if the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Use jwt.decode() from PyJWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the username/subject from the payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception
        
    # Return the user identifier
    return {"username": username}

# --- Mock Example Usage ---
def get_password_hash(password):
    return pwd_context.hash(password)

MOCK_USERS = {
    "testuser": {
        "username": "testuser",
        "hashed_password": get_password_hash("password123"),
    }
}

def authenticate_user(username: str, password: str):
    """Authenticates the user against the mock database."""
    user = MOCK_USERS.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user
