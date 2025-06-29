
# 🧠 LangChain Tool-Calling Integration with ConversationalRetrievalChain

## 🎯 Objective  
Build a conversational AI that:
- Utilizes **RAG + memory** via `ConversationalRetrievalChain`
- Dynamically invokes external tools (search, calculations, APIs)
- Returns structured `tool_calls` alongside answers

## ⚙️ Architecture Overview  
Adopt an **agent-based approach**:
1. Wrap your retrieval chain as a tool  
2. Define additional tools (e.g., calculator, search)  
3. Bind these tools to a tool-calling LLM  
4. Use `AgentExecutor` to orchestrate reasoning and tool usage  
5. Agent output includes structured `tool_calls`

## 1. Wrap Retrieval as a Tool  
```python
from langchain_core.tools import tool

@tool
def retrieve_context(query: str) -> str:
    return conv_retrieval_chain.run({"question": query})["answer"]
```

## 2. Define Additional Tools  
```python
@tool
def calculate(expression: str) -> float:
    return safe_eval(expression)
```

## 3. Bind Tools to LLM  
```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([retrieve_context, calculate])
```

## 4. Create the Agent  
```python
from langchain.agents import create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
  ("system", "You are an AI assistant. Use `retrieve_context` for facts and `calculate` for math."),
  ("human", "{input}"),
  ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(
  llm=llm_with_tools,
  tools=[retrieve_context, calculate],
  prompt=prompt
)
```

## 5. Add Memory & Execute  
```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

executor = AgentExecutor(
  agent=agent,
  tools=[retrieve_context, calculate],
  memory=memory,
  verbose=True,
  max_iterations=5
)
```

## 6. Run & Inspect `tool_calls`  
```python
response = executor.invoke({"input": user_query})
print(response.output)
print(response.tool_calls)
```

## ✅ Why This Approach Beats Pure RetrievalChain  
| Feature                     | ConversationalRetrievalChain | Tool-Calling Agent |
|----------------------------|------------------------------|--------------------|
| RAG + Memory               | ✔️                           | ✔️                 |
| Dynamic Tool Invocation    | ❌                           | ✔️                 |
| Structured `tool_calls`    | ❌                           | ✔️                 |
| Multi-step Reasoning       | ❌                           | ✔️                 |
| Tool Enforcement           | ❌                           | ✔️                 |

## 🧪 End-to-End Sample Code  
```python
from langchain_core.tools import tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

@tool
def retrieve_context(q: str) -> str:
    return conv_retrieval_chain.run({"question": q})["answer"]

@tool
def calculate(expr: str) -> float:
    return safe_eval(expr)

tools = [retrieve_context, calculate]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools as needed."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
agent = create_tool_calling_agent(llm=llm_with_tools, tools=tools, prompt=prompt)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, max_iterations=5)

res = executor.invoke({"input": "Calculate 12*7 and then tell me the capital of France."})
print(res.output)
print(res.tool_calls)
```

## 🔗 References  
- [LangChain Tool-Calling](https://python.langchain.com/docs/how_to/tool_calling/)
- [Conversational Retrieval Agents](https://blog.langchain.dev/conversational-retrieval-agents/)
- [LangChain API Reference](https://api.python.langchain.com/)
