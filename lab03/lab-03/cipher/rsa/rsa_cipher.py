import rsa
import os

class RSACipher:
    def __init__(self):
        # Tạo thư mục chứa key ngay tại thư mục hiện tại
        self.keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)

    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        with open(os.path.join(self.keys_dir, 'publicKey.pem'), 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open(os.path.join(self.keys_dir, 'privateKey.pem'), 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))
        return "Keys generated successfully"

    def load_keys(self):
        try:
            with open(os.path.join(self.keys_dir, 'publicKey.pem'), 'rb') as p:
                public_key = rsa.PublicKey.load_pkcs1(p.read())
            with open(os.path.join(self.keys_dir, 'privateKey.pem'), 'rb') as p:
                private_key = rsa.PrivateKey.load_pkcs1(p.read())
            return public_key, private_key
        except Exception as e:
            print(f"Error loading keys: {e}")
            return None, None

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('utf-8'), key).hex()

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(bytes.fromhex(ciphertext), key).decode('utf-8')
        except:
            return "Decryption Failed"

    def sign(self, message, key):
        return rsa.sign(message.encode('utf-8'), key, 'SHA-1').hex()

    def verify(self, message, signature, key):
        try:
            return rsa.verify(message.encode('utf-8'), bytes.fromhex(signature), key) == 'SHA-1'
        except:
            return False