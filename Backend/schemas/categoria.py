from sqlmodel import SQLModel, Field


class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str = Field(min_length=2, max_length=300)


class CategoriaRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
