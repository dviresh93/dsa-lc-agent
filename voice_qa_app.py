#!/usr/bin/env python3
"""
Voice Q&A Application
Integrates speech-to-text, OpenAI API, and text-to-speech for a complete voice interaction system
"""

import os
import sys
import time
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from qa_processor import QAProcessor

class VoiceQAApp:
    def __init__(self, whisper_model="base", openai_api_key=None):
        """
        Initialize the Voice Q&A application
        
        Args:
            whisper_model: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
            openai_api_key: OpenAI API key (optional, can be set via environment variable)
        """
        print("🚀 Initializing Voice Q&A Application...")
        print("=" * 50)
        
        # Initialize components
        try:
            print("📝 Loading Speech-to-Text engine...")
            self.stt = SpeechToText(model_size=whisper_model)
            
            print("🔊 Initializing Text-to-Speech engine...")
            self.tts = TextToSpeech()
            
            print("🧠 Setting up Q&A processor...")
            self.qa = QAProcessor(api_key=openai_api_key)
            
            print("=" * 50)
            print("✅ Voice Q&A Application ready!")
            
            # Welcome message
            welcome_msg = "Hello! I'm your voice assistant. I can listen to your questions and respond using AI. Say 'quit' or 'exit' to stop."
            print(f"🤖 {welcome_msg}")
            self.tts.speak(welcome_msg)
            
        except Exception as e:
            print(f"❌ Error initializing application: {e}")
            sys.exit(1)
    
    def listen_and_respond(self, recording_duration=5):
        """
        Listen to user input, process the question, and respond with voice
        
        Args:
            recording_duration: How long to record in seconds
        """
        try:
            # Step 1: Listen to user input
            print("\n" + "="*50)
            user_question = self.stt.record_audio(duration=recording_duration)
            
            if not user_question:
                error_msg = "I couldn't hear you clearly. Please try again."
                print(f"⚠️ {error_msg}")
                self.tts.speak(error_msg)
                return True
            
            # Check for exit commands
            if any(word in user_question.lower() for word in ['quit', 'exit', 'stop', 'bye']):
                goodbye_msg = "Goodbye! Thanks for using the voice assistant."
                print(f"👋 {goodbye_msg}")
                self.tts.speak(goodbye_msg)
                return False
            
            # Step 2: Process the question using OpenAI
            print("🧠 Processing your question...")
            ai_response = self.qa.process_question(user_question)
            
            if not ai_response:
                ai_response = "I'm sorry, I couldn't process your question. Please try again."
            
            print(f"🤖 Response: {ai_response}")
            
            # Step 3: Convert response to speech and play it
            self.tts.speak(ai_response)
            
            return True
            
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            return False
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            print(f"❌ {error_msg}")
            self.tts.speak("Sorry, I encountered an error. Please try again.")
            return True
    
    def run_interactive_mode(self):
        """Run the voice Q&A application in interactive mode"""
        print("\n🎤 Interactive Mode Started")
        print("💡 Tips:")
        print("   - Speak clearly after the recording prompt")
        print("   - Say 'quit', 'exit', or 'stop' to end the session")
        print("   - Press Ctrl+C at any time to quit")
        
        try:
            while True:
                print("\n📞 Ready for your question...")
                if not self.listen_and_respond():
                    break
                
                # Small pause between interactions
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n👋 Session ended by user. Goodbye!")
    
    def test_components(self):
        """Test all components individually"""
        print("\n🧪 Testing Components...")
        
        # Test TTS
        print("1. Testing Text-to-Speech...")
        self.tts.speak("Text to speech is working correctly.")
        
        # Test Q&A processor
        print("2. Testing Q&A Processor...")
        test_response = self.qa.process_question("Hello, can you hear me?")
        print(f"   Q&A Response: {test_response}")
        self.tts.speak(test_response)
        
        # Test STT (requires user input)
        print("3. Testing Speech-to-Text...")
        print("   Say something for 3 seconds...")
        transcribed = self.stt.record_audio(duration=3)
        print(f"   Transcribed: '{transcribed}'")
        
        print("✅ Component testing completed!")

def main():
    """Main function to run the Voice Q&A application"""
    print("🎙️ Voice Q&A Application")
    print("Powered by OpenAI Whisper + GPT + Text-to-Speech")
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️ WARNING: No OpenAI API key found!")
        print("Set your API key with: export OPENAI_API_KEY='your-api-key-here'")
        print("Or the app will use basic fallback responses.")
        
        user_input = input("\nContinue anyway? (y/n): ").lower()
        if user_input != 'y':
            print("👋 Goodbye!")
            return
    
    # Get user preferences
    print("\n⚙️ Configuration:")
    model_choice = input("Whisper model size (tiny/base/small/medium/large) [base]: ").strip() or "base"
    
    try:
        # Initialize and run the application
        app = VoiceQAApp(whisper_model=model_choice, openai_api_key=api_key)
        
        # Choose mode
        print("\n🎯 Choose mode:")
        print("1. Interactive Voice Q&A")
        print("2. Test Components")
        
        choice = input("Enter choice (1-2) [1]: ").strip() or "1"
        
        if choice == "2":
            app.test_components()
        else:
            app.run_interactive_mode()
            
    except Exception as e:
        print(f"❌ Application error: {e}")
    
    print("\n👋 Thanks for using Voice Q&A!")

if __name__ == "__main__":
    main()