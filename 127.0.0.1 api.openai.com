127.0.0.1   api.openai.com
127.0.0.1   oai.hf.space
127.0.0.1   openaiapi-site.azureedge.net
127.0.0.1   api.anthropic.com
OPENAI_API_BASE=http://127.0.0.1:8001/v1
OPENAI_API_KEY=local-ai-key
FORCE_LOCAL_AI=true
LOCAL_AI_ENDPOINT=http://127.0.0.1:8001/v1
ZOMBIECODER_HOST=http://127.0.0.1:12345
OLLAMA_HOST=http://127.0.0.1:11434
AI_PROVIDER=zombiecoder
AI_MODEL=local-llama
EDITOR_MODE=local_ai