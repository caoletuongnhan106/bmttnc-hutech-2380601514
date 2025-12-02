from flask import Flask, request, jsonify
from cipher.rsa import RSACipher # Import module RSA vừa làm

app = Flask(__name__)

# Khởi tạo đối tượng RSA
rsa_cipher = RSACipher()

# API 1: Tạo cặp khóa (Public/Private)
@app.route('/api/rsa/generate_keys', methods=['GET'])
def generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

# API 2: Mã hóa (Encrypt)
@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data['message']
    key_type = data['key_type'] # 'public' hoặc 'private'
    
    # Load khóa từ file
    public_key, private_key = rsa_cipher.load_keys()

    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})
        
    encrypted_message = rsa_cipher.encrypt(message, key)
    return jsonify({'encrypted_message': encrypted_message})

# API 3: Giải mã (Decrypt)
@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key_type = data['key_type']
    
    public_key, private_key = rsa_cipher.load_keys()
    
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type'})
        
    decrypted_message = rsa_cipher.decrypt(ciphertext, key)
    return jsonify({'decrypted_message': decrypted_message})

# API 4: Ký tên (Sign)
@app.route('/api/rsa/sign', methods=['POST'])
def sign():
    data = request.json
    message = data['message']
    
    public_key, private_key = rsa_cipher.load_keys()
    
    # Ký bằng Private Key
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature})

# API 5: Xác thực (Verify)
@app.route('/api/rsa/verify', methods=['POST'])
def verify():
    data = request.json
    message = data['message']
    signature = data['signature']
    
    public_key, private_key = rsa_cipher.load_keys()
    
    # Xác thực bằng Public Key
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# Chạy Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)