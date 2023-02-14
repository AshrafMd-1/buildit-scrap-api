from sqlalchemy import Column, Integer, String, Boolean

from buildit_api.db.database import Base


class User(Base):
    __tablename__ = "user_login"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True, index=True )
    user = Column(String)
    token = Column(String)
    logged_in = Column(Boolean, default=False)
    # s_time = Column(String)
    # e_time = Column(String)
    branch = Column(String)
    user_id = Column(String,unique=True, index=True)
