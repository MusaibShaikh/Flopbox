from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import hashlib

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    Id = Column(String(36), primary_key=True, server_default=text("(uuid())"))
    Username = Column(String(256), unique=True, nullable=False)
    Email = Column(String(256), unique=True, nullable=False)
    Salt = Column(String(32))
    PasswordHash = Column(String(256))
    Files = relationship("File", back_populates="Owner")

class File(Base):
    __tablename__ = 'Files'
    Id = Column(String(36), primary_key=True, server_default=text("(uuid())"))
    Filename = Column(String(256), index=True, nullable=False)
    FilePath = Column(String(512), nullable=False)
    FileType = Column(String(50), nullable=False)
    MD5Hash = Column(String(32), nullable=False)  
    UploadDate = Column(DateTime)
    UserId = Column(String(36), ForeignKey('Users.Id'))
    Owner = relationship("User", back_populates="Files")
    Comment = Column(Text) 

