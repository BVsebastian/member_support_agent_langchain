import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

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

  // Simulate typing indicator and assistant response
  const handleSendMessage = () => {
    if (!inputValue.trim()) return;
    const userMsg = {
      id: Date.now(),
      sender: "user",
      text: inputValue,
      type: "user",
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsTyping(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "assistant",
          text: "Thank you for your question! I'm here to help with any inquiries about your account, services, or general banking questions. How else can I assist you today?",
          type: "assistant",
        },
      ]);
      setIsTyping(false);
    }, 2000);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
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
              <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                <div className="text-gray-800 text-sm">{msg.text}</div>
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
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4 rounded-b-2xl">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything..."
              className="w-full px-4 py-3 pr-12 bg-gray-100 border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm text-gray-800"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim()}
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
