import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)