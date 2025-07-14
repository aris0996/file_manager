import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import shutil

BASE_DIR = "/data"  # folder root yang di-manage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/list")
def list_files(path: str = ""):
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="Path not found")
    items = []
    for entry in os.scandir(abs_path):
        items.append({
            "name": entry.name,
            "is_dir": entry.is_dir(),
            "size": entry.stat().st_size if not entry.is_dir() else None
        })
    return {"items": items}

@app.post("/upload")
def upload_file(path: str = Form(""), file: UploadFile = File(...)):
    abs_path = os.path.join(BASE_DIR, path, file.filename)
    with open(abs_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"success": True}

@app.get("/download")
def download_file(path: str):
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(abs_path, filename=os.path.basename(abs_path))

@app.post("/delete")
def delete_file(path: str = Form(...)):
    abs_path = os.path.join(BASE_DIR, path)
    if os.path.isdir(abs_path):
        shutil.rmtree(abs_path)
    elif os.path.isfile(abs_path):
        os.remove(abs_path)
    else:
        raise HTTPException(status_code=404, detail="File/folder not found")
    return {"success": True}

@app.post("/rename")
def rename_file(path: str = Form(...), new_name: str = Form(...)):
    abs_path = os.path.join(BASE_DIR, path)
    new_path = os.path.join(os.path.dirname(abs_path), new_name)
    os.rename(abs_path, new_path)
    return {"success": True}

@app.get("/preview")
def preview_file(path: str):
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(4096)
    return JSONResponse({"content": content}) 