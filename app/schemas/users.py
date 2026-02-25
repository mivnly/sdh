from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str | None = None
    surname: str | None = None
    comment: str | None = None

class UserCreate(UserBase):
    username: str
    role: str = "user"
    
class UserRead(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = None
    role: str | None = None
