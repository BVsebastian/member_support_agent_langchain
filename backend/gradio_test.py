"""
Gradio test interface for Member Support Agent
"""

import gradio as gr
from chat_chain import ChatChain

# Initialize chat chain
chat_chain = ChatChain()

def chat_with_alexa(message, history):
    """Chat with Alexa"""
    response = chat_chain.get_response(message)
    return response

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_alexa,
    title="Alexa - Member Support Agent",
    description="Ask me about Horizon Bay Credit Union services!",
    examples=[
        "What services do you offer?",
        "How do I apply for a loan?",
        "What are your account fees?",
        "I need help with my debit card"
    ]
)

if __name__ == "__main__":
    demo.launch() 