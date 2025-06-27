"""
Chat Chain for Alexa - Member Support Agent
Builds LangChain's ConversationalRetrievalChain with memory and retriever
"""

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from document_pipeline import DocumentPipeline
from prompt_manager import get_system_prompt

class ChatChain:
    def __init__(self):
        """Initialize the chat chain with retriever, memory, and LLM"""
        # Initialize document pipeline and get retriever
        self.document_pipeline = DocumentPipeline()
        self.retriever = self.document_pipeline.get_retriever()
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Get system prompt
        system_prompt = get_system_prompt()

        # Create custom prompt template with our system prompt
        custom_prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=f"{system_prompt}\n\nContext: {{context}}\n\nChat History: {{chat_history}}\n\nQuestion: {{question}}\n\nAnswer:"
        )

        # Build the conversational retrieval chain with custom prompt
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": custom_prompt},
            verbose=False
        )

    def get_response(self, message: str) -> str:
        """Get response from the chat chain"""
        try:
            response = self.chain.invoke({"question": message})
            return response["answer"]
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support." 
        
    