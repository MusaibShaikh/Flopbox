from sqlalchemy import CHAR, Column, DateTime, Float, Integer, JSON, String, TIMESTAMP, create_engine, text
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DbObject():
    def __init__(self):
        self._current_session = None

    def CreateConnection(self,db_connection_string: str):
        if self._current_session == None:
            print("initializing session")
            try:
                mysql_engine = create_engine(db_connection_string)
                session_maker = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
                self._current_session = session_maker()
            except Exception as e:
                logger.error(f"Database connection failed: {e}")

    def GetCurrentSession(self):
        return self._current_session