from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import secrets
'''
Using RSA (asymmetric) and AES (symmetric) encryption
'''


# Using a class
class Encryption:
    # initiallising class
    def __init__(self, key_size: int = 2048):
        # RSA keypair for key exchange
        self.private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = key_size
        )
        self.public_key = self.private_key.public_key()

        # AES session key (None until exchanged)
        self.session_key = None

# RSA Functions

    def get_public_key_bytes(self) -> bytes:
        # return PEM encoded public key bytes
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def load_peer_public_key(self, pem_bytes: bytes):
        # Load and return the peer's public key from PEM bytes
        return serialization.load_pem_public_key(pem_bytes)

    def encrypt_for_peer(self, peer_public_key, data: bytes) -> bytes:
        # Encrypt data (like a session key) with the peer's public key
        return peer_public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_with_private(self, ciphertext: bytes) -> bytes:
        # Decrypt RSA-encrypted data (like a session key)
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

# AES functions

    def create_session_key(self):
        # Generate a new AES-256 session key
        self.session_key = secrets.token_bytes(32)
        return self.session_key

    def set_session_key(self, key: bytes):
        # Set an externally provided session key (from peer)
        self.session_key = key

    def encrypt_message(self, message: str) -> str:
        # Encrypts a message using AES-GCM with the current session key
        if self.session_key is None:
            raise ValueError("Session key not set!")
        aesgcm = AESGCM(self.session_key)
        nonce = secrets.token_bytes(12)
        ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
        return f"{nonce.hex()}:{ciphertext.hex()}"

    def decrypt_message(self, encrypted: str) -> str:
        # Decrypts AES-GCM encrypted message
        if self.session_key is None:
            raise ValueError("Session key not set!")
        aesgcm = AESGCM(self.session_key)
        nonce_hex, ct_hex = encrypted.split(":")
        nonce = bytes.fromhex(nonce_hex)
        ciphertext = bytes.fromhex(ct_hex)
        return aesgcm.decrypt(nonce, ciphertext, None).decode()