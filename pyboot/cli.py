import os
import subprocess
import webbrowser
import time
import shutil

PYPROJECT_TEMPLATE = """\
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A PySpring-generated Python application"
authors = [{{name = "Your Name", email = "your.email@example.com"}}]
dependencies = [
    "fastapi",
    "sqlalchemy",
    "pydantic",
    "requests",
    "gunicorn",
    "tensorflow",  # AI/ML support
    "torch",       # AI/ML support (correct package name)
    "uvicorn"      # ASGI server for FastAPI
]

[tool.setuptools]
packages = ["src.{project_name}"]

[project.scripts]
pyspring-cli = "pyspring.cli:main"
"""

MAIN_PY_TEMPLATE = """\
from fastapi import FastAPI
from {project_name}.routes import init_routes

app = FastAPI()
init_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

ROUTES_PY_TEMPLATE = """\
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to PySpring!"}

def init_routes(app):
    app.include_router(router)
"""

CONFIG_PY_TEMPLATE = """\
import os

class Config:
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
"""

DATABASE_PY_TEMPLATE = """\
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from {project_name}.config import Config

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""

README_TEMPLATE = """\
# {project_name}

This is a PySpring-generated Python project.
"""

GITIGNORE_TEMPLATE = """\
__pycache__/
.env
*.pyc
instance/
"""

def create_project_structure(project_name):
    """Creates a structured project with all necessary files."""
    project_path = os.path.join(os.getcwd(), project_name)
    
    if os.path.exists(project_path):
        response = input(f"Error: Directory '{project_name}' already exists. Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
        else:
            shutil.rmtree(project_path)
    
    # Create base directories
    os.makedirs(os.path.join(project_path, "src", project_name, "services"))
    os.makedirs(os.path.join(project_path, "src", project_name, "models"))
    os.makedirs(os.path.join(project_path, "src", project_name, "utils"))
    os.makedirs(os.path.join(project_path, "tests"))

    # Create core project files
    with open(os.path.join(project_path, "src", project_name, "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(project_path, "src", project_name, "main.py"), "w") as f:
        f.write(MAIN_PY_TEMPLATE.format(project_name=project_name))
    with open(os.path.join(project_path, "src", project_name, "routes.py"), "w") as f:
        f.write(ROUTES_PY_TEMPLATE)
    with open(os.path.join(project_path, "src", project_name, "config.py"), "w") as f:
        f.write(CONFIG_PY_TEMPLATE)
    with open(os.path.join(project_path, "src", project_name, "database.py"), "w") as f:
        f.write(DATABASE_PY_TEMPLATE.format(project_name=project_name))

    # Create project metadata files
    with open(os.path.join(project_path, "pyproject.toml"), "w") as f:
        f.write(PYPROJECT_TEMPLATE.format(project_name=project_name))
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(README_TEMPLATE.format(project_name=project_name))
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.write(GITIGNORE_TEMPLATE)

    print(f"✅ PySpring project '{project_name}' created successfully!")
    
    # Navigate to project directory
    os.chdir(project_path)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run(["pip", "install", "."])

    # Run the app in a new process
    print("🚀 Launching the application...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([os.path.join(project_path, "src"), env.get("PYTHONPATH", "")])
    process = subprocess.Popen(["uvicorn", f"src.{project_name}.main:app", "--host", "127.0.0.1", "--port", "8000"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give the server some time to start
    time.sleep(3)

    # Open in browser
    webbrowser.open("http://127.0.0.1:8000")

def main():
    import sys
    if len(sys.argv) < 3 or sys.argv[1] != "init":
        print("Usage: pyspring-cli init <project_name>")
    else:
        create_project_structure(sys.argv[2])

if __name__ == "__main__":
    main()