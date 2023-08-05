from fastapi import Depends
from sqlalchemy.orm import Session

from db import create_session


class BaseRepository:

    def __init__(self, session: Session = Depends(create_session)):
        self.session: Session = session
