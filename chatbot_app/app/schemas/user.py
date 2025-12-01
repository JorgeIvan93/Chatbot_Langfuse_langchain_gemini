from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=4, max_length=128)
    email: EmailStr | None = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    is_active: bool

    class Config:
        from_attributes = True 
