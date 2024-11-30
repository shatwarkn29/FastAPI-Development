from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas , database , models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import Settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Requirements
SECRET_KEY = Settings.secret_key
ALGORITHM = Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    # Set expiration for the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode token using jose
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Retrieve user_id from payload
        userid: str = payload.get("user_id")
        
        # Validate presence of user_id
        if userid is None:
            raise credentials_exception
        
        # Create token data
        token_data = schemas.TokenData(id=userid)
    except JWTError as e:
        print(f"JWT error: {e}")  # Log actual error
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme) , db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
