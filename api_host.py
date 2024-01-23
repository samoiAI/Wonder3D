import os
import subprocess
import asyncio
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from pydantic import BaseModel
from rembg import remove


class QAslot(BaseModel):
    master_id: str = Form(...)
    file: UploadFile = File(...)

from contextlib import asynccontextmanager
app = FastAPI()


def generate_mesh(master_id):
    command = [
    "accelerate", "launch",
    "--config_file", "1gpu.yaml",
    "test_mvdiffusion_seq.py",
    "--config", "configs/mvdiffusion-joint-ortho-6views.yaml",
    "validation_dataset.root_dir=./user_images",
    f"validation_dataset.filepaths=[ 'pic{master_id}.png']",
    "save_dir=./outputs", "&&",
    "cd", "./instant-nsr-pl", "&&",
    "python", "launch.py",
    "--config", "configs/neuralangelo-ortho-wmask.yaml",
    "--gpu", "0",
    "--train", "dataset.root_dir=../outputs/cropsize-192-cfg1.0/",
    f"dataset.scene=pic{master_id}"
    ]
    subprocess.run(command, shell=True)

@asynccontextmanager
@app.post("/2dto3d")
async def create_upload_file(    
    master_id: str = Form(...),
    file: UploadFile = File(...)
):
    
    try:
        contents = file.file.read()
        master_id = master_id.decode('utf-8') if isinstance(master_id, bytes) else master_id
        with open("user_images/pic" + master_id + ".png", 'wb') as f:
            f.write(remove(contents))
    except Exception as e:
        return {"response": "There was an error uploading the file : " +  str(e)}
    finally:
        file.file.close()
    
    try:
        generate_mesh(master_id)
    except Exception as e:
        return {"response": "There was an error generating mesh : " + str(e)}
    return {"response": f"Task completed for user {master_id}"}


if __name__ == "__main__":
    uvicorn.run("api_host:app", host='0.0.0.0', port=8083, reload=True)