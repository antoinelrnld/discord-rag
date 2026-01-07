import uvicorn
from fastapi import FastAPI, Form
from api.agent import Agent


app = FastAPI()
agent = Agent()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/invoke")
async def invoke(text: str = Form()):
    return await agent.invoke(text)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
