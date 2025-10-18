from pydantic import BaseModel, EmailStr, field_validator



class RegisterUser(BaseModel):
        
    login: str
    password: str
    name: str
    
    @field_validator("password")
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v
    

class LoginUser(BaseModel):
    
    login: str
    password: str   


class UpdateUser(BaseModel):

    login: str
    name: str


class UserShema(BaseModel):

    id: int
    name: str
    login: str