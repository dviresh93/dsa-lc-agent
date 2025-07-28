import whisper
import subprocess
import tempfile
import os
import time
from typing import Optional

class SpeechToText:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the Speech-to-Text engine using system audio tools
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        
        # Check if we have arecord (ALSA) available
        self.audio_tool = self._detect_audio_tool()
        if not self.audio_tool:
            raise RuntimeError("No suitable audio recording tool found. Please install alsa-utils or pulseaudio-utils.")
        
        print(f"Using audio tool: {self.audio_tool}")
        print("Whisper model and audio system ready!")
    
    def _detect_audio_tool(self):
        """Detect available audio recording tools"""
        tools = [
            ("arecord", ["arecord", "--version"]),
            ("parecord", ["parecord", "--version"]),
            ("sox", ["sox", "--version"])
        ]
        
        for tool_name, test_cmd in tools:
            try:
                subprocess.run(test_cmd, capture_output=True, check=True, timeout=5)
                return tool_name
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        return None
    
    def record_audio(self, duration: int = 5, sample_rate: int = 16000) -> str:
        """
        Record audio using system tools and return transcribed text
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
        print(f"🎤 Recording for {duration} seconds... Speak now!")
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_filename = tmp_file.name
            
            # Record audio using system tools
            if self.audio_tool == "arecord":
                cmd = [
                    "arecord",
                    "-f", "S16_LE",
                    "-r", str(sample_rate),
                    "-c", "1",
                    "-d", str(duration),
                    temp_filename
                ]
            elif self.audio_tool == "parecord":
                cmd = [
                    "parecord",
                    "--format=s16le",
                    f"--rate={sample_rate}",
                    "--channels=1",
                    temp_filename
                ]
            elif self.audio_tool == "sox":
                cmd = [
                    "sox",
                    "-d",
                    "-r", str(sample_rate),
                    "-c", "1",
                    "-b", "16",
                    temp_filename,
                    "trim", "0", str(duration)
                ]
            else:
                raise RuntimeError(f"Unsupported audio tool: {self.audio_tool}")
            
            # Start recording
            if self.audio_tool == "parecord":
                # parecord doesn't have duration option, so we need to timeout
                process = subprocess.Popen(cmd)
                time.sleep(duration)
                process.terminate()
                process.wait()
            else:
                subprocess.run(cmd, check=True, timeout=duration + 5)
            
            print("✅ Recording completed!")
            
            # Check if file exists and has content
            if not os.path.exists(temp_filename) or os.path.getsize(temp_filename) == 0:
                print("❌ No audio recorded")
                return ""
            
            print("🔄 Transcribing audio...")
            # Transcribe using Whisper
            result = self.model.transcribe(temp_filename)
            transcribed_text = result["text"].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            print(f"📝 Transcribed: '{transcribed_text}'")
            return transcribed_text
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Audio recording failed: {e}")
            return ""
        except subprocess.TimeoutExpired:
            print("❌ Recording timeout")
            return ""
        except Exception as e:
            print(f"❌ Error during recording/transcription: {e}")
            return ""
    
    def record_audio_manual(self) -> str:
        """
        Manual recording mode - user controls when to start/stop
        
        Returns:
            Transcribed text
        """
        print("🎤 Manual recording mode")
        print("Press Enter to START recording...")
        input()
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_filename = tmp_file.name
            
            # Start recording in background
            if self.audio_tool == "arecord":
                cmd = [
                    "arecord",
                    "-f", "S16_LE",
                    "-r", "16000",
                    "-c", "1",
                    temp_filename
                ]
            elif self.audio_tool == "parecord":
                cmd = [
                    "parecord",
                    "--format=s16le",
                    "--rate=16000",
                    "--channels=1",
                    temp_filename
                ]
            elif self.audio_tool == "sox":
                cmd = [
                    "sox",
                    "-d",
                    "-r", "16000",
                    "-c", "1",
                    "-b", "16",
                    temp_filename
                ]
            
            print("🔴 Recording started... Press Enter to STOP")
            process = subprocess.Popen(cmd)
            
            # Wait for user to stop
            input()
            
            # Stop recording
            process.terminate()
            process.wait()
            
            print("✅ Recording stopped!")
            
            # Check if file exists and has content
            if not os.path.exists(temp_filename) or os.path.getsize(temp_filename) == 0:
                print("❌ No audio recorded")
                return ""
            
            print("🔄 Transcribing audio...")
            # Transcribe using Whisper
            result = self.model.transcribe(temp_filename)
            transcribed_text = result["text"].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            print(f"📝 Transcribed: '{transcribed_text}'")
            return transcribed_text
            
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
        stt = SpeechToText(model_size="tiny")  # Use tiny for faster testing
        
        print("Testing Speech-to-Text...")
        print("Choose recording mode:")
        print("1. Automatic (5 seconds)")
        print("2. Manual (press Enter to start/stop)")
        
        choice = input("Enter choice (1-2) [1]: ").strip() or "1"
        
        if choice == "2":
            text = stt.record_audio_manual()
        else:
            text = stt.record_audio(duration=5)
        
        print(f"Final result: '{text}'")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("- Make sure you have a microphone connected")
        print("- Install audio tools: sudo apt install alsa-utils")
        print("- Check microphone permissions")