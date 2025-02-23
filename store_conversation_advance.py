import json
import sqlite3
from typing import List
from datetime import datetime
from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart, UserPromptPart, SystemPromptPart, ModelRequest

class SQLliteDB:
    def __init__(self, db_name='conversation1.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        
    def create_table(self):
        with self.conn:
             self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_list TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    def add_message(self, session_id: str, messages:str) -> None:
        self.conn.execute("INSERT INTO conversation_history2 (session_id, message_list) VALUES (?,?)", (session_id, messages))
        self.conn.commit()
    
    def get_history(self, session_id:str)-> List[ModelMessage]:
        def _parse_message(data: bytes)->List[ModelMessage]:
            json_data = json.loads(data.decode('utf-8'))
            messages = []
            
            for msg in json_data:
                parts = []
                for part in msg['parts']:
                    part_kind = part['part_kind']

                    if part_kind == 'system-prompt':
                        parts.append(SystemPromptPart(content=part['content'], dynamic_ref=part.get('dynamic_ref')))
                    elif part_kind == 'user-prompt':
                        parts.append(UserPromptPart(
                            content=part['content'],
                            timestamp=datetime.fromisoformat(part['timestamp']),
                            part_kind=part['part_kind'],
                        ))
                    elif part_kind == 'text':
                        parts.append(TextPart(content=part['content'], part_kind=part['part_kind']))
                    else:
                        raise ValueError(f"Unknown part_kind: {part_kind}")
                if msg['kind'] == 'request':
                    messages.append(ModelRequest(parts=parts, kind='request'))
                elif msg['kind'] == 'response':
                    messages.append(ModelResponse(
                        parts=parts,
                        model_name=msg.get('model_name'),
                        timestamp=datetime.fromisoformat(msg['timestamp'].replace("Z", "")),
                        kind='response',
                    ))
                else:
                    raise ValueError(f"Unknown Message Kind: {msg['kind']}")
            return messages
        cursor = self.conn.execute(f"SELECT message_list from conversation_history2 WHERE session_id= '{session_id}' ORDER BY timestamp DESC LIMIT 1")
        messages = cursor.fetchall()
        model_messages: list[ModelMessage] = []
        
        for item in messages:
            model_messages.extend(_parse_message(item[0]))
        return model_messages
    
def chat(session_id:str, message:str)-> ModelMessage:  
    history = db.get_history(session_id)
    result = agent.run_sync(message, message_history=history)
    db.add_message(session_id, result.all_messages_json())  
    return result.data

db = SQLliteDB()
session_id = 'session_12'
agent = Agent('openai:gpt-3.5-turbo-0125', system_prompt='Be an helpful assistant and answer in a concise manner.')

## Testing
# print(chat(session_id, "Hello, my name is Alexander, but people call me Alex."))
# print(chat(session_id, "I work as a software engineer at Google."))
# print(chat(session_id, "I live in New York with my wife and two kids."))
# print(chat(session_id, "My hobbies include hiking, chess, and playing the piano."))
# print(chat(session_id, "Oh, and I also have a golden retriever named Max!"))

# # 🔍 **Memory Recall Test**
# print(chat(session_id, "What is my name?"))  # Should respond with "Your name is Alexander, but people call you Alex."
# print(chat(session_id, "Where do I work?"))  # Should say "You work at Google."
# print(chat(session_id, "Tell me about my pet."))  # Should recall "You have a golden retriever named Max."

# # 🔄 **Context Switching Test**
# print(chat(session_id, "By the way, I recently started learning French."))
# print(chat(session_id, "Can you remind me which language I’m learning?"))  # Should say "French."
# print(chat(session_id, "What other hobbies do I have?"))  # Should list hiking, chess, and piano.

# # ❌ **Contradiction Test**
# print(chat(session_id, "Actually, I don't have any pets."))  # Changes previous fact
# print(chat(session_id, "Do I have a pet?"))  # Should acknowledge contradiction & clarify

# # 🧠 **Inference & Reasoning Test**
# print(chat(session_id, "I just moved to San Francisco!"))
# print(chat(session_id, "Where do I live?"))  # Should now say "San Francisco" instead of "New York."
# print(chat(session_id, "Does my workplace match my location?"))  # Should infer "Yes, Google has offices in San Francisco."

# # 🔀 **Memory Overload & List Handling**
# print(chat(session_id, "I have visited Japan, Canada, and Germany."))
# print(chat(session_id, "Which countries have I traveled to?"))  # Should list the correct countries.

# # ⏳ **Time-Based Reasoning**
# print(chat(session_id, "Today is my wife's birthday."))
# print(chat(session_id, "What special event is happening today?"))  # Should recall and mention the wife's birthday.
# print(chat(session_id, "Remind me in a week what happened today."))  # Should handle time-based reminders.

# # 🏗 **Extended Knowledge Test**
# print(chat(session_id, "I'm planning to build a mobile app for fitness tracking."))
# print(chat(session_id, "What kind of features should I consider for my app?"))  # Should generate fitness app ideas.
# print(chat(session_id, "Based on what you know about me, do you think I would enjoy working on this app?"))  
# # Should recall past responses (software engineer, hobbies, hiking) and infer motivation.

# # 🚀 **Future Intent Test**
# print(chat(session_id, "I want to start a YouTube channel next year."))
# print(chat(session_id, "What goals have I mentioned for the future?"))  
# # Should list fitness app & YouTube channel.

# # 🛠 **Technical Knowledge Check**
# print(chat(session_id, "I mostly work with Python and JavaScript."))
# print(chat(session_id, "Recommend a Python framework for web development."))  # Should suggest Django or Flask.
# print(chat(session_id, "Which programming languages do I use?"))  # Should recall Python & JavaScript.

# # 🔄 **Final Memory Summary Test**
# print(chat(session_id, "Summarize everything you know about me."))  
# # Should generate a detailed summary of Alex, his job, location, hobbies, pet status, language learning, travels, and future goals.

print(chat(session_id=session_id, message='Who am I and What do I Program??'))

