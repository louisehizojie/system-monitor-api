import check_services
import config
import conn_oracle
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from auth_pyjwt import authenticate_user, create_access_token, get_current_user
import uvicorn

logger = config.logger
app = FastAPI(lifespan=conn_oracle.lifespan)

""" Likely only needed for development when running client from your machine.
    Once deployed, the client would be running from the same server and expected to have the same origin.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates the user and returns a JWT access token upon success.
    """
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Create the token, using 'sub' (subject) to identify the user
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    
    # Return the token in the standard OAuth2 format
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def read_root():
    return { "database": config.db_conn_info.database }

@app.get("/crmmessengerstatus")
async def check_crm_messenger():
    return {"status": f"{check_services.get_crm_messenger_status()}"}

@app.get("/allstatuses")
async def check_all_statuses(current_user: dict = Depends(get_current_user)):
    return check_services.get_all_statuses()

if __name__ == "__main__":
    logger.info("Service started successfully!")
    uvicorn.run(
        "main:app", 
        host=config.server_info.host, 
        port=config.server_info.port, 
        workers=config.server_info.workers,
        ssl_keyfile=config.server_info.ssl_keyfile,
        ssl_certfile=config.server_info.ssl_certfile
    )
