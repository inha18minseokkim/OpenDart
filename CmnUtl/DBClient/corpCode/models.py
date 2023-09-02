from sqlalchemy import Column, TEXT, INT, BIGINT, UniqueConstraint, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class corpInfo(Base):
    __tablename__ = "TB_CORP_CODE"
    idx = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    corp_code = Column(String(length=8 , collation='utf8mb4_general_ci'),nullable=False)
    corp_name = Column(String(length=255 , collation='utf8mb4_general_ci'), nullable=False)
    stock_code = Column(String(length=6 , collation='utf8mb4_general_ci'), nullable=False)
    modify_date = Column(String(length=255 , collation='utf8mb4_general_ci'), nullable=True)