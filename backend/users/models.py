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
    classcharts_session_id = models.TextField(null=True)
    classcharts_student_id = models.IntegerField(null=True)

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
        self.access_token = self.encrypted_token(self.access_token)

    @property
    def decrypted_refresh_token(self) -> str:
        """Return the decrypted refresh token."""
        if self.refresh_token:
            return self.decrypted_token(self.refresh_token)
        return ""

    @decrypted_refresh_token.setter
    def decrypted_refresh_token(self, value: str) -> None:
        """Encrypt and set the refresh token."""
        self.refresh_token = self.encrypted_token(self.refresh_token)

    @property
    def decrypted_classcharts_session_id(self) -> str:
        """Return the decrypted refresh token."""
        if self.classcharts_session_id:
            return self.decrypted_token(self.classcharts_session_id)
        return ""

    @decrypted_classcharts_session_id.setter
    def decrypted_classcharts_session_id(self, value: str) -> None:
        """Encrypt and set the refresh token."""
        self.classcharts_session_id = self.encrypted_token(self.classcharts_session_id)

    def save(self, *args, **kwargs):
        """Override save method to encrypt access and refresh tokens before saving."""
        if self.access_token:
            self.access_token = self.encrypted_token(self.access_token)
        if self.refresh_token:
            self.refresh_token = self.encrypted_token(self.refresh_token)
        super().save(*args, **kwargs)

