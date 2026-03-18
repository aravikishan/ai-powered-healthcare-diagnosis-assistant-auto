from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import uvicorn

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

# Models
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    medical_history = Column(String)

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    symptoms = Column(String)
    results = Column(String)

# Pydantic models
class PatientBase(BaseModel):
    name: str
    age: int
    medical_history: str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True

class DiagnosisCreate(BaseModel):
    patient_id: int
    symptoms: str

class DiagnosisResponse(BaseModel):
    id: int
    patient_id: int
    symptoms: str
    results: str

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/patient/{id}", response_class=HTMLResponse)
async def patient_details_page(request: Request, id: int):
    return templates.TemplateResponse("patient_details.html", {"request": request, "id": id})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/api/patients", response_model=List[PatientResponse])
async def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients

@app.post("/api/diagnosis", response_model=DiagnosisResponse)
async def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    # Mock AI-driven diagnosis logic
    results = "Possible flu, common cold"
    db_diagnosis = Diagnosis(**diagnosis.dict(), results=results)
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis

@app.get("/api/patient/{id}", response_model=PatientResponse)
async def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/api/login")
async def login(username: str, password: str):
    # Mock authentication logic
    if username == "admin" and password == "password":
        return {"access_token": "fake-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Initialize database and seed data
init_db()

# Seed data
with SessionLocal() as db:
    if not db.query(Patient).first():
        db.add_all([
            Patient(name="John Doe", age=30, medical_history="No significant history"),
            Patient(name="Jane Smith", age=25, medical_history="Asthma")
        ])
        db.commit()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
