import time
import requests
from helper import *


URL     = "http://localhost:8000/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}
MODEL   = os.getenv("MODEL", "meta-llama/Llama-3.2-1B-Instruct")


# Health Check
HEALTH_ENDPOINT = f"http://0.0.0.0:8000/health"  # some vLLM endpoints may have /health
RETRY_INTERVAL = 5  # seconds
MAX_RETRIES = 600   # try for up to 50 minutes

def check_vllm_ready():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=2)
            if response.status_code == 200:
                print("vLLM server is ready!", flush=True)
                return True
        except requests.RequestException:
            pass  # server not ready yet

        print(f"Attempt {attempt}: vLLM server not ready, retrying in {RETRY_INTERVAL}s...", flush=True)
        time.sleep(RETRY_INTERVAL)

    print("vLLM server did not become ready within the timeout period.", flush=True)
    return False


if not check_vllm_ready():
    time.sleep(1000000)


# Inference Test
INPUT_PROMPT = "Who are you? Please tell me how to learn AI and ML, using 1000+ words"
PAYLOAD = {
    "model": MODEL,
    "messages": [{"role": "user", "content": INPUT_PROMPT}]
}

while True:
    try:
        response = requests.post(URL, json=PAYLOAD, headers=HEADERS, timeout=600)

        if response.status_code == 200:
            data = response.json()
            tokens = data.get('usage', {}).get('total_tokens', 'N/A')
            print(f"Success, tokens returned: {tokens}", flush=True)
        else:
            print(f"Failed", flush=True)

    except requests.RequestException as e:
        print(f"Error: {e}", flush=True)
    time.sleep(2)
