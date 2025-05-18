# Copyright 2025 James G Willmore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import bcrypt
from cryptography.fernet import Fernet

# File paths
SALT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "resources",
    "encrypted_salt.bin",
)
FERNET_KEY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "resources",
    "fernet.key",
)


class Authentication:
    """Authentication class for password hashing and verification.
    This class handles the generation and storage of a Fernet key and an encrypted salt,
    and provides methods for hashing and verifying passwords using bcrypt.
    Attributes:
        fernet_key (bytes): The Fernet key used for encryption/decryption.
        fernet (Fernet): The Fernet object initialized with the Fernet key.
        salt (bytes): The salt used for hashing passwords, stored in encrypted form.
    """

    def __init__(self):
        # Step 1: Generate/load Fernet key (used to encrypt/decrypt salt)
        self.fernet_key = self.load_or_create_fernet_key()
        self.fernet = Fernet(self.fernet_key)

        # Step 2: Generate/load encrypted salt
        self.salt = self.load_or_create_encrypted_salt(self.fernet)

    def load_or_create_fernet_key(self):
        """Generate/load Fernet key."""
        if os.path.exists(FERNET_KEY_FILE):
            with open(FERNET_KEY_FILE, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(FERNET_KEY_FILE, "wb") as f:
                f.write(key)
            return key

    def load_or_create_encrypted_salt(self, fernet: Fernet):
        """Generate/load encrypted salt."""
        if os.path.exists(SALT_FILE):
            with open(SALT_FILE, "rb") as f:
                encrypted_salt = f.read()
                return fernet.decrypt(encrypted_salt)
        else:
            salt = bcrypt.gensalt()
            encrypted_salt = fernet.encrypt(salt)
            with open(SALT_FILE, "wb") as f:
                f.write(encrypted_salt)
            return salt

    def hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt and the stored salt.
        This function takes a password as input, hashes it using bcrypt with the stored salt,
        and returns the hashed password as bytes.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password.
        Example:
            hashed_password = auth.hash_password("my_secure_password")
        """
        return bcrypt.hashpw(password.encode(), self.salt)

    def verify_password(self, password: str, stored_hash: bytes) -> bool:
        """Verify a password against a stored hash.
        This function takes a password and a stored hash as input,
        and checks if the password matches the stored hash.

        Args:
            password (str): The password to verify.
            stored_hash (bytes): The stored hash to compare against.
        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        Example:
            is_valid = auth.verify_password("my_secure_password", stored_hash)
        """
        return bcrypt.checkpw(password.encode(), stored_hash)
