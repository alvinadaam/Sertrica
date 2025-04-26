# tests/test_encryption.py

import sys
import os

# Add the src directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from encryption import aes_encrypt, aes_decrypt

def test_encryption():
    # Test data and key
    data = "Hello, SERTRICA!"
    key = b"mysecretkey123456"  # Example 16-byte key (should be 256-bit for AES-256)

    # Encrypt the data
    encrypted_data = aes_encrypt(data, key)
    print(f"Encrypted Data: {encrypted_data.hex()}")  # Print encrypted data in hex

    # Decrypt the data
    decrypted_data = aes_decrypt(encrypted_data, key)
    print(f"Decrypted Data: {decrypted_data.decode()}")  # Print decrypted data as string
    
    # Test if encryption-decryption cycle is correct
    assert data == decrypted_data.decode(), "Decryption failed!"
    print("Encryption and Decryption passed!")

# Run the test
test_encryption()
