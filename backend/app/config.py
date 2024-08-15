class Config:
    SECRET_KEY = 'mysupersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False