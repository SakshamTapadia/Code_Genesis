# Code Genesis AI Assistant

Deployed Model Link : [ (https://codegenesis.streamlit.app/) ]
## Description
Companion is an AI assistant built using Streamlit that helps users with coding, debugging, and other technical tasks. It allows users to select from various AI models and adjust the creativity level of the responses.

The application features three specialized models:
- **deepseek-r1:1.5b**: Expert in code, debugging, documentation, and solution architecture
- **deepseek-coder:1.3b**: Specialized in code generation, algorithm optimization, and performance tuning
- **medllama2**: Focused on medical knowledge and biomedical research analysis

## Features
- **Multiple Model Selection**: Choose between different AI models each with unique capabilities
- **Adjustable Creativity Levels**: Fine-tune the AI's response style from strict factual (0.0) to highly creative (0.9)
- **Interactive Chat Interface**: User-friendly chat interface with model-specific styling
- **Persistent Chat History**: Maintains conversation context throughout the session
- **Custom Styling**: Dark theme with model-specific gradient backgrounds for chat messages

## Installation

### Install Ollama
1. Follow the instructions on the [Ollama website](https://ollama.com/docs/installation) to install Ollama on your local machine.

2. After installation, start the Ollama server:
```bash
ollama serve
```

### Install Models
1. Download the required models using the following commands:
```bash
ollama pull deepseek-r1:1.5b
ollama pull deepseek-coder:1.3b
ollama pull medllama2
```

### Clone the Repository
1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the project directory:
```bash
cd <project-directory>
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
1. Start the application:
```bash
streamlit run app2.py
```

2. Configure the AI assistant:
   - Select a model from the sidebar
   - Adjust the creativity level using the slider
   - Each creativity level has specific use cases described in the sidebar

3. Start chatting:
   - Type your questions in the chat input
   - Receive AI responses with model-specific styling

## Dependencies
- streamlit
- langchain_ollama
- langchain_core

## System Requirements
- Local Ollama server running on http://localhost:11434
- Python 3.6 or higher

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License.
