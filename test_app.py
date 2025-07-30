#!/usr/bin/env python3
"""
Simple test script for the Voice Q&A Application
"""

import os
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from qa_processor import QAProcessor

def test_individual_components():
    """Test each component individually"""
    print("🧪 Testing Individual Components")
    print("=" * 50)
    
    # Test 1: Text-to-Speech
    print("\n1. Testing Text-to-Speech...")
    try:
        tts = TextToSpeech()
        test_message = "Hello! Text to speech is working correctly."
        print(f"Speaking: {test_message}")
        tts.speak(test_message)
        print("✅ TTS test passed!")
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
    
    # Test 2: Q&A Processor
    print("\n2. Testing Q&A Processor...")
    try:
        qa = QAProcessor()
        test_question = "Hello, how are you?"
        response = qa.process_question(test_question)
        print(f"Q: {test_question}")
        print(f"A: {response}")
        print("✅ Q&A test passed!")
    except Exception as e:
        print(f"❌ Q&A test failed: {e}")
    
    # Test 3: Speech-to-Text (optional - requires user input)
    print("\n3. Testing Speech-to-Text...")
    try:
        print("This test requires speaking into your microphone.")
        choice = input("Do you want to test speech recognition? (y/n): ").lower()
        
        if choice == 'y':
            stt = SpeechToText(model_size="tiny")  # Use tiny model for faster loading
            print("Speak something for testing...")
            text = stt.record_audio(duration=3)
            print(f"You said: '{text}'")
            print("✅ STT test completed!")
        else:
            print("⏭️ STT test skipped")
    except Exception as e:
        print(f"❌ STT test failed: {e}")

def test_integration():
    """Test the complete integration"""
    print("\n🔗 Testing Complete Integration")
    print("=" * 50)
    
    try:
        # Initialize components
        print("Initializing components...")
        tts = TextToSpeech()
        qa = QAProcessor()
        
        # Test without speech recognition first
        print("\n📝 Testing text-based Q&A flow...")
        
        test_questions = [
            "Hello",
            "What is Python?",
            "How are you?",
            "Thank you"
        ]
        
        for question in test_questions:
            print(f"\nQ: {question}")
            response = qa.process_question(question)
            print(f"A: {response}")
            
            # Speak the response
            print("🔊 Speaking response...")
            tts.speak(response)
            
            print("✅ Question processed successfully!")
        
        print("\n✅ Integration test completed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def main():
    """Main test function"""
    print("🎙️ Voice Q&A Application - Test Suite")
    print("Powered by OpenAI Whisper + GPT + Text-to-Speech")
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found!")
    else:
        print("⚠️ No OpenAI API key found - using fallback responses")
    
    print("\nChoose test mode:")
    print("1. Test individual components")
    print("2. Test complete integration")
    print("3. Test both")
    
    try:
        choice = input("Enter choice (1-3) [3]: ").strip() or "3"
        
        if choice in ["1", "3"]:
            test_individual_components()
        
        if choice in ["2", "3"]:
            test_integration()
            
        print("\n🎉 All tests completed!")
        
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")

if __name__ == "__main__":
    main()