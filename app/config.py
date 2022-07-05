#this file is used to hold all the environment variables.
#for dev wee define all the env vars in the .env file in project folder.
#but at prod we define thwese on system itself instead of file.
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings() #created object of the setting class]
print(settings.database_hostname)
print(settings.database_port)
print(settings.database_password)
print(settings.database_name)
print(settings.database_username)
print(settings.secret_key)
print(settings.algorithm)

print(settings.access_token_expire_minutes)

