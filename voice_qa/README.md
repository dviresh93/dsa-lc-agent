# Voice Q&A Application

A complete voice-powered question and answer system that integrates speech-to-text, OpenAI GPT, and text-to-speech for natural voice interactions.

## Features

- 🎤 **Speech Recognition**: Uses OpenAI Whisper for accurate speech-to-text conversion
- 🧠 **AI-Powered Responses**: Integrates with OpenAI GPT for intelligent question answering
- 🔊 **Text-to-Speech**: Converts AI responses back to natural-sounding speech
- 💬 **Interactive Mode**: Continuous voice conversation loop
- 🛠️ **Fallback Support**: Works even without OpenAI API key (limited functionality)

## Setup

### 1. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set OpenAI API Key (Recommended)
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Quick Start
```bash
python voice_qa_app.py
```

### Component Testing
Run individual component tests:
```bash
# Test speech-to-text
python speech_to_text.py

# Test text-to-speech
python text_to_speech.py

# Test Q&A processor
python qa_processor.py
```

## How It Works

1. **Listen**: Records your voice using the microphone
2. **Transcribe**: Converts speech to text using Whisper
3. **Process**: Sends question to OpenAI GPT for intelligent response
4. **Speak**: Converts AI response to speech and plays it back

## Configuration Options

### Whisper Model Sizes
- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: Better accuracy
- `medium`: High accuracy
- `large`: Best accuracy, slowest

### Voice Settings
Modify `text_to_speech.py` to adjust:
- Speech rate
- Volume
- Voice selection

## Example Interaction

```
🎤 Recording for 5 seconds... Speak now!
📝 Transcribed: 'What is machine learning?'
🧠 Processing your question...
🤖 Response: Machine learning is a branch of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed...
🔊 Speaking: [AI response converted to speech]
```

## Troubleshooting

### Audio Issues
- Ensure microphone permissions are granted
- Check system audio settings
- Try different Whisper model sizes

### OpenAI API Issues
- Verify API key is set correctly
- Check API quota/billing
- App works with fallback responses if API unavailable

### Dependencies
If installation fails, try:
```bash
# For audio libraries on Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# For macOS
brew install portaudio
```

## Commands

While running the app, you can say:
- "quit", "exit", "stop", or "bye" to end the session
- Any question or statement for AI response
- Use Ctrl+C to force quit

## Files Structure

- `voice_qa_app.py`: Main application
- `speech_to_text.py`: Whisper integration
- `text_to_speech.py`: TTS functionality  
- `qa_processor.py`: OpenAI API integration
- `requirements.txt`: Python dependencies

## License

Open source - feel free to modify and use as needed!