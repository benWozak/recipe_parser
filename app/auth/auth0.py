from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
import os
from typing import Optional

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://localhost:8000/authorize",
    tokenUrl="http://localhost:8000/oauth/token"
)

class Auth0Handler:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.api_audience = os.getenv("AUTH0_API_AUDIENCE")
        self.algorithms = ["RS256"]
        
    async def verify_token(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            jwks_url = f"https://{self.domain}/.well-known/jwks.json"
            unverified_headers = jwt.get_unverified_headers(token)
            jwks_client = jwt.PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=self.algorithms,
                audience=self.api_audience,
                issuer=f"https://{self.domain}/"
            )
            
            return payload
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

auth0_handler = Auth0Handler()