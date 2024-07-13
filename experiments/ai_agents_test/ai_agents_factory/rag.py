import os

from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import (DirectoryLoader,
                                                  UnstructuredMarkdownLoader)
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings


class DocumentManager:
    def __init__(self, directory_path, glob_pattern="**/*.md"):
        self.directory_path = directory_path
        self.glob_pattern = glob_pattern
        self.documents = []
        self.all_sections = []
    
    def load_documents(self):
        loader = DirectoryLoader(self.directory_path, glob=self.glob_pattern, show_progress=True, loader_cls=UnstructuredMarkdownLoader)
        self.documents = loader.load()

    def split_documents(self):
        headers_to_split_on = [("\n#", "Header 1"), ("\n##", "Header 2"), ("\n###", "Header 3"), ("\n####", "Header 4")]
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        for doc in self.documents:
            sections = text_splitter.split_text(doc.page_content)
            self.all_sections.extend(sections)

            print(f"Split {doc.metadata['source']} into {len(sections)} sections")

       


class EmbeddingManager:
    def __init__(self, all_sections, persist_directory='db'):
        self.all_sections = all_sections
        self.persist_directory = persist_directory
        self.vectordb = None
        
    def create_and_persist_embeddings(self):
        embedding = OpenAIEmbeddings() #model='text-embedding-3-small')
        self.vectordb = Chroma.from_documents(documents=self.all_sections, embedding=embedding, persist_directory=self.persist_directory)
        self.vectordb.persist()


class ConversationalRetrievalAgent:
    def __init__(self, vectordb, temperature=0.5):
        self.vectordb = vectordb
        self.llm = OpenAI(temperature=temperature)
        self.chat_history = []
    
    def get_chat_history(self, inputs):
        res = []
        for human, ai in inputs:
            res.append(f"Human:{human}\nAI:{ai}")
        return "\n".join(res)
    
    def setup_bot(self):
        retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})
        self.bot = ConversationalRetrievalChain.from_llm(
            self.llm, retriever, return_source_documents=True, get_chat_history=self.get_chat_history
        )

    def generate_prompt(self, question):
        if not self.chat_history:
            prompt = f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. \nQuestion: {question}\nContext: \nAnswer:"
        else:
            context_entries = [f"Question: {q}\nAnswer: {a}" for q, a in self.chat_history[-3:]]
            context = "\n\n".join(context_entries)
            prompt = f"Using the context provided by recent conversations, answer the new question in a concise and informative. Limit your answer to a maximum of three sentences.\n\nContext of recent conversations:\n{context}\n\nNew question: {question}\n\Answer:"
        
        return prompt
    
    def ask_question(self, query):
        prompt = self.generate_prompt(query)

        result = self.bot.invoke({"question": prompt, "chat_history": self.chat_history})

        self.chat_history.append((query, result["answer"]))

        return result["answer"]
    


def main():
    # Initialising and loading documents
    doc_manager = DocumentManager('./marckdown_folder')
    doc_manager.load_documents()
    doc_manager.split_documents()

    # Creation and persistence of embeddings
    embed_manager = EmbeddingManager(doc_manager.all_sections)
    embed_manager.create_and_persist_embeddings()

    # Setup and use of conversation bots
    bot = ConversationalRetrievalAgent(embed_manager.vectordb)
    bot.setup_bot()
    print(bot.ask_question("Question one"))
    print(bot.ask_question("Question two"))
    print(bot.ask_question("Question three"))

if __name__ == "__main__":
    main()