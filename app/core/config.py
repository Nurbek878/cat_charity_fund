from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
