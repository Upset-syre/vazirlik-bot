from bot.exts import db
from bot.config import SQLALCHEMY_DATABASE_URI

engine = create_async_engine(
        SQLALCHEMY_DATABASE_URI
    )

async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )