from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.main import router
from config.settings import get_settings

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
    servers=[

        {
            "url": "http://localhost:7000",
            "description": "Development server"
        },

    ]
)

# CSRF config


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
    expose_headers= settings.exposed_headers,



)




app.include_router(router)


# root api endpoint
@app.get("/")
def root():
    return {"message": "whispR to the world!"}