import uvicorn
from fastapi import FastAPI
from api.dependencies import AgentDependency
from pydantic import BaseModel

app = FastAPI()


class InvokeRequest(BaseModel):
    text: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/invoke")
async def invoke(request: InvokeRequest, agent: AgentDependency):
    return await agent.invoke(request.text)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
