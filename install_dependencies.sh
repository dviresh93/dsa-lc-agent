#!/bin/bash

echo "🔧 Installing system dependencies for Voice Q&A App..."
echo "=================================================="

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install ffmpeg (required by Whisper)
echo "🎵 Installing ffmpeg..."
sudo apt install -y ffmpeg

# Install ALSA utilities (for audio recording)
echo "🎤 Installing ALSA utilities..."
sudo apt install -y alsa-utils

# Test audio recording
echo "🧪 Testing audio recording..."
echo "This will test your microphone for 2 seconds..."
echo "Say something when prompted:"

arecord -d 2 -f S16_LE -r 16000 -c 1 /tmp/test_audio.wav
echo "✅ Audio test completed!"

# Test if ffmpeg is working
echo "🧪 Testing ffmpeg..."
ffmpeg -version | head -1

echo ""
echo "✅ All dependencies installed successfully!"
echo ""
echo "Now you can run the voice app with:"
echo "  source venv/bin/activate"
echo "  python3 voice_qa_app.py"