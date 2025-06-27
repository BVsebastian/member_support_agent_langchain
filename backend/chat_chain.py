"""
Chat Chain for Alexa - Member Support Agent
Builds LangChain's ConversationalRetrievalChain with memory and retriever
"""

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from document_pipeline import DocumentPipeline
from prompt_manager import get_system_prompt
from tools import send_notification, record_user_details, log_unknown_question

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

        # Create LangChain tools
        self.tools = [
            Tool(
                name="send_notification",
                description="Send notification for escalation. Use when user needs escalation for loan, card, account, fraud, or refinance issues. Parameters: original_request (str), contact_info (dict with name, email, phone), issue_type (str: loan/card/account/fraud/refinance)",
                func=send_notification
            ),
            Tool(
                name="record_user_details", 
                description="Record user contact details for follow-up. Use when user provides any contact information. Parameters: user_details (dict with name, email, phone, notes)",
                func=record_user_details
            ),
            Tool(
                name="log_unknown_question",
                description="Log questions that cannot be answered from knowledge base. Use when you cannot find information to answer user's question. Parameters: question (str), context (dict, optional)",
                func=log_unknown_question
            )
        ]

        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Get system prompt
        system_prompt = get_system_prompt()

        # Create custom prompt template with our system prompt
        custom_prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=f"{system_prompt}\n\nContext: {{context}}\n\nChat History: {{chat_history}}\n\nQuestion: {{question}}\n\nAnswer:"
        )

        # Build the conversational retrieval chain with custom prompt and tools
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm_with_tools,
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
        
    