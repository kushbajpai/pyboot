from fastapi import FastAPI
import os
import shutil
import zipfile

app = FastAPI()

TEMPLATES = {
    "core": "from pyboot.core import PyBootApp\n\napp = PyBootApp()\n\n@app.route('/')\ndef home():\n    return {'message': 'Hello, PyBoot!'}\n\nif __name__ == '__main__':\n    app.run()",
    "db": "from sqlalchemy import create_engine\nengine = create_engine('sqlite:///app.db')\nprint('Database initialized')",
    "mq": "import pika\nprint('RabbitMQ setup')",
    "ml": "import tensorflow as tf\nprint('AI/ML module ready')"
}

def create_project(name, dependencies):
    os.makedirs(name, exist_ok=True)
    with open(f"{name}/app.py", "w") as f:
        f.write(TEMPLATES["core"])
    
    if "db" in dependencies:
        with open(f"{name}/db.py", "w") as f:
            f.write(TEMPLATES["db"])

    if "mq" in dependencies:
        with open(f"{name}/mq.py", "w") as f:
            f.write(TEMPLATES["mq"])
    
    if "ml" in dependencies:
        with open(f"{name}/ml.py", "w") as f:
            f.write(TEMPLATES["ml"])
    
    # Create a ZIP file
    zip_filename = f"{name}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for root, _, files in os.walk(name):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), name))
    
    return zip_filename

@app.get("/generate")
def generate_project(name: str, dependencies: str = ""):
    deps = dependencies.split(",") if dependencies else []
    zip_file = create_project(name, deps)
    return {"message": f"Project {name} generated!", "zip": zip_file}
