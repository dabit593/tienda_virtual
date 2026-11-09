from sqlmodel import SQLModel, Field


class UsuarioCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=80)
    correo: str = Field(max_length=120)
    password: str = Field(min_length=8, max_length=80)


class UsuarioPublic(SQLModel):
    id: int
    nombre: str
    correo: str
    rol: str


class Token(SQLModel):
    access_token: str
    token_type: str
