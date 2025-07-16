# app/models/__init__.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("Defina a variável DATABASE_URL no arquivo .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria o declarative base
Base = declarative_base()

# **IMPORTA AQUI OS MODELOS PARA REGISTRÁ-LOS NO Base.metadata**
from app.models.car import Car
# Se tiver outros modelos, importe todos aqui!
