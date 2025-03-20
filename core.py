from fastapi import FastAPI

class PyBootApp:
    def __init__(self):
        self.app = FastAPI()

    def route(self, path):
        def wrapper(func):
            self.app.get(path)(func)
            return func
        return wrapper

    def run(self, host="0.0.0.0", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
