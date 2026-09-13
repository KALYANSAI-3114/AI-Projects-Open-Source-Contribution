from gtts import gTTS

def generate_speech(text, output_filepath="response.mp3"):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        tts.save(output_filepath)
        
        return output_filepath
    except Exception as e:
        return f"Error generating speech: {str(e)}"

if __name__ == "__main__":
    pass