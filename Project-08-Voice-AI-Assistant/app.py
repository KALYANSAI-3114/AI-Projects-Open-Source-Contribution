import streamlit as st
import os
import tempfile
from voice_ai.llm import get_llm_response
from voice_ai.stt import transcribe_audio
from voice_ai.tts import generate_speech

st.set_page_config(page_title="Voice AI Assistant", page_icon="🦢", layout="centered")
st.title("🦢 Voice AI Assistant")
st.write("Click the microphone, ask a question, and hear the AI respond!")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": "You are an advanced, highly intelligent voice assistant. Your primary goal is to provide the most accurate, direct, and concise answers possible. Because your responses will be read aloud, you must avoid long paragraphs, bullet points, and markdown formatting. Speak in a natural, conversational tone. Never mention that you are an AI model like Qwen, Llama, or Groq. If asked about your identity, state that you are an advanced Voice AI Assistant. Get straight to the point without filler words like 'Well' or 'Actually'."}
    ]

for message in st.session_state.conversation_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])

audio_value = st.audio_input("Record your question")

if audio_value:
    audio_bytes = audio_value.getvalue()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name
    
    with st.spinner("Listening..."):
        user_text = transcribe_audio(temp_audio_path)
        os.remove(temp_audio_path) 
        
        if not user_text:
            st.error("I couldn't hear you. Please try again.")
        else:
            with st.chat_message("user"):
                st.write(user_text)
                
            with st.spinner("Thinking..."):
                ai_response, st.session_state.conversation_history = get_llm_response(
                    user_text, st.session_state.conversation_history
                )
                
                if not ai_response:
                    st.error("I had trouble connecting to my brain. Please try again.")
                else:
                    with st.chat_message("assistant"):
                        st.write(ai_response)
                        
                    with st.spinner("Speaking..."):
                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_resp:
                            resp_path = temp_resp.name
                        
                        audio_file_path = generate_speech(ai_response, resp_path)
                        
                        if audio_file_path:
                            st.audio(audio_file_path, format="audio/mp3")
                            os.remove(audio_file_path)
                        else:
                            st.error("I couldn't generate audio for the response.")