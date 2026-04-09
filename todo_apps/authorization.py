from passlib.context import CryptContext
from jose import JWTError,jwt,ExpiredSignatureError
from datetime import datetime,timedelta
from fastapi import HTTPException



SECRET_KEY = "mysecretkey"     #tosign jwt token
ALGORITHM = "HS256"            #HMAC + SHA256 to encrypt and verify token
ACCESS_TOKEN_EXPIRE_MINUTES = 30   #3 minutes

#password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],     #bcrypt is hashing alog.
    deprecated="auto"       #handle old hash automatically.
)


#hash password
def hash_password(password: str):
    if len(password) > 72:
        password = password[:72]

    return pwd_context.hash(password) #the object that calls .hash() method to hash the plain password.


#verify password
def verify_password(plain_password:str, hashed_password:str):
    if len(plain_password) > 72:
        plain_password = plain_password[:72]

    return pwd_context.verify(plain_password, hashed_password)

#create jwt token before table 3
# def create_access_token(data:dict):
#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     to_encode.update({"exp" : expire})

#     encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) #expllicitly working as base64 only which encodes the data

#     return encoded_jwt

#after table 3
# def create_access_token(user):
#     # 🔥 Extract role from user_roles table
#     role = user.roles[0].role if user.roles else None

#     if not role:
#         raise HTTPException(status_code=400, detail="User has no role assigned")

#     to_encode = {
#         "sub": str(user.id),
#         "role": role
#     }

#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})

#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#after table 3 creation
def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



    
# to verify token  for oauth2 authentication.
# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")
#         role: str = payload.get("role")

#         if user_id is None or role is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return { 
#             "user_id" : user_id,
#             "role": role
#         }

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#for jwt
def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])  #deocdes the parameters that r given.
        user_id = payload.get("sub") #from the decoded data get the subject/id of user and store in user_id.
        role = payload.get("role")
        # return user_id.strip() if user_id else None
        #strip is used to remove unwanted space.

        #for rbac
        if not user_id or not role:
            raise HTTPException(status_code=401,detail="Invalid Token")
        
        return{
            "user_id" : user_id.strip(),
            "role": role
        } 
        
    #when the token gets expired.
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token Expired")
        # return "expired"
        #to catch error if anything goes invalid/expired/worng
        # instead of crashing, return none.

    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid Token")
        # return None
        #runs if token is invalid/wrong/corrupted.
    
    
#to create a refresh token before table 3
# def create_refresh_token(data:dict):
#     to_encode = data.copy()

#     expire = datetime.utcnow() + timedelta(days=7)    #long expiry for refresh token.
#     to_encode.update({"exp" : expire})

#     return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

#after table 3
# def create_refresh_token(user):
#     role = user.roles[0].role if user.roles else None

#     if not role:
#         raise HTTPException(status_code=400, detail="User has no role assigned")

#     to_encode = {
#         "sub": str(user.id),
#         "role": role
#     }

#     expire = datetime.utcnow() + timedelta(days=7)
#     to_encode.update({"exp": expire})

#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#after table 3 creation
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#jwt used to encode and decode JWT Token
#HWTError used to handle errors during decoding/verification
#datetime gets current time
#timedate help to add time (like 30 minutes.)
#secret key used in HMAC to sign the token   (HS256)
#HS256 = HMAC + SHA256

#ACCESS_TOKEN_EXPIRE_MINUTES = 30 tell that token will expire in 30 minutes
#data:dict is function that will take dictionary (payload) as data.
#.copy() to make copy of input data to avoid the alteration of it.
#utcnow() gets current time, and timedelta() (add 30minutes to it)

#jwt to create and decode tokens
#JWTError (for genereal error like invalid token)
#ExpiredSignatureError   when token in expired.
#datetime for current time
#timedelta to add time(min., days)
#CryptContext is a password hashing manager from Passlib i.e it is object that handles password hashing and verifying passwords for you.
# passlib.context is module/package in passlib library that contatins tools to manage password hashing. Ex: Cryptocontext.
# jose (JavaScript Object Signing & Encryption) is library  used for creating and verifying JWT Tokens
#jwt used for creating and decoding token
#JWTError is error class 
#ExpiredSignatureError is specific error used when token expiry time is over. 