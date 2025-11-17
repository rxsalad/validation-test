mkdir -p /result/$FOLDER

#################### vLLM Server - Background

VLLM_USE_V1=1 vllm serve $MODEL \
 --enforce-eager \
 --host 0.0.0.0 \
 --port 8000 \
 --tensor-parallel-size 8 \
 --seed 1024 \
 --dtype float16 \
 --max-model-len 10000 \
 --max-num-batched-tokens 10000 \
 --max-num-seqs 256 \
 --trust-remote-code \
 --gpu-memory-utilization 0.9 > /result/$FOLDER/vllm_server_${NODE_NAME}.log 2>&1 &

#################### Test Client

python3 test.py > /result/$FOLDER/client_${NODE_NAME}.log 2>&1
