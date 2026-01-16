from typing import Any, Dict

import uvicorn
from api.dependencies import AgentDependency
from fastapi import FastAPI
from pydantic import BaseModel

app: FastAPI = FastAPI()


class HealthResponse(BaseModel):
    status: str


class InvokeRequest(BaseModel):
    text: str


class InvokeResponse(BaseModel):
    result: Dict[str, Any]


@app.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/invoke")
async def invoke(request: InvokeRequest, agent: AgentDependency) -> InvokeResponse:
    result = await agent.invoke(request.text)
    return InvokeResponse(result=result)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
