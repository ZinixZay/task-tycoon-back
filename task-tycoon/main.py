from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def get_home():
    return {"data": "test"}