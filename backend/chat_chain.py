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
from document_pipeline import DocumentPipeline

class ChatChain:
    def __init__(self):
        """Initialize the agent executor with tools, memory, and LLM"""
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )
        
        # Initialize document pipeline once for reuse in forced searches
        self._doc_pipeline = DocumentPipeline()
        self._retriever = None

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
            verbose=False,
            max_iterations=5
        )

    def get_response(self, message: str) -> str:
        """Get response from the agent executor"""
        try:
            print(f"DEBUG: User message: {message}")
            
            # Use the agent executor to get response
            response = self.executor.invoke({"input": message})
            
            print(f"DEBUG: Response keys: {response.keys()}")
            
            # Check if there were tool calls
            tool_called = False
            if "intermediate_steps" in response and len(response['intermediate_steps']) > 0:
                print(f"DEBUG: Tool calls made: {len(response['intermediate_steps'])}")
                tool_called = True
                for i, step in enumerate(response['intermediate_steps']):
                    tool_name = step[0].tool
                    tool_args = step[0].tool_input
                    tool_result = step[1]
                    print(f"DEBUG: Tool {i+1}: {tool_name}")
                    print(f"DEBUG: Tool {i+1} args: {tool_args}")
                    print(f"DEBUG: Tool {i+1} result: {str(tool_result)[:100]}...")
            else:
                print(f"❌ DEBUG: NO TOOL CALLS MADE - FORCING SEARCH!")
                
                # Force a search if agent didn't use tools
                try:
                    print(f"🔧 FORCING direct retriever search with query: '{message}'")
                    
                    # Use cached retriever for better performance
                    if not self._retriever:
                        self._retriever = self._doc_pipeline.get_retriever()
                    
                    search_result = self._retriever.invoke(message)
                    print(f"🔍 FORCED SEARCH FOUND: {len(search_result)} documents")
                    
                    # Create a new response based on search results
                    if search_result:
                        doc_content = "\n".join([doc.page_content for doc in search_result[:3]])
                        print(f"🔧 DOCUMENT CONTENT PREVIEW: {doc_content[:200]}...")
                        
                        new_prompt = f"""Based on this information from the knowledge base:

{doc_content}

Please answer the user's question: {message}

If the information doesn't contain the answer, say so and provide the default contact number 1-888-HBCU-HELP."""
                        
                        forced_response = self.llm.invoke(new_prompt)
                        print(f"🔧 FORCED RESPONSE: {forced_response.content[:100]}...")
                        return forced_response.content
                    else:
                        return "I wasn't able to find information about that in our knowledge base. Please contact our member service representatives at 1-888-HBCU-HELP for assistance."
                        
                except Exception as e:
                    print(f"❌ FORCED SEARCH ERROR: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fall back to original response if forced search fails
            
            # Check memory state
            if "chat_history" in response:
                print(f"DEBUG: Memory has {len(response['chat_history'])} messages")
            
            # Return the output from the agent
            output = response["output"]
            print(f"DEBUG: Agent response: {output[:100]}...")
            
            return output
            
        except Exception as e:
            print(f"DEBUG: Error: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support." 
        
    