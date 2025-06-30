import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { sendMessage } from "../api/chat.js";
import { marked } from "marked";

export default function ChatWindow() {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "assistant",
      text: "Hello! I'm Alexa, your member assistant. I'm here to help answer questions about your account, services, and more. How can I assist you today?",
      type: "welcome",
    },
    {
      id: 2,
      sender: "user",
      text: "What are your current loan rates?",
      type: "user",
    },
    {
      id: 3,
      sender: "assistant",
      text: (
        <span>
          Our current loan rates vary by type:
          <ul className="text-gray-800 text-sm mt-2 space-y-1">
            <li>• Auto loans: Starting at 3.25% APR</li>
            <li>• Personal loans: Starting at 5.99% APR</li>
            <li>• Home loans: Starting at 4.15% APR</li>
          </ul>
          <span className="block mt-2">
            Would you like more details about any specific loan type?
          </span>
        </span>
      ),
      type: "assistant",
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-focus input when processing ends
  useEffect(() => {
    if (!isProcessing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isProcessing]);

  // Real API call to send message with improved conversation flow
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = inputValue.trim();
    const userMsg = {
      id: Date.now(),
      sender: "user",
      text: userMessage,
      type: "user",
    };

    // Add user message immediately
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsTyping(true);
    setIsProcessing(true);

    try {
      // Call our real API
      const result = await sendMessage(userMessage);

      if (result.success) {
        // Add Alexa's response
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            sender: "assistant",
            text: result.data.response,
            type: "assistant",
          },
        ]);
      } else {
        // Handle API error
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            sender: "assistant",
            text: "I'm sorry, I'm having trouble connecting right now. Please try again later.",
            type: "error",
          },
        ]);
      }
    } catch (error) {
      // Handle unexpected errors
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "assistant",
          text: "I'm sorry, something went wrong. Please try again.",
          type: "error",
        },
      ]);
    } finally {
      setIsTyping(false);
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !isProcessing) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="bg-white shadow-lg max-w-xl w-full mx-auto flex flex-col h-[80vh]">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
            <FontAwesomeIcon icon={faRobot} className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="text-xl font-semibold text-gray-900">Alexa</span>
            <p className="text-sm text-gray-500">
              Horizon Bay Member Assistant
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-600">Online</span>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg) =>
          msg.sender === "assistant" ? (
            <div key={msg.id} className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
                <FontAwesomeIcon
                  icon={faRobot}
                  className="w-5 h-5 text-gray-600"
                />
              </div>
              <div
                className={`border rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm ${
                  msg.type === "error"
                    ? "bg-red-50 border-red-200"
                    : "bg-white border-gray-200"
                }`}
              >
                {typeof msg.text === "string" ? (
                  <div
                    className={`text-sm ${
                      msg.type === "error" ? "text-red-700" : "text-gray-800"
                    }`}
                    dangerouslySetInnerHTML={{ __html: marked.parse(msg.text) }}
                  />
                ) : (
                  <div
                    className={`text-sm ${
                      msg.type === "error" ? "text-red-700" : "text-gray-800"
                    }`}
                  >
                    {msg.text}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div
              key={msg.id}
              className="flex items-start space-x-3 justify-end"
            >
              <div className="bg-blue-500 text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                <p className="text-sm">{msg.text}</p>
              </div>
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <FontAwesomeIcon icon={faUser} className="w-5 h-5 text-white" />
              </div>
            </div>
          )
        )}
        {isTyping && (
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
              <FontAwesomeIcon
                icon={faRobot}
                className="w-5 h-5 text-gray-600"
              />
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 shadow-sm">
              <div className="flex items-center space-x-2">
                <span className="text-gray-500 text-sm">Alexa is typing</span>
                <div className="flex space-x-1">
                  <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4 rounded-b-2xl">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                isProcessing ? "Please wait..." : "Ask me anything..."
              }
              disabled={isProcessing}
              className="w-full px-4 py-3 pr-12 bg-gray-100 border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isProcessing}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FontAwesomeIcon icon={faPaperPlane} className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div className="flex items-center justify-center mt-2">
          <p className="text-xs text-gray-500">
            Powered by AI • Responses may vary
          </p>
        </div>
      </footer>
    </div>
  );
}
