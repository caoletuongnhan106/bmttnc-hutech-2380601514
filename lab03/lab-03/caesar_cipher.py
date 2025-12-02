import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        
        # Bắt sự kiện click chuột vào nút
        self.uic.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.uic.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        # Đường dẫn API (Lưu ý: Lab 2 phải đang chạy)
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        
        # Lấy dữ liệu từ giao diện
        payload = {
            "plain_text": self.uic.txt_plain_text.text(),
            "key": int(self.uic.txt_key.text())
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Hiển thị kết quả lên ô Cipher Text
                self.uic.txt_cipher_text.setText(data['encrypted_message'])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.uic.txt_cipher_text.text(),
            "key": int(self.uic.txt_key.text())
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.uic.txt_plain_text.setText(data['decrypted_message'])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_())