import os
import base64

secret_key = base64.urlsafe_b64encode(os.urandom(24))
print(secret_key.decode('utf-8'))
