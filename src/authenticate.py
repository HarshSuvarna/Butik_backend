import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from dotenv import load_dotenv

load_dotenv()

class AuthHandler():
    security = HTTPBearer()
    secret = os.getenv("SECRETS")
    
    def encode_token(self, mobile, cc):
        secret = os.getenv("SECRETS")
        algorithms = os.getenv("ALGORITHMS")

        payload = {
            #'exp': datetime.utcnow() + timedelta(days=120),
            #'iat': datetime.utcnow(),
            'sub':  [mobile, cc]
    
        }
        return jwt.encode(
            payload,
            secret,
            algorithm=algorithms
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail={'status_code':0, 'message':'Signature has expired', 'data':{}})
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail={'status_code':0, 'message':'Invalid token', 'data':{}})

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)