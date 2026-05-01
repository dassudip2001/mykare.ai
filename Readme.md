# MyKare

MyKare is a multi-service application built with LiveKit for real-time voice AI interactions. It consists of backend services, frontend interfaces, and LiveKit agent components for voice-enabled AI assistants.

## Project Structure

This repository contains several interconnected services:

- **`backend/`**: Python-based backend service (placeholder for API or additional logic).
- **`frontend/`**: Next.js frontend application.
- **`livekit-be/`**: LiveKit Agents backend for Python, providing voice AI capabilities.
- **`livekit-fe/`**: React frontend with LiveKit Agents UI components for voice interactions.

## Features

- **Voice AI Assistant**: Powered by LiveKit Agents with support for real-time voice interactions.
- **Multiple Frontends**: Separate interfaces for different use cases (Next.js and React with Agents UI).
- **Modular Architecture**: Backend and frontend services can be deployed independently.
- **LiveKit Integration**: Utilizes LiveKit for media streaming, agent orchestration, and observability.
- **Customizable UI**: Includes various audio visualizers, themes, and UI components.

## Getting Started

### Prerequisites

- Node.js (for frontend services)
- Python 3.8+ (for backend services)
- LiveKit Cloud account (for voice AI features)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mykare
   ```

2. Set up each service:

#### Backend

```bash
cd backend
pip install -r requirements.txt  # If dependencies exist
python main.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### LiveKit Backend (livekit-be)

```bash
cd livekit-be
pip install -e .
# Configure LiveKit credentials
python src/agent.py
```

#### LiveKit Frontend (livekit-fe)

```bash
cd livekit-fe
npm install
npm run dev
```

### Environment Setup

For LiveKit services, ensure you have:

- LiveKit API key and secret
- OpenAI API key (for inference)
- Cartesia API key (for TTS)
- Deepgram API key (for STT)

## Usage

1. Start the LiveKit backend agent.
2. Launch the frontend interfaces.
3. Connect to a LiveKit room for voice interactions.

## Development

- Use the provided Dockerfiles for containerized deployment.
- Refer to individual service READMEs for detailed setup and customization.

## Contributing

Contributions are welcome! Please read the contributing guidelines for each service.

## License

This project is licensed under the MIT License - see the LICENSE files in each service directory for details.
