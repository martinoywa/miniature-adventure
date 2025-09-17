## Thoughtful AI Support Agent

## How To Run
### Ollama Installation
1. Download Ollama: https://ollama.com/download
2. Download Models (Terminal/CMD):
```
$ ollama pull llama3.1
$ ollama pull nomic-embed-text
```

### Set Python Environment
1. Install Python 3.10: https://www.python.org/downloads/
2. Create and activate virtual environment:
``` Linux/MacOS
$ python3 -m venv env
$ . env/bin/activate
```
OR
``` Windows
$ python3 -m venv env
$ .\env\Scripts\Activate
```
3. Install Requirements:
```
$ pip install -r requirements.txt
```

### Run Application
```
$ streamlit run main.py
```
