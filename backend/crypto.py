"""Cryptographic primitives for keys and signatures."""

from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import hashlib
import base64


class Wallet:
    """Simple wallet with ECDSA key pair and signing capability."""

    def __init__(self):
        """Initialize empty wallet. Call generate_keypair() to create keys."""
        self.private_key = None
        self.public_key = None
        self.address = ""
        self._private_key_pem = ""
        self._public_key_pem = ""

    def generate_keypair(self):
        """
        Generate new ECDSA public/private key pair.

        Uses SECP256k1 curve (same as Bitcoin/Ethereum) for educational alignment.
        Keys are stored in PEM format for portability and readability.

        Returns:
            None (modifies self)
        """
        # Generate SECP256k1 private key (same curve as Bitcoin)
        self.private_key = ec.generate_private_key(ec.SECP256K1())

        # Derive public key from private key (automatic via elliptic curve math)
        self.public_key = self.private_key.public_key()

        # Serialize keys to PEM format (human-readable, standard format)
        self._private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        self._public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # Generate address from public key (hash of public key bytes)
        self.address = generate_address(self._public_key_pem)

    def sign(self, message: str) -> str:
        """
        Sign a message with private key using ECDSA.

        Creates a cryptographically secure signature that can be verified
        using only the message, signature, and public key.

        Args:
            message: The message to sign

        Returns:
            Signature as hex string
        """
        if not self.private_key:
            raise ValueError("Cannot sign without a private key. Call generate_keypair() first.")

        # Sign message using ECDSA with SHA256
        signature_bytes = self.private_key.sign(
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )

        # Convert to hex string for easy transmission/storage
        return signature_bytes.hex()

    @staticmethod
    def verify(message: str, signature: str, public_key_pem: str) -> bool:
        """
        Verify an ECDSA signature against a message and public key.

        This is real cryptographic verification - the signature can only be
        created by someone holding the private key corresponding to the public key.

        Args:
            message: The original message
            signature: The signature to verify (hex string)
            public_key_pem: Public key in PEM format

        Returns:
            True if signature is valid, False otherwise
        """
        if not signature or not public_key_pem:
            return False

        try:
            # Convert hex signature back to bytes
            signature_bytes = bytes.fromhex(signature)

            # Load public key from PEM format
            public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))

            # Verify signature using ECDSA
            public_key.verify(
                signature_bytes,
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )

            # If no exception raised, signature is valid
            return True

        except (ValueError, InvalidSignature):
            # Invalid signature format or verification failed
            return False

    def get_public_key_pem(self) -> str:
        """Get public key in PEM format for sharing."""
        return self._public_key_pem

    def get_private_key_pem(self) -> str:
        """Get private key in PEM format. Keep this secret!"""
        return self._private_key_pem


def generate_address(public_key_pem: str) -> str:
    """
    Generate address from public key.

    Uses simple hash of public key for educational purposes.
    Real systems use more complex derivation (e.g., Bitcoin's Base58Check).
    """
    # Hash the public key to create address
    return hashlib.sha256(public_key_pem.encode()).hexdigest()[:40]


class LetterEncryption:
    """RSA encryption for letters from past iterations."""

    def __init__(self):
        """Initialize encryption system. Call generate_keypair() to create keys."""
        self.private_key = None
        self.public_key = None
        self._private_key_pem = ""
        self._public_key_pem = ""

    def generate_keypair(self):
        """
        Generate RSA public/private key pair for letter encryption.

        Uses RSA-4096 for strong encryption of letter content.
        This is separate from the ECDSA wallet keys - RSA is better
        suited for encryption while ECDSA is optimal for signatures.

        RSA-4096 allows encrypting messages up to ~500 bytes.
        For larger messages, OAEP padding is used.

        Returns:
            None (modifies self)
        """
        # Generate RSA 4096-bit key pair (larger keys allow larger messages)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )

        # Derive public key from private key
        self.public_key = self.private_key.public_key()

        # Serialize to PEM format
        self._private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        self._public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    def encrypt_message(self, message: str, public_key_pem: str) -> str:
        """
        Encrypt a message using RSA public key encryption.

        This allows encrypting messages to future iterations - they can
        only be decrypted by someone with the corresponding private key.

        Args:
            message: The plaintext message to encrypt
            public_key_pem: Public key in PEM format to encrypt to

        Returns:
            Base64-encoded encrypted message
        """
        # Load public key from PEM
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))

        # Encrypt using OAEP padding (secure padding scheme)
        encrypted_bytes = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Return as base64 for easy storage/transmission
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt_message(self, encrypted_message: str, private_key_pem: str) -> str:
        """
        Decrypt an RSA-encrypted message using private key.

        Args:
            encrypted_message: Base64-encoded encrypted message
            private_key_pem: Private key in PEM format

        Returns:
            Decrypted plaintext message

        Raises:
            ValueError: If decryption fails (wrong key or corrupted data)
        """
        try:
            # Load private key from PEM
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None
            )

            # Decode base64
            encrypted_bytes = base64.b64decode(encrypted_message)

            # Decrypt using OAEP padding
            decrypted_bytes = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return decrypted_bytes.decode('utf-8')

        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def get_public_key_pem(self) -> str:
        """Get public key in PEM format for sharing."""
        return self._public_key_pem

    def get_private_key_pem(self) -> str:
        """Get private key in PEM format. Keep this secret!"""
        return self._private_key_pem


def encrypt_letter(message: str, public_key_pem: str) -> str:
    """
    Helper function to encrypt a letter to a public key.

    Args:
        message: Letter content to encrypt
        public_key_pem: Recipient's public key

    Returns:
        Base64-encoded encrypted letter
    """
    encryptor = LetterEncryption()
    return encryptor.encrypt_message(message, public_key_pem)


def decrypt_letter(encrypted_message: str, private_key_pem: str) -> str:
    """
    Helper function to decrypt a letter with a private key.

    Args:
        encrypted_message: Encrypted letter content
        private_key_pem: Private key to decrypt with

    Returns:
        Decrypted letter content

    Raises:
        ValueError: If decryption fails
    """
    encryptor = LetterEncryption()
    return encryptor.decrypt_message(encrypted_message, private_key_pem)
