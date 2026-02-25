from sqlalchemy import Identity, BigInteger, MetaData, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Creating only one class with single metadata and registry.
# Otherwise each class will have its own.
class Base(DeclarativeBase):
    metadata = MetaData(schema="public")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    surname: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
