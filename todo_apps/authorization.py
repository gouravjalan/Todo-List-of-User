from passlib.context import CryptContext
from jose import JWTError,jwt,ExpiredSignatureError
from datetime import datetime,timedelta
from fastapi import HTTPException


#secret key for jwt
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

#password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


#hash password
def hash_password(password: str):
    if len(password) > 72:
        password = password[:72]

    return pwd_context.hash(password)

#verify password
def verify_password(plain_password:str, hashed_password:str):
    if len(plain_password) > 72:
        plain_password = plain_password[:72]

    return pwd_context.verify(plain_password, hashed_password)

#create jwt token
def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) #expllicitly working as base64 only which encodes the data

    return encoded_jwt

#to verify token  for oauth2 authentication.
# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")

#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return user_id

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#for jwt
def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])  #deocdes the parameters that r given.
        user_id = payload.get("sub") #from the decoded data get the subject/id of user and store in user_id.

        return user_id.strip() if user_id else None
    #strip is used to remove unwanted space.

    
    #when the token gets expired.
    except ExpiredSignatureError:
        # return "expired"
        raise HTTPException(status_code=401,detail="Token Expired")
    #to catch error if anything goes invalid/expired/worng
    # instead of crashing, return none.
    except JWTError:
        # return None
        raise HTTPException(status_code=401,detail="Invalid Token")
    
    
    
#to create a refresh token
def create_refresh_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=7)    #long expiry for refresh token.
    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


#jwt used to encode and decode JWT Token
#HWTError used to handle errors during decoding/verification
#datetime gets current time
#timedate help to add time (like 30 minutes.)
#secret key used in HMAC to sign the token   (HS256)
#HS256 = HMAC + SHA256

#ACCESS_TOKEN_EXPIRE_MINUTES = 30 tell that token will expire in 30 minutes
#data:dict is function that will take dictionary (payload) as data.
#.copy() to make copy of input data to avoid the alteration of it.
#utcnow() gets current time, and add 30minutes to it.