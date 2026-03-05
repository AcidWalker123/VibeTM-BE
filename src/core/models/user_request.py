from pydantic import BaseModel, Field, field_validator
import re


class UserRegistrationRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=5, max_length=8)
    email: str = Field(min_length=5, max_length=255)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str):
        if not v.strip():
            raise ValueError("Can't be empty")
        # Ensure only alphabetic characters (no numbers or special chars)
        if not v.isalpha():
            raise ValueError("Can't contain numbers, special characters, or symbols")
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if not v.strip():
            raise ValueError("Can't be empty")
        # Check for special characters (allowing only alphanumeric)
        if not v.isalnum():
            raise ValueError("Can't contain special characters")
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str):
        if "@" not in v:
            raise ValueError("Must contain @ symbol")
        if not v.endswith(".com"):
            raise ValueError("Must end with .com")

        # Check for special characters in the local part (before @)
        # Assuming typical alphanumeric email constraints based on your requirements
        local_part = v.split("@")[0]
        if not re.match(r'^[a-zA-Z0-9]+$', local_part):
            raise ValueError("Cant contain special Characters")
        return v