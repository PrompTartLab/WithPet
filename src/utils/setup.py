from typing import Optional

from sqlite3 import Connection

from pinecone import Pinecone

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from omegaconf import DictConfig
from hydra.utils import instantiate

from .data_utils import load_csv_to_sqlite

from ..modules.context import Context


class SetUp:
    def __init__(
        self,
        config: DictConfig,
    ) -> None:
        self.config = config

    def get_llm(self) -> ChatOpenAI:
        llm: ChatOpenAI = instantiate(
            self.config.llms.llm,
        )
        return llm

    def get_llm_stream(
        self,
        callbacks: BaseCallbackHandler,
    ) -> ChatOpenAI:
        llm_stream: ChatOpenAI = instantiate(
            self.config.llms.llm_stream,
            callbacks=[callbacks],
        )
        return llm_stream

    def get_connection(self) -> Connection:
        data_path = f"{self.config.data_path}/{self.config.data_file_name}.csv"
        data_file_name = self.config.data_file_name
        conn = load_csv_to_sqlite({data_path: data_file_name})
        return conn

    def get_vs_example(
        self,
        embeddings: OpenAIEmbeddings,
    ) -> FAISS:
        vs_example = FAISS.load_local(
            folder_path=self.config.vector_store_example,
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )
        return vs_example

    def get_vs_data(
        self,
        embeddings: OpenAIEmbeddings,
    ) -> PineconeVectorStore:
        pc = Pinecone(api_key=self.config.pinecone_api_key)
        index = pc.Index(name=self.config.pinecone_index_name)
        vs_data = PineconeVectorStore(index=index, embedding=embeddings)
        return vs_data

    def get_context(
        self,
        llm: ChatOpenAI,
        llm_stream: ChatOpenAI,
        conn: Connection,
        vs_example: FAISS,
        vs_data: Optional[FAISS],
    ) -> Context:
        context = Context(
            llm=llm,
            llm_stream=llm_stream,
            conn=conn,
            vs_example=vs_example,
            vs_data=vs_data,
        )
        return context

    def get_prompt_template(
        self,
        prompt_type: str,
    ) -> PromptTemplate:
        prompt_template: PromptTemplate = instantiate(
            self.config.prompt_templates[prompt_type],
        )
        return prompt_template

    def get_source_columns(self) -> PromptTemplate:
        source_columns: PromptTemplate = instantiate(
            self.config.source_columns,
        )
        return source_columns
