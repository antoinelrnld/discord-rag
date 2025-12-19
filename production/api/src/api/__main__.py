import uvicorn
from fastapi import FastAPI, Form
from api.inference import Inferencer

app = FastAPI()
inferencer = Inferencer()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/infer")
async def infer(text: str = Form()):
    return inferencer.infer(text)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()