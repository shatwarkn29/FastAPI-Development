"""
Configuration module for the application.

This module defines the `Settings` class, which reads and stores
environment variables for the application's configuration.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    A class to hold application settings loaded from environment variables.

    Attributes:
        database_hostname (str): The hostname for the database.
        database_port (str): The port number for the database.
        database_password (str): The password for the database.
        database_name (str): The name of the database.
        database_username (str): The username for the database.
        secret_key (str): The secret key for the application.
        algorithm (str): The hashing algorithm for security.
        access_token_expire_minutes (int): Token expiration time in minutes.
    """

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """
        Configuration for Pydantic's BaseSettings.

        Attributes:
            env_file (str): The name of the file containing environment variables.
        """
        env_file = ".env"


# Instantiate the settings object
settings = Settings()
