import React, { useState } from "react";
import "./App.css"; // import this

const App = () => {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]); // [ [user, bot], ... ]
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newHistory = [...chatHistory, [userInput, ""]];
    setChatHistory(newHistory);
    setUserInput("");
    setIsLoading(true);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userInput,
        history: chatHistory,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let botReply = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      botReply += decoder.decode(value);
      setChatHistory((prev) => {
        const updated = [...prev];
        updated[updated.length - 1][1] = botReply;
        return updated;
      });
    }

    setIsLoading(false);
  };

  return (
    <div className="app-container">
      <h1 className="chat-title">🏡 Aarvasa Chat Assistant</h1>

      <div className="chat-box">
        {chatHistory.map(([user, bot], i) => (
          <div className="chat-message" key={i}>
            <div className="user">You: {user}</div>
            <div className="bot">Bot: {bot}</div>
            <hr className="divider" />
          </div>
        ))}
        {isLoading && <div className="typing">Typing...</div>}
      </div>

      <div className="input-area">
        <input
          placeholder="Ask about properties or navigation..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default App;
