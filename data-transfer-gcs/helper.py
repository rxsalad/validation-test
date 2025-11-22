import os
import subprocess
import time
from dotenv import load_dotenv
load_dotenv()

# Access to DO Spaces
GCS_JSON_FILE = os.getenv("GCS_JSON_FILE", "")
GCS_REGION    = os.getenv("GCS_REGION", "")


# Create the configuration file for rclone
# https://developers.cloudflare.com/r2/examples/rclone/
filename = os.path.expanduser("~")+"/.config/rclone/rclone.conf"
with open(filename,'w') as f:
    f.write("[gcs]\n")
    f.write("type = google cloud storage\n")
    f.write("service_account_file = {}\n".format(GCS_JSON_FILE))
    f.write("region = {}\n".format(GCS_REGION))
    f.write("no_acl = true")


# upload_local_to_cloud
def Uploader(source, bucket, target, chunk_size_mbype="10M", concurrency="10"):    
    cmd = f'rclone copyto {source} gcs:{bucket}/{target} --s3-chunk-size={chunk_size_mbype} --transfers={concurrency} --ignore-times'
    try:                                      
        subprocess.run(cmd, shell=True, check=True, stderr=subprocess.PIPE)
        print(cmd, flush=True)
    except subprocess.CalledProcessError as e:
        print(f"The error message: {e}", flush=True)



