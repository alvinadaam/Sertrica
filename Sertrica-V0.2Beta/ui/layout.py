# ui/layout.py

import sys
import os

# Add the src directory to the Python module search path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
if src_path not in sys.path:
    sys.path.append(src_path)

if __name__ == "__main__" and __package__ is None:
    # Adjust the module search path for direct execution
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
from encryption import aes_encrypt, aes_decrypt, aes_rsa_hybrid_encrypt, aes_rsa_hybrid_decrypt, generate_rsa_keys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from ui.layoutParts.styles import set_dark_theme  # Use absolute import for set_dark_theme

class SertricaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setup_connections()
        self.setup_styles()
        self.toggle_rsa_key_management()  # Initialize visibility of RSA key management
        self.private_key = None
        self.public_key = None

    def load_ui(self):
        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), 'main_window.ui')
        loadUi(ui_path, self)

        # Set window properties
        self.setWindowTitle("SERTRICA")
        self.resize(800, 600)

    def setup_connections(self):
        # Connect buttons to their respective methods
        self.encrypt_btn.clicked.connect(self.encrypt_data)
        self.decrypt_btn.clicked.connect(self.decrypt_data)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.clear_btn.clicked.connect(self.clear_inputs)
        self.file_btn.clicked.connect(self.upload_file)
        self.copy_encrypted.clicked.connect(self.copy_encrypted_text)
        self.copy_decrypted.clicked.connect(self.copy_decrypted_text)
        self.save_encrypted_btn.clicked.connect(self.save_encrypted_to_file)
        self.save_decrypted_btn.clicked.connect(self.save_decrypted_to_file)
        self.generate_rsa_keys_btn.clicked.connect(self.generate_rsa_keys)
        self.import_rsa_keys_btn.clicked.connect(self.import_rsa_keys)
        self.export_rsa_keys_btn.clicked.connect(self.export_rsa_keys)
        self.encryption_type.currentIndexChanged.connect(self.toggle_rsa_key_management)

    def clear_inputs(self):
        # Clear input fields
        self.text_input.clear()
        self.key_input.clear()
        self.encrypted_output.clear()
        self.decrypted_output.clear()
        self.error_label.clear()
        self.progress.hide()

    def encrypt_data(self):
        # Encrypt the input data
        try:
            self.progress.show()
            self.progress.setValue(0)
            QTimer.singleShot(100, lambda: self.progress.setValue(50))  # Simulate progress

            data = self.text_input.toPlainText()
            key = self.key_input.text().encode('utf-8')
            mode = self.encryption_type.currentText()

            if mode == "AES":
                encrypted_data = aes_encrypt(data, key)
                self.encrypted_output.setPlainText(encrypted_data.hex())
                self.error_label.clear()
            elif mode == "AES+RSA Hybrid":
                if not self.private_key or not self.public_key:
                    raise ValueError("RSA keys are not generated or imported.")
                encrypted_data = aes_rsa_hybrid_encrypt(data, key, self.public_key)
                self.encrypted_output.setPlainText(encrypted_data.hex())
                self.error_label.clear()

            QTimer.singleShot(200, lambda: self.progress.setValue(100))  # Simulate progress
        except Exception as e:
            self.error_label.setText(f"Encryption failed: {str(e)}")
            self.log_error(e)

    def decrypt_data(self):
        # Decrypt the input data
        try:
            self.progress.show()
            self.progress.setValue(0)
            QTimer.singleShot(100, lambda: self.progress.setValue(50))  # Simulate progress

            encrypted_text = self.text_input.toPlainText()
            if not encrypted_text.strip():
                raise ValueError("Encrypted data cannot be empty.")

            key = self.key_input.text().encode('utf-8')
            mode = self.encryption_type.currentText()

            if mode == "AES":
                encrypted_data = bytes.fromhex(encrypted_text)
                decrypted_data = aes_decrypt(encrypted_data, key)
                self.decrypted_output.setPlainText(decrypted_data.decode())
                self.error_label.clear()
            elif mode == "AES+RSA Hybrid":
                if not self.private_key:
                    raise ValueError("Private RSA key is not available.")
                encrypted_data = bytes.fromhex(encrypted_text)
                decrypted_data = aes_rsa_hybrid_decrypt(encrypted_data, self.private_key)
                self.decrypted_output.setPlainText(decrypted_data.decode())
                self.error_label.clear()

            QTimer.singleShot(200, lambda: self.progress.setValue(100))  # Simulate progress
        except Exception as e:
            self.error_label.setText(f"Error during decryption: {str(e)}")
            self.log_error(e)

    def upload_file(self):
        # Upload a file and load its contents into the text input
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_input.setPlainText(file.read())
            except Exception as e:
                self.error_label.setText(f"Error loading file: {str(e)}")
                self.log_error(e)

    def save_encrypted_to_file(self):
        # Save the encrypted output to a file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.encrypted_output.toPlainText())
            except Exception as e:
                self.error_label.setText(f"Error saving file: {str(e)}")
                self.log_error(e)

    def save_decrypted_to_file(self):
        # Save the decrypted output to a file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.decrypted_output.toPlainText())
            except Exception as e:
                self.error_label.setText(f"Error saving file: {str(e)}")
                self.log_error(e)

    def log_error(self, error):
        # Log errors to a file
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{str(error)}\n")

    def copy_encrypted_text(self):
        # Copy encrypted text to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.encrypted_output.toPlainText())

    def copy_decrypted_text(self):
        # Copy decrypted text to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.decrypted_output.toPlainText())

    def toggle_theme(self):
        # Toggle between light and dark themes
        if self.styleSheet():
            self.setStyleSheet("")  # Switch to light theme
        else:
            set_dark_theme(self)  # Use the imported function

    def setup_styles(self):
        # Set the default style for the application
        set_dark_theme(self)  # Use the imported function

    def generate_rsa_keys(self):
        # Generate RSA keys and display them in the UI
        try:
            self.private_key, self.public_key = generate_rsa_keys()
            self.public_key_field.setPlainText(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()
            )
            self.private_key_field.setPlainText(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode()
            )
            self.error_label.clear()
        except Exception as e:
            self.error_label.setText(f"Error generating RSA keys: {str(e)}")
            self.log_error(e)

    def import_rsa_keys(self):
        # Import RSA keys from files
        try:
            private_key_path, _ = QFileDialog.getOpenFileName(self, "Open Private Key", "", "PEM Files (*.pem);;All Files (*)")
            public_key_path, _ = QFileDialog.getOpenFileName(self, "Open Public Key", "", "PEM Files (*.pem);;All Files (*)")
            if private_key_path and public_key_path:
                with open(private_key_path, 'rb') as priv_file:
                    self.private_key = serialization.load_pem_private_key(
                        priv_file.read(),
                        password=None,
                        backend=default_backend()
                    )
                with open(public_key_path, 'rb') as pub_file:
                    self.public_key = serialization.load_pem_public_key(
                        pub_file.read(),
                        backend=default_backend()
                    )
                self.error_label.clear()
        except Exception as e:
            self.error_label.setText(f"Error importing RSA keys: {str(e)}")
            self.log_error(e)

    def export_rsa_keys(self):
        # Export RSA keys to files
        try:
            private_key_path, _ = QFileDialog.getSaveFileName(
                self, "Save Private Key", "private_key.pem", "PEM Files (*.pem);;All Files (*)"
            )
            public_key_path, _ = QFileDialog.getSaveFileName(
                self, "Save Public Key", "public_key.pem", "PEM Files (*.pem);;All Files (*)"
            )
            if private_key_path:
                with open(private_key_path, 'wb') as priv_file:
                    priv_file.write(
                        self.private_key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.NoEncryption()
                        )
                    )
            if public_key_path:
                with open(public_key_path, 'wb') as pub_file:
                    pub_file.write(
                        self.public_key.public_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                        )
                    )
            if private_key_path or public_key_path:
                self.error_label.setText("RSA keys exported successfully.")
            else:
                self.error_label.setText("Export canceled.")
        except Exception as e:
            self.error_label.setText(f"Error exporting RSA keys: {str(e)}")
            self.log_error(e)

    def toggle_rsa_key_management(self):
        # Show or hide RSA key management section based on encryption type
        if self.encryption_type.currentText() == "AES":
            self.rsa_key_group.hide()
        else:
            self.rsa_key_group.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SertricaUI()
    ex.show()
    sys.exit(app.exec_())