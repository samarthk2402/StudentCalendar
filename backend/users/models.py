from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

class UserCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.URLField()
    scopes = models.TextField()

    def encrypted_token(self, token: str) -> str:
        """Encrypt a token using the encryption key."""
        encryption_key = os.environ['ENCRYPTION_KEY']
        encryption_key_bytes = encryption_key.encode()
        cipher_suite = Fernet(encryption_key_bytes)
        return cipher_suite.encrypt(token.encode()).decode()

    def decrypted_token(self, token: str) -> str:
        """Decrypt a token using the encryption key."""
        encryption_key = os.environ['ENCRYPTION_KEY']
        encryption_key_bytes = encryption_key.encode()
        cipher_suite = Fernet(encryption_key_bytes)
        return cipher_suite.decrypt(token.encode()).decode()

    @property
    def decrypted_access_token(self) -> str: # runs when decrypted access token is retrieved
        """Return the decrypted access token."""
        if self.access_token:
            return self.decrypted_token(self.access_token)
        return ""

    @decrypted_access_token.setter
    def decrypted_access_token(self, value: str) -> None: # runs when decrypted access token is set
        """Encrypt and set the access token."""
        encryption_key = os.environ['ENCRYPTION_KEY']
        encryption_key_bytes = encryption_key.encode()
        cipher_suite = Fernet(encryption_key_bytes)
        self.access_token = cipher_suite.encrypt(value.encode()).decode()

    @property
    def decrypted_refresh_token(self) -> str:
        """Return the decrypted refresh token."""
        if self.refresh_token:
            encryption_key = os.environ['ENCRYPTION_KEY']
            encryption_key_bytes = encryption_key.encode()
            cipher_suite = Fernet(encryption_key_bytes)
            return cipher_suite.decrypt(self.refresh_token.encode()).decode()
        return ""

    @decrypted_refresh_token.setter
    def decrypted_refresh_token(self, value: str) -> None:
        """Encrypt and set the refresh token."""
        encryption_key = os.environ['ENCRYPTION_KEY']
        encryption_key_bytes = encryption_key.encode()
        cipher_suite = Fernet(encryption_key_bytes)
        self.refresh_token = cipher_suite.encrypt(value.encode()).decode()

    def save(self, *args, **kwargs):
        """Override save method to encrypt access and refresh tokens before saving."""
        if self.access_token:
            self.access_token = self.encrypted_token(self.access_token)
        if self.refresh_token:
            self.refresh_token = self.encrypted_token(self.refresh_token)
        super().save(*args, **kwargs)

