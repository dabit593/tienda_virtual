from sqlmodel import SQLModel, Field


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str = Field(max_length=300)
