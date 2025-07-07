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
        
        # Session management
        self.session_conversations = {}  # session_id -> conversation_id

    def get_or_create_conversation(self, session_id: str) -> int:
        """Get existing conversation or create new one for session"""
        from database import ConversationCRUD, UserCRUD, ConversationCreate, UserCreate
        
        # Check if session already has a conversation
        if session_id in self.session_conversations:
            return self.session_conversations[session_id]
        
        # Create anonymous user for this session
        try:
            user = UserCRUD.create(UserCreate(
                name="Anonymous",
                email=f"anonymous_{session_id}@demo.com"
            ))
        except Exception:
            # User might already exist, try to get by email
            user = UserCRUD.get_by_email(f"anonymous_{session_id}@demo.com")
            if not user:
                raise Exception("Failed to create or retrieve user")
        
        # Create new conversation for this session
        conversation = ConversationCRUD.create(ConversationCreate(
            user_id=user.id
        ))
        
        # Store conversation ID for this session
        self.session_conversations[session_id] = conversation.id
        
        print(f"📝 SESSION: Created conversation {conversation.id} for session {session_id}")
        return conversation.id

    def store_message(self, conversation_id: int, content: str, sender: str = "user"):
        """Store message in database"""
        from database import MessageCRUD, MessageCreate
        
        try:
            message = MessageCRUD.create(MessageCreate(
                conversation_id=conversation_id,
                content=content
            ))
            print(f"💾 MESSAGE: Stored {sender} message in conversation {conversation_id}")
            return message
        except Exception as e:
            print(f"❌ MESSAGE STORAGE ERROR: {e}")
            return None

    def get_response(self, message: str, session_id: str = None) -> str:
        """Get response using the agent executor with verbose logging and session management"""
        try:
            print(f"🎯 AGENT EXECUTOR: Processing message: '{message}'")
            
            # Handle session management if session_id provided
            conversation_id = None
            if session_id:
                conversation_id = self.get_or_create_conversation(session_id)
                # Store user message
                self.store_message(conversation_id, message, "user")
            
            # Create enhanced input with session context for tools
            enhanced_input = message
            if session_id:
                enhanced_input = f"Session ID: {session_id}\n\nUser Message: {message}"
            
            # Use the agent executor that's already configured
            response = self.executor.invoke({"input": enhanced_input})
            
            # Extract the response text
            response_text = response.get('output', 'I apologize, but I encountered an issue processing your request.')
            
            # Store agent response if we have a conversation
            if conversation_id:
                self.store_message(conversation_id, response_text, "agent")
            
            print(f"🤖 AGENT RESPONSE: {response_text[:100]}...")
            return response_text
                
        except Exception as e:
            print(f"❌ AGENT ERROR: {e}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support at 1-888-HBCU-HELP." 
        
    