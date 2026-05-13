from typing import Annotated

from sqlmodel import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_session


SessionDep = Annotated[Session, Depends(get_session)]

FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
