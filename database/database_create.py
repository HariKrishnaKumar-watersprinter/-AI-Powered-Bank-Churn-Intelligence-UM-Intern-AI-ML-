import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, and_,or_,update,delete
from sqlalchemy.orm import declarative_base
import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
load_dotenv()

DATABASE_URL = st.secrets["url"]
engine = sa.create_engine(DATABASE_URL, pool_pre_ping=True)
st.info("✅ Connected to Supabase PostgreSQL")
#else:
   # model_path = os.path.join(os.getcwd(), "database", "bank_data.db")
   # engine = sa.create_engine(f'sqlite:///{model_path}',connect_args={"check_same_thread": False})

#if "sqlite" in str(engine.url):
  #  with engine.connect() as conn:
     #   conn.execute(sa.text("PRAGMA journal_mode=WAL;"))
     #   conn.commit()
Base = declarative_base()

class BankCustomer(Base):
    __tablename__ = 'bank_customers'
    id = sa.Column(sa.Integer, primary_key=True)
    CustomerId = sa.Column(sa.Integer, nullable=False,unique=True)
    CreditScore = sa.Column(sa.Integer, nullable=False)
    Geography = sa.Column(sa.String, nullable=False)
    Gender = sa.Column(sa.String, nullable=False)
    Age = sa.Column(sa.Integer, nullable=False)
    Tenure = sa.Column(sa.Integer, nullable=False)
    Balance = sa.Column(sa.Float, nullable=False)
    NumOfProducts = sa.Column(sa.Integer, nullable=False)
    HasCrCard = sa.Column(sa.Integer, nullable=False)
    IsActiveMember = sa.Column(sa.Integer, nullable=False)
    EstimatedSalary = sa.Column(sa.Float, nullable=False)
    Exited=sa.Column(sa.Integer,nullable=False)
    


Base.metadata.create_all(bind=engine)
st.success("✅ Table checked/created successfully")
SessionLocal = sessionmaker(bind=engine)

def save_data(CustomerId,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited):
    session = SessionLocal()
    try:
        # Check if the customer already exists to prevent UNIQUE constraint error
        customer = session.query(BankCustomer).filter_by(CustomerId=CustomerId).first()
        
        if customer:
            # Update existing record (Upsert logic)
            customer.CreditScore = CreditScore
            customer.Geography = Geography
            customer.Gender = Gender
            customer.Age = Age
            customer.Tenure = Tenure
            customer.Balance = Balance
            customer.NumOfProducts = NumOfProducts
            customer.HasCrCard = HasCrCard
            customer.IsActiveMember = IsActiveMember
            customer.EstimatedSalary = EstimatedSalary
            customer.Exited = Exited
        else:
            # Insert new record
            new_customer = BankCustomer(
                CustomerId=CustomerId, CreditScore=CreditScore, Geography=Geography, 
                Gender=Gender, Age=Age, Tenure=Tenure, Balance=Balance, 
                NumOfProducts=NumOfProducts, HasCrCard=HasCrCard, 
                IsActiveMember=IsActiveMember, EstimatedSalary=EstimatedSalary ,Exited = Exited
            )
            session.add(new_customer)
        
        session.commit()
    except Exception as e:
        session.rollback()  # This fixes the PendingRollbackError for future attempts
        raise e
    finally:
        session.close()

def get_all_data():
    session = SessionLocal()
    try:
        return session.query(BankCustomer).all()
    finally:
        session.close()
