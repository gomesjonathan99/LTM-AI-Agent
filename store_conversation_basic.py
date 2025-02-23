import sqlite3
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

class SQLliteDB:
    def __init__(self, db_name='conversation.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        
    def create_table(self):
        with self.conn:
             self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                agent_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    def save_message(self, session_id, user_message, agent_response):
        with self.conn:
            self.conn.execute('''
                              INSERT INTO conversation_history (session_id, user_message, agent_response)
                              VALUES (?, ?, ?)
                              ''', (session_id, user_message, agent_response))
    def get_history(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_message, agent_response FROM conversation_history WHERE session_id = ? ORDER BY timestamp ASC',(session_id, ))
        return cursor.fetchall()
    
def chat(session_id, message):  
    history = db.get_history(session_id)
    context = '\n'.join(f'User: {msg}\nAssistant: {resp}' for msg, resp in history)
    result = agent.run_sync(f'{context}\nUser: {message}')
    response = result.data
    db.save_message(session_id, message, response)  
    return response

db = SQLliteDB()
session_id = 'session_1'
agent = Agent('openai:gpt-3.5-turbo-0125', system_prompt='Be an helpful assistant and answer in a concise manner.')

# print(chat(session_id, 'Hi I am John Roger'))
print(chat(session_id, 'Can you tell me what you know about me?'))