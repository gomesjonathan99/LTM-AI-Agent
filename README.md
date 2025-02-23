# 🤖 LTM-AI-Agent  

**LTM-AI-Agent** is an AI chatbot with **Long-Term Memory (LTM)** that remembers user interactions, recalls past conversations, and adapts responses based on stored context.  

## 🚀 Features  
- ✅ **Persistent Memory**: Stores & retrieves chat history from SQLite.  
- ✅ **Context Awareness**: Remembers user details across sessions.  
- ✅ **Contradiction Handling**: Updates facts when new information is provided.  
- ✅ **Inference & Reasoning**: Understands and adapts responses based on memory.  
- ✅ **Time-Based Memory**: Can recall past events over time.  

## 🛠 Tech Stack  
- **Python** 🐍  
- **SQLite** 🗄️  
- **Pydantic AI** 🤖  
- **OpenAI GPT-3.5 Turbo**  

## 📂 Project Structure  
```
📦 LTM-AI-Agent
├── 📜 store_conversation_advance.py  # Chatbot logic & memory handling
├── 📜 conversation1.db               # SQLite database (auto-created)
├── 📜 requirements.txt               # Dependencies
├── 📜 README.md                      # Project documentation
```

## 🚀 Clone & Run  

### 1️⃣ Clone the repository  
```sh
git clone https://github.com/JonathanJourney99/LTM-AI-Agent.git
```

### 2️⃣ Install dependencies  
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the chatbot  
```sh
python store_conversation_advance.py
```

## 📌 Usage  

- **Start a conversation**  
  ```python
  print(chat(session_id="session_12", message="Hello!"))
  ```

- **Retrieve past knowledge**  
  ```python
  print(chat(session_id="session_12", message="What do you remember about me?"))
  ```

- **Handle contradictions**  
  ```python
  print(chat(session_id="session_12", message="Actually, I don't have a pet."))
  print(chat(session_id="session_12", message="Do I have a pet?"))
  ```
## 📜 License  
This project is licensed under the **MIT License**.  
---
