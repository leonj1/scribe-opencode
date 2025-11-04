from fastapi import APIRouter, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
import os

router = APIRouter()

# Initialize OAuth
oauth = OAuth()

# Google OAuth2 configuration
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/auth/google/login')
async def google_login(request: Request):
    """Initiate Google OAuth2 login flow."""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google/callback')
async def google_callback(request: Request):
    """Handle Google callback, issue backend JWT."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        if not user:
            raise HTTPException(status_code=400, detail='Failed to get user info from Google')
        
        # TODO: Implement JWT token generation and user session management
        # This would typically involve:
        # 1. Checking if user exists in database
        # 2. Creating new user if not exists
        # 3. Generating backend JWT token
        # 4. Returning token to frontend
        
        return {"user": user, "access_token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Google authentication failed: {str(e)}')