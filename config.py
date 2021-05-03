from dataclasses import dataclass

@dataclass
class Config:
    db_type: str = 'postgresql'
    db_user: str = 'postgres'
    db_password: str = 'password'
    db_host: str = '1.2.3.4'
    db_name: str = 'selecticket'

    @classmethod
    def get_db_uri(cls):
        return f'{cls.db_type}://{cls.db_user}:{cls.db_password}@{cls.db_host}/{cls.db_name}'