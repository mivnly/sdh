from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str
    comment: str | None = None

class UserCreate(UserBase):
    role: str = "user"
    
class UserRead(UserBase):
    role: str = "user"
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
    role: str | None = None
