# src/encryption.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
import os

def aes_encrypt(data: str, key: bytes):
    try:
        if not data:
            raise ValueError("Data cannot be empty.")
        if len(key) < 16:
            raise ValueError("Key must be at least 16 bytes long.")
        
        key = key.ljust(32, b'\0')[:32]  # Ensure key is 256 bits
        iv = os.urandom(16)  # Generate a random IV (Initialization Vector)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return iv + encrypted_data  # Return IV + encrypted data
    except ValueError as ve:
        print(f"Validation Error: {ve}")
        raise
    except Exception as e:
        print(f"Error during encryption: {e}")
        raise

def aes_decrypt(encrypted_data: bytes, key: bytes):
    try:
        if not encrypted_data:
            raise ValueError("Encrypted data cannot be empty.")
        if len(key) < 16:
            raise ValueError("Key must be at least 16 bytes long.")
        
        key = key.ljust(32, b'\0')[:32]  # Ensure key is 256 bits

        iv = encrypted_data[:16]  # Extract the IV
        encrypted_data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted_data) + unpadder.finalize()  # Return decrypted data
    except ValueError as ve:
        print(f"Validation Error: {ve}")
        raise
    except Exception as e:
        print(f"Error during decryption: {e}")
        raise

def generate_rsa_keys():
    """Generate RSA private and public keys."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt_key(aes_key: bytes, public_key):
    """Encrypt AES key using RSA public key."""
    return public_key.encrypt(
        aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt_key(encrypted_key: bytes, private_key):
    """Decrypt AES key using RSA private key."""
    return private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def aes_rsa_hybrid_encrypt(data: str, aes_key: bytes, public_key):
    """Encrypt data using AES and encrypt AES key using RSA."""
    try:
        if len(aes_key) < 16:
            aes_key = aes_key.ljust(16, b'\0')  # Ensure AES key is at least 16 bytes long
        aes_encrypted_data = aes_encrypt(data, aes_key)
        rsa_encrypted_key = rsa_encrypt_key(aes_key, public_key)
        return rsa_encrypted_key + aes_encrypted_data  # Concatenate RSA-encrypted key and AES-encrypted data
    except Exception as e:
        print(f"Error during hybrid encryption: {e}")
        raise

def aes_rsa_hybrid_decrypt(encrypted_data: bytes, private_key):
    """Decrypt data using RSA for the AES key and AES for the data."""
    try:
        rsa_encrypted_key = encrypted_data[:256]  # RSA-encrypted key is 256 bytes
        aes_encrypted_data = encrypted_data[256:]  # Remaining is AES-encrypted data

        aes_key = rsa_decrypt_key(rsa_encrypted_key, private_key)
        return aes_decrypt(aes_encrypted_data, aes_key)
    except Exception as e:
        print(f"Error during hybrid decryption: {e}")
        raise
