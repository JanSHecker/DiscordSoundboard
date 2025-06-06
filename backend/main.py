from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from db import SessionLocal, engine
from models import Base, Sound
import shutil, os
import bot
import models

UPLOAD_DIR = "sounds"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this securely later
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/upload")
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    sound = Sound(filename=file.filename)
    db.add(sound)
    await db.commit()
    return {"filename": file.filename}

@app.get("/sounds")
async def get_sounds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(models.Sound.__table__.select())
    return [row.filename for row in result]
    
@app.post("/play")
async def play(name: str = Form(...)):
    return bot.play(name)
