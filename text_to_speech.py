import pyttsx3
from typing import Optional

class TextToSpeech:
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize the Text-to-Speech engine
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        try:
            self.engine = pyttsx3.init()
            
            # Configure speech settings
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to use a female voice if available, otherwise use default
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
            
            print("✅ Text-to-Speech engine initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing TTS engine: {e}")
            self.engine = None
    
    def speak(self, text: str) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            
        Returns:
            True if successful, False otherwise
        """
        if not self.engine:
            print("❌ TTS engine not available")
            return False
        
        if not text.strip():
            print("⚠️ No text to speak")
            return False
        
        try:
            print(f"🔊 Speaking: '{text}'")
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ Error during speech: {e}")
            return False
    
    def save_to_file(self, text: str, filename: str) -> bool:
        """
        Save text as audio file
        
        Args:
            text: Text to convert
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if not self.engine:
            print("❌ TTS engine not available")
            return False
        
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            print(f"✅ Audio saved to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
            return False
    
    def set_rate(self, rate: int):
        """Set speech rate"""
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        if self.engine:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def list_voices(self):
        """List available voices"""
        if not self.engine:
            print("❌ TTS engine not available")
            return
        
        voices = self.engine.getProperty('voices')
        if voices:
            print("Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} ({voice.id})")
        else:
            print("No voices available")
    
    def set_voice(self, voice_index: int):
        """Set voice by index"""
        if not self.engine:
            print("❌ TTS engine not available")
            return
        
        voices = self.engine.getProperty('voices')
        if voices and 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            print(f"✅ Voice changed to: {voices[voice_index].name}")
        else:
            print(f"❌ Invalid voice index: {voice_index}")

# Test function
if __name__ == "__main__":
    tts = TextToSpeech()
    
    print("Testing Text-to-Speech...")
    
    # List available voices
    tts.list_voices()
    
    # Test speech
    test_text = "Hello! This is a test of the text to speech system. How do I sound?"
    tts.speak(test_text)