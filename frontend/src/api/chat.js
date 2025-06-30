import axios from "axios";

// Create configured axios instance
const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000, // 30 seconds
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log("API Request:", {
      method: config.method?.toUpperCase(),
      url: config.url,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    console.log("API Response:", {
      status: response.status,
      url: response.config.url,
      data: response.data,
    });
    return response;
  },
  (error) => {
    console.error("API Response Error:", {
      status: error.response?.status,
      message: error.message,
      url: error.config?.url,
      data: error.response?.data,
    });
    return Promise.reject(error);
  }
);

// Send message to chat endpoint
const sendMessage = async (message) => {
  try {
    // Send POST request to /chat endpoint
    const response = await apiClient.post("/chat", { message });

    // Return successful response
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    // Handle different types of errors
    let errorMessage = "Sorry, I'm having trouble connecting right now.";

    if (error.response) {
      // Server responded with error status
      if (error.response.status === 400) {
        errorMessage = "Invalid request. Please try again.";
      } else if (error.response.status === 500) {
        errorMessage = "Server error. Please try again later.";
      } else {
        errorMessage = `Error ${error.response.status}. Please try again.`;
      }
    } else if (error.request) {
      // Network error - no response received
      errorMessage = "Network error. Please check your connection.";
    } else {
      // Other error
      errorMessage = "An unexpected error occurred. Please try again.";
    }

    // Return error response
    return {
      success: false,
      error: errorMessage,
    };
  }
};

// Test function to verify sendMessage works
const testSendMessage = async () => {
  console.log("🧪 Testing sendMessage function...");

  try {
    const result = await sendMessage("Hello Alexa, what are your loan rates?");
    console.log("✅ Test result:", result);

    if (result.success) {
      console.log("✅ Success! Response:", result.data);
    } else {
      console.log("❌ Error:", result.error);
    }
  } catch (error) {
    console.error("❌ Test failed:", error);
  }
};

export default apiClient;
export { sendMessage, testSendMessage };
