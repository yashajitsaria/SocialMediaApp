from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    accessToken = oauth2.create_access_token(payload={"user_id": user.id})
    return {"access_token": accessToken, "token_type": "bearer"}