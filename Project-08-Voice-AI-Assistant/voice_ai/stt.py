from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_file_path):
    try:
        segments, info = model.transcribe(audio_file_path, beam_size=5, vad_filter=True)
        
        text = "".join([segment.text for segment in segments])
        
        text = text.strip()
        
        if len(text) > 1000:
            text = text[:1000]
            
        return text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"