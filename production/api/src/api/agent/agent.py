from api.agent.system_prompt import Language, SYSTEM_PROMPT
from typing_extensions import List, TypedDict

from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langgraph.graph import START, StateGraph


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class Agent:
    def __init__(self, llm: BaseChatModel, vector_store: VectorStore, language: Language):
        self.vector_store = vector_store
        self.llm = llm
        self.prompt = PromptTemplate.from_template(SYSTEM_PROMPT[language])
        self.graph = self.create_graph()

    async def retrieve(self, state: State):
        retrieved_docs = await self.vector_store.asimilarity_search(state["question"], k=6)
        return {"context": retrieved_docs}

    async def generate(self, state: State):
        sorted_context = sorted(state["context"], key=lambda x: x.metadata["timestamp"])
        docs_content = "\n\n".join(doc.page_content for doc in sorted_context)
        messages = await self.prompt.ainvoke({"question": state["question"], "context": docs_content})
        response = await self.llm.ainvoke(messages)
        return {"answer": response.content}
    
    def create_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        return graph_builder.compile()
        
    async def invoke(self, prompt: str):
        return await self.graph.ainvoke({"question": prompt})
