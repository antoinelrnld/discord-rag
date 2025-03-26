import os
from langchain_openai import ChatOpenAI
from inference.prompting import get_prompt_template
from utils.vector_store import get_vector_store
from langgraph.graph import START, StateGraph
from inference import State


class Inferencer:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.prompt = get_prompt_template()
        self.graph = self.create_graph()

    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(state["question"], k=6)
        return {"context": retrieved_docs}

    def generate(self, state: State):
        sorted_context = sorted(state["context"], key=lambda x: x.metadata["timestamp"])
        docs_content = "\n\n".join(doc.page_content for doc in sorted_context)
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}
    
    def create_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        return graph_builder.compile()
    
    def infer(self, prompt: str):
        return self.graph.invoke({"question": prompt})