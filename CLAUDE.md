# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based English conversation practice application that uses OpenAI's GPT-4 and audio APIs to provide interactive language learning experiences. The app supports three practice modes:
- **日常英会話 (Daily Conversation)**: Free-form conversation practice with grammatical corrections
- **シャドーイング (Shadowing)**: Listen and repeat exercises with evaluation
- **ディクテーション (Dictation)**: Listen and transcribe exercises with accuracy assessment

## Development Commands

### Running the Application
```bash
streamlit run main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### System Dependencies
The application requires audio processing libraries:
- `ffmpeg` - for audio format conversion
- `portaudio19-dev` - for PyAudio to work with microphone input

## Architecture

### Core Components

**main.py** (287 lines)
- Entry point and UI orchestration
- Manages session state for all three practice modes
- Handles user interactions and mode switching
- Controls audio recording/playback flow

**functions.py** (199 lines)
- Audio processing utilities (recording, transcription, playback)
- LangChain conversation chain creation
- Problem generation and evaluation logic
- Key functions:
  - `record_audio()`: Captures user voice input
  - `transcribe_audio()`: Converts speech to text using Whisper
  - `play_wav()`: Plays audio with variable speed control
  - `create_chain()`: Sets up LangChain conversation chains
  - `create_problem_and_play_audio()`: Generates and plays practice problems
  - `create_evaluation()`: Evaluates user responses

**constants.py** (55 lines)
- Configuration constants and prompt templates
- Three main prompt templates:
  - `SYSTEM_TEMPLATE_BASIC_CONVERSATION`: English tutor persona
  - `SYSTEM_TEMPLATE_CREATE_PROBLEM`: Problem generation (15-word sentences)
  - `SYSTEM_TEMPLATE_EVALUATION`: Japanese evaluation feedback

### Key Technologies

- **Frontend**: Streamlit for web UI
- **LLM Integration**: LangChain with OpenAI GPT-4o-mini
- **Audio Processing**: 
  - OpenAI Whisper for speech-to-text
  - OpenAI TTS for text-to-speech
  - PyAudio/pydub for audio manipulation
  - WebRTC for real-time audio streaming
- **Memory Management**: ConversationSummaryBufferMemory (1000 token limit)

### Session State Management

The app maintains extensive session state for:
- Message history and conversation memory
- Mode-specific flags (shadowing_flg, dictation_flg, etc.)
- Audio processing state
- OpenAI API client instances
- LangChain conversation chains

### Audio Flow

1. User speaks → `audiorecorder` component captures audio
2. Audio saved as WAV → Whisper API transcribes to text
3. Text sent to GPT-4 → Response generated
4. Response converted to speech → TTS API creates audio
5. Audio played back with adjustable speed (0.6x to 2.0x)

## Environment Configuration

Requires `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

## Directory Structure

- `audio/input/`: Temporary storage for recorded user audio
- `audio/output/`: Temporary storage for generated AI audio
- `images/`: User and AI avatar icons
- `.streamlit/`: Streamlit configuration (currently empty config.toml)