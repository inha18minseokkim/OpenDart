from sqlalchemy import Column, TEXT, INT, BIGINT, UniqueConstraint, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class corpCmnAnn(Base):
    __tablename__ = "TB_CORP_CMN_ANN"
    rcept_no = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True,unique=True)
    corp_code = Column(String(length=8 , collation='utf8mb4_general_ci'), nullable=False)
    corp_name = Column(String(length=255 , collation='utf8mb4_general_ci'), nullable=False)
    report_nm = Column(String(length=255 , collation='utf8mb4_general_ci'), nullable=False)
    rcept_dt = Column(String(length=255 , collation='utf8mb4_general_ci'), nullable=True)