from typing import Any, Dict, List, TypedDict

from api.agent.system_prompt import SYSTEM_PROMPT, Language
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages.ai import AIMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class Agent:
    def __init__(
        self, llm: BaseChatModel, vector_store: VectorStore, language: Language
    ) -> None:
        self.vector_store: VectorStore = vector_store
        self.llm: BaseChatModel = llm
        self.prompt: PromptTemplate = PromptTemplate.from_template(
            SYSTEM_PROMPT[language]
        )
        self.graph: CompiledStateGraph = self.create_graph()

    async def retrieve(self, state: State) -> Dict[str, List[Document]]:
        retrieved_docs: List[Document] = await self.vector_store.asimilarity_search(
            state["question"], k=6
        )
        return {"context": retrieved_docs}

    async def generate(self, state: State) -> Dict[str, str]:
        sorted_context: List[Document] = sorted(
            state["context"], key=lambda x: x.metadata["timestamp"]
        )
        docs_content: str = "\n\n".join(doc.page_content for doc in sorted_context)
        messages: PromptValue = await self.prompt.ainvoke(
            {"question": state["question"], "context": docs_content}
        )
        response: AIMessage = await self.llm.ainvoke(messages)
        return {"answer": response.content}

    def create_graph(self) -> CompiledStateGraph:
        graph_builder: StateGraph = StateGraph(State).add_sequence(
            [self.retrieve, self.generate]
        )
        graph_builder.add_edge(START, "retrieve")
        return graph_builder.compile()

    async def invoke(self, prompt: str) -> Dict[str, Any]:
        return await self.graph.ainvoke({"question": prompt})
