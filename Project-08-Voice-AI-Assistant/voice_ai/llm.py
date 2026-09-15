import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "qwen/qwen3.8-27b"

def get_llm_response(user_input, conversation_history):
    temp_history = conversation_history + [{"role": "user", "content": user_input}]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=temp_history,
            model=MODEL_NAME,
        )
        ai_response = chat_completion.choices[0].message.content
        
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response, conversation_history

    except Exception:
        return None, conversation_history