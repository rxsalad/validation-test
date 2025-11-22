import time
import requests
import os
import threading
from helper import Uploader


URL     = "http://localhost:8000/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}
MODEL   = os.getenv("MODEL", "meta-llama/Llama-3.2-1B-Instruct")

INPUT_PROMPT = "Who are you? Please tell me how to learn AI and ML, using 1000+ words"
PAYLOAD = { "model": MODEL, "messages": [{"role": "user", "content": INPUT_PROMPT}] }


# Access to DO Spaces
BUCKET    = os.getenv("BUCKET", "")
FOLDER    = os.getenv("FOLDER", "")
NODE_NAME = os.getenv("NODE_NAME", "")


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


# Wait until vLLM server is ready.
# Many instances running concurrently may generate too many model download requests, which could be throttled by Hugging Face.
# Improvement: if the vLLM server fails due to model download issues, restart the pod after some time.
# Or run 10 instances every 10 minutes (for Llama 3 8B).
if not check_vllm_ready():
    # Restart the pod
    time.sleep(1000000)
    

# Inference function
def run_inference():
    
    while True:
        try:
            response = requests.post(URL, json=PAYLOAD, headers=HEADERS, timeout=600)

            if response.status_code == 200:
                data = response.json()
                tokens = data.get('usage', {}).get('total_tokens', 'N/A')
                print(f"Success, tokens returned: {tokens}", flush=True)
            else:
                print(f"Failed with status code {response.status_code}", flush=True)

        except requests.RequestException as e:
            print(f"Error: {e}", flush=True)

        time.sleep(2)


# Create and start a thread
inference_thread = threading.Thread(target=run_inference, daemon=True)
inference_thread.start()

# Main thread can continue doing other things
print("Inference thread started and running in the background...")

# Upload log file every 10 minutes
while True:
    Uploader(f"vllm_server.log", BUCKET, f"{FOLDER}/{NODE_NAME}.log")    
    time.sleep(600)