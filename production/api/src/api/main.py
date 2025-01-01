import uvicorn
from fastapi import FastAPI, Form
from inference import Inferencer

app = FastAPI()
inferencer = Inferencer()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/infer")
async def infer(text: str = Form()):
    return inferencer.infer(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)