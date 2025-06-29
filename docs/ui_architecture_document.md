# 🧠 Expert Knowledge Worker – UI Architecture Documentation

## 🎯 Purpose

This document outlines the architecture and structure of the **React TypeScript frontend UI** used in the Member Support Agent project.

---

## 📁 File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx      # Main chat interface component
│   │   ├── MessageBubble.tsx   # Individual message component
│   │   ├── TypingIndicator.tsx # Animated typing indicator
│   │   └── ChatInput.tsx       # Message input component
│   ├── api/
│   │   └── chat.ts             # API client for backend communication
│   ├── types/
│   │   └── chat.ts             # TypeScript interfaces
│   ├── App.tsx                 # Main app component
│   └── index.tsx               # App entry point
└── package.json                # Dependencies and scripts
```

---

## 🧩 UI Sections and Components

### 1. `<ChatWindow>` – Main Chat Interface

- **Header**: Assistant avatar, name ("Alexa"), role ("Member Assistant"), online status
- **Chat Area**: Scrollable container for conversation messages
- **Input Footer**: Message input field and send button

### 2. `<MessageBubble>` – Individual Messages

- **User messages**: Blue chat bubbles aligned to the right
- **Assistant messages**: White bubbles with border, aligned left
- **Message content**: Text with proper formatting and timestamps

### 3. `<TypingIndicator>` – Loading Animation

- **Animated dots**: Shows "Alexa is typing" with animated dots
- **Auto-hide**: Disappears when response is received

### 4. `<ChatInput>` – Message Input

- **Input field**: Where user types their question
- **Send button**: Floating action button (paper plane icon)
- **Validation**: Disabled when input is empty

---

## ⚙️ React/TypeScript Logic

### State Management

- `messages`: Array of conversation messages
- `isTyping`: Boolean for typing indicator
- `inputValue`: Current input field value
- `isLoading`: API call loading state

### Event Handlers

- `handleSendMessage()`: Submits message to API
- `handleInputChange()`: Updates input value
- `handleKeyPress()`: Submit on Enter key
- `scrollToBottom()`: Auto-scrolls chat

### API Integration

- `sendMessage()`: POST request to backend `/chat` endpoint
- `handleApiError()`: Error handling and user feedback
- `formatMessage()`: Formats messages for display

---

## 🎨 Styling and Frameworks

- **TailwindCSS**: Utility-first styling framework
- **Font Awesome**: Icons for bot/user/send button
- **Inter Font**: Clean and professional typography
- **Responsive Design**: Mobile-first approach
- **Custom Animations**: Smooth transitions and typing indicators

---

## ✅ Summary

This React TypeScript frontend provides a modern, responsive chat interface that integrates seamlessly with the FastAPI backend. It follows React best practices with proper component separation, TypeScript type safety, and clean UX principles.
