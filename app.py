from flask import Flask, render_template, request
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
from dotenv import load_dotenv

# key = get_random_bytes(32)
key=os.getenv("key")

# Encrypt a string
def encrypt_string(plain_text: str, key: bytes) -> str:
    # Convert text to bytes
    data = plain_text.encode('utf-8')
    
    # Create AES cipher in GCM mode (generates a random nonce automatically)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # Pack nonce, tag, and ciphertext together, then encode in Base64 for a safe string representation
    result = base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
    return result

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get the number from the form and convert it to float or int
        user_input = request.form.get("text")
        if user_input:
            text = user_input
            result = encrypt_string(text, key)
            
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)