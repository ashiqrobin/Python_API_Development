from .database import Base
from sqlalchemy import Column

class Post(Base):
    __tablename__ = "post"
    id = Column()