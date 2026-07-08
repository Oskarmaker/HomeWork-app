from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="student/entry")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="teacher/entry")

async def get_current_user(token = Depends(oauth2_scheme)):
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def require_teacher(user = Depends(get_current_user)):
    if user.get('role') != 'teacher':
        raise HTTPException(status_code=403, detail="You are not a teacher")
    return user

def require_student(user = Depends(get_current_user)):
    if user.get('role') != 'student':
        raise HTTPException(status_code=403, detail="You are not a student")
    return user