from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

o2auth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(payload: dict):
    toEncode = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

    return encodedJWT

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(o2auth_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW_Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user
