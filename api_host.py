import os
import subprocess
import asyncio
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from pydantic import BaseModel
from rembg import remove
import time


class QAslot(BaseModel):
    master_id: str = Form(...)
    file: UploadFile = File(...)

from contextlib import asynccontextmanager
app = FastAPI()


def generate_mesh(master_id, image_id):
    command = [
    "accelerate", "launch",
    "--config_file", "1gpu.yaml",
    "test_mvdiffusion_seq.py",
    "--config", "configs/mvdiffusion-joint-ortho-6views.yaml",
    f"validation_dataset.root_dir=./user_data/{master_id}",
    f"validation_dataset.filepaths=['pic-{image_id}.png']",
    "save_dir=./outputs", "&&",
    "cd", "./instant-nsr-pl", "&&",
    "python", "launch.py",
    "--config", "configs/neuralangelo-ortho-wmask.yaml",
    "--gpu", "0",
    "--train", "dataset.root_dir=../outputs/cropsize-192-cfg1.0/",
    f"dataset.scene=pic-{image_id}"
    ]
    subprocess.run(command, shell=True)

def move_obj_file(master_id, image_id):
    import shutil
    obj_file = []
    root = "instant-nsr-pl/exp/pic-" + image_id
    destination_path = "user_data/" + master_id

    def search_files(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.obj'):
                    obj_file.append(os.path.join(root, file))

            for subdir in dirs:
                search_files(os.path.join(root, subdir))
    search_files(root)

    destination_path = os.path.join(destination_path, image_id + ".obj")
    shutil.move(obj_file[-1], destination_path)

    

@asynccontextmanager
@app.post("/2dto3d")
async def create_upload_file(    
    master_id: str = Form(...),
    image_id: str = Form(...),
    file: UploadFile = File(...)
):
    
    try:
        contents = file.file.read()
        master_id = master_id.decode('utf-8') if isinstance(master_id, bytes) else master_id

        if not os.path.exists("user_data/" + master_id):
            os.makedirs("user_data/" + master_id)
        with open("user_data/" + master_id + "/pic-" + image_id + ".png", 'wb') as f:
            f.write(remove(contents))

    except Exception as e:
        return {"response": "There was an error uploading the file : " +  str(e)}
    finally:
        file.file.close()
    
    try:
        start_time =time.time()
        generate_mesh(master_id, image_id)
        move_obj_file(master_id, image_id)
        end_time = time.time()
        elapsed_time = end_time -start_time
    except Exception as e:
        return {"response": "There was an error generating mesh : " + str(e)}
    return {"response": f"Task completed for user {master_id}. It cost {elapsed_time} sec"}


if __name__ == "__main__":
    uvicorn.run("api_host:app", host='0.0.0.0', port=8083, reload=True)