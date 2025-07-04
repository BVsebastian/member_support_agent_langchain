"""
Chat Chain for Alexa - Member Support Agent
Builds LangChain's AgentExecutor with tool calling agent
"""

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from prompt_manager import get_system_prompt
from tools import send_notification, record_user_details, log_unknown_question, search_knowledge_base

class ChatChain:
    def __init__(self):
        """Initialize the agent executor with tools, memory, and LLM"""
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

        # Define all tools
        self.tools = [
            search_knowledge_base,
            send_notification,
            record_user_details,
            log_unknown_question
        ]

        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Get system prompt
        system_prompt = get_system_prompt()

        # Create prompt template for agent
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        # Create the agent
        self.agent = create_tool_calling_agent(
            llm=self.llm_with_tools,
            tools=self.tools,
            prompt=self.prompt
        )

        # Create the executor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,  # Enable verbose to see tool calls
            max_iterations=5
        )

    def get_response(self, message: str) -> str:
        """Get response using the agent executor with verbose logging"""
        try:
            print(f"🎯 AGENT EXECUTOR: Processing message: '{message}'")
            
            # Use the agent executor that's already configured
            response = self.executor.invoke({"input": message})
            
            print(f"🤖 AGENT RESPONSE: {response.get('output', 'No output')[:100]}...")
            return response.get('output', 'I apologize, but I encountered an issue processing your request.')
                
        except Exception as e:
            print(f"❌ AGENT ERROR: {e}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support at 1-888-HBCU-HELP." 
        
    