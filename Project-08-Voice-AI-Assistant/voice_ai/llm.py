import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "qwen/qwen3.8-27b"

def get_llm_response(user_input, conversation_history):
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model=MODEL_NAME,
        )
        ai_response = chat_completion.choices[0].message.content
        
        conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        return ai_response, conversation_history

    except Exception as e:
        return f"Error talking to AI: {str(e)}", conversation_history

# --- Testing block ---
if __name__ == "__main__":
    history = [
        {"role": "system", "content": "You are a helpful, friendly voice assistant. Keep your answers brief and conversational."}
    ]
    
    print("AI Brain initialized. Type 'quit' to exit.")
    while True:
        user_text = input("You: ")
        if user_text.lower() == 'quit':
            break
            
        response, history = get_llm_response(user_text, history)
        print(f"AI: {response}")
        print(f"(Memory now has {len(history)} messages)\n")