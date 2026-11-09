from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    correo: str = Field(unique=True, index=True, max_length=120)
    hashed_password: str
    rol: str = Field(default="cliente")
