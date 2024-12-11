import speech_recognition as sr

def transcribe_audio(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_path) as source:
            print("Processing audio...")
            audio_data = recognizer.record(source)  # Read the entire audio file

        # Transcribe audio to text
        text = recognizer.recognize_google(audio_data)
        return text

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
audio_path = r"backend logic\testaudio.wav"  # Replace with the path to your audio file
transcription = transcribe_audio(audio_path)
print("Transcription:")
print(transcription)
