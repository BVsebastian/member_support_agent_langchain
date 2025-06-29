<html><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script> window.FontAwesomeConfig = { autoReplaceSvg: 'nest'};</script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    
    <style>
        ::-webkit-scrollbar { display: none;}
        * { font-family: 'Inter', sans-serif; }
    </style>
    <script>tailwind.config = {
  "theme": {
    "extend": {
      "colors": {
        "primary": "#3B82F6",
        "secondary": "#F3F4F6",
        "accent": "#1F2937"
      },
      "fontFamily": {
        "sans": [
          "Inter",
          "sans-serif"
        ]
      }
    }
  }
};</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;500;600;700;800;900&amp;display=swap"><style>
      body {
        font-family: 'Inter', sans-serif !important;
      }
      
      /* Preserve Font Awesome icons */
      .fa, .fas, .far, .fal, .fab {
        font-family: "Font Awesome 6 Free", "Font Awesome 6 Brands" !important;
      }
    </style><style>
  .highlighted-section {
    outline: 2px solid #3F20FB;
    background-color: rgba(63, 32, 251, 0.1);
  }

.edit-button {
position: absolute;
z-index: 1000;
}

::-webkit-scrollbar {
display: none;
}

html, body {
-ms-overflow-style: none;
scrollbar-width: none;
}
</style></head>

<body class="bg-gray-50 h-screen overflow-hidden">
    <div id="chat-container" class="flex flex-col h-full max-w-4xl mx-auto bg-white shadow-lg">
        <header id="header" class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-lg"></i>
                </div>
                <div>
                    <h1 class="text-xl font-semibold text-gray-900">Alexa</h1>
                    <p class="text-sm text-gray-500">Member Assistant</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-sm text-gray-600">Online</span>
            </div>
        </header>

        <main id="chat-main" class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            <div id="welcome-message" class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-gray-600 text-sm"></i>
                </div>
                <div class="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                    <p class="text-gray-800 text-sm">Hello! I'm Alexa, your member assistant. I'm here to help answer questions about your account, services, and more. How can I assist you today?</p>
                </div>
            </div>

            <div id="sample-user-message" class="flex items-start space-x-3 justify-end">
                <div class="bg-primary text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                    <p class="text-sm">What are your current loan rates?</p>
                </div>
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-white text-sm"></i>
                </div>
            </div>

            <div id="sample-assistant-message" class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-gray-600 text-sm"></i>
                </div>
                <div class="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                    <p class="text-gray-800 text-sm">Our current loan rates vary by type:</p>
                    <ul class="text-gray-800 text-sm mt-2 space-y-1">
                        <li>• Auto loans: Starting at 3.25% APR</li>
                        <li>• Personal loans: Starting at 5.99% APR</li>
                        <li>• Home loans: Starting at 4.15% APR</li>
                    </ul>
                    <p class="text-gray-800 text-sm mt-2">Would you like more details about any specific loan type?</p>
                </div>
            </div>

            <div id="typing-indicator" class="flex items-start space-x-3 hidden">
                <div class="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-gray-600 text-sm"></i>
                </div>
                <div class="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 shadow-sm">
                    <div class="flex items-center space-x-2">
                        <span class="text-gray-500 text-sm">Alexa is typing</span>
                        <div class="flex space-x-1">
                            <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                            <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                            <div class="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer id="footer" class="bg-white border-t border-gray-200 px-6 py-4">
            <div id="input-container" class="flex items-center space-x-3">
                <div class="flex-1 relative">
                    <input type="text" id="message-input" placeholder="Ask me anything..." class="w-full px-4 py-3 pr-12 bg-gray-100 border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm">
                    <button id="send-button" class="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled="">
                        <i class="fas fa-paper-plane text-sm"></i>
                    </button>
                </div>
            </div>
            <div class="flex items-center justify-center mt-2">
                <p class="text-xs text-gray-500">Powered by AI • Responses may vary</p>
            </div>
        </footer>
    </div>

    <script>
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const chatMain = document.getElementById('chat-main');
        const typingIndicator = document.getElementById('typing-indicator');

        messageInput.addEventListener('input', function() {
            sendButton.disabled = this.value.trim() === '';
        });

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !sendButton.disabled) {
                sendMessage();
            }
        });

        sendButton.addEventListener('click', sendMessage);

        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addUserMessage(message);
            messageInput.value = '';
            sendButton.disabled = true;

            showTypingIndicator();

            setTimeout(() => {
                hideTypingIndicator();
                addAssistantMessage("Thank you for your question! I'm here to help with any inquiries about your account, services, or general banking questions. How else can I assist you today?");
            }, 2000);
        }

        function addUserMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'flex items-start space-x-3 justify-end';
            messageDiv.innerHTML = `
                <div class="bg-primary text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                    <p class="text-sm">${message}</p>
                </div>
                <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-white text-sm"></i>
                </div>
            `;
            chatMain.appendChild(messageDiv);
            scrollToBottom();
        }

        function addAssistantMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'flex items-start space-x-3';
            messageDiv.innerHTML = `
                <div class="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-robot text-gray-600 text-sm"></i>
                </div>
                <div class="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
                    <p class="text-gray-800 text-sm">${message}</p>
                </div>
            `;
            chatMain.appendChild(messageDiv);
            scrollToBottom();
        }

        function showTypingIndicator() {
            typingIndicator.classList.remove('hidden');
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.classList.add('hidden');
        }

        function scrollToBottom() {
            chatMain.scrollTop = chatMain.scrollHeight;
        }
    </script>

</body></html>
