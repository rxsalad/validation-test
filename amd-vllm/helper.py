import os
from dotenv import load_dotenv
load_dotenv()

# Access to DO Spaces
SPACES_URL    = os.getenv("AWS_ENDPOINT_URL", "")
SPACES_REGION = os.getenv("AWS_REGION", "")
SPACES_ID     = os.getenv("AWS_ACCESS_KEY_ID", "")
SPACES_KEY    = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# Create the configuration file for rclone
# https://developers.cloudflare.com/r2/examples/rclone/
filename = os.path.expanduser("~")+"/.config/rclone/rclone.conf"
with open(filename,'w') as f:
    f.write("[ds]\n")
    f.write("type = s3\n")
    f.write("provider = DigitalOcean\n")
    f.write("access_key_id = {}\n".format(SPACES_ID))
    f.write("secret_access_key = {}\n".format(SPACES_KEY))
    f.write("region = {}\n".format(SPACES_REGION))
    f.write("endpoint = {}\n".format(SPACES_URL))
    f.write("bucket_acl = private")