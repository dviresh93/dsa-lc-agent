import whisper
import speech_recognition as sr
import tempfile
import os
from typing import Optional

class SpeechToText:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the Speech-to-Text engine
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("Whisper model and microphone ready!")
    
    def record_audio(self, duration: int = 5, timeout: int = 1) -> str:
        """
        Record audio from microphone and return the transcribed text
        
        Args:
            duration: Maximum recording duration in seconds
            timeout: Timeout before recording starts
            
        Returns:
            Transcribed text
        """
        print(f"🎤 Start speaking... (will stop automatically or after {duration} seconds)")
        
        try:
            with self.microphone as source:
                # Listen for audio with timeout and phrase time limit
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=duration
                )
            
            print("✅ Recording completed!")
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_filename = tmp_file.name
                
                # Write audio data to file
                with open(temp_filename, 'wb') as f:
                    f.write(audio.get_wav_data())
            
            print("🔄 Transcribing audio...")
            # Transcribe using Whisper
            result = self.model.transcribe(temp_filename)
            transcribed_text = result["text"].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            print(f"📝 Transcribed: '{transcribed_text}'")
            return transcribed_text
            
        except sr.WaitTimeoutError:
            print("❌ No speech detected within timeout period")
            return ""
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition: {e}")
            return ""
        except Exception as e:
            print(f"❌ Error during recording/transcription: {e}")
            return ""
    
    def transcribe_file(self, audio_file_path: str) -> str:
        """
        Transcribe audio from a file
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            print(f"🔄 Transcribing file: {audio_file_path}")
            result = self.model.transcribe(audio_file_path)
            transcribed_text = result["text"].strip()
            print(f"📝 Transcribed: '{transcribed_text}'")
            return transcribed_text
        except Exception as e:
            print(f"❌ Error transcribing file: {e}")
            return ""

# Test function
if __name__ == "__main__":
    try:
        stt = SpeechToText()
        
        print("Testing Speech-to-Text...")
        print("Press Enter when ready to start recording...")
        input()
        
        text = stt.record_audio(duration=5)
        print(f"Result: {text}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have a microphone connected and permissions are granted.")