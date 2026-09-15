from gtts import gTTS

def generate_speech(text, output_filepath):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        tts.save(output_filepath)
        
        return output_filepath
    except Exception:
        return None