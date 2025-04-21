//Chat
import { useEffect, useRef, useState } from "react";
import { useAuth } from "../../context/AuthContext";

export default function Chat() {
  const { user: currentUser, token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const ws = useRef(null);

  useEffect(() => {
    // ws.current = new WebSocket(`ws://${window.location.host}/chat/ws`);
    // ws.current = new WebSocket("ws://localhost:8000/chat/ws");
    ws.current = new WebSocket(`ws://localhost:8000/chat/ws?token=${token}`);

    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      ws.current.close();
    };
  }, []);

  const sendMessage = (e) => {
    e.preventDefault();
    if (inputValue && ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(inputValue);
      setInputValue("");
    }
  };

  return (
    <div>
      <h1>WebSocket Chat</h1>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          autoComplete="off"
        />
        <button type="submit">Send</button>
      </form>
      <ul>
        {messages.map((msg, idx) => (
          <li key={idx}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}
