from fastapi import FastAPI

app = FastAPI(
    title="LifeOS Co-Pilot API",
    version="2.0.1",
    servers=[
        {
            "url": "https://life-os-private-practical-co-pilot.onrender.com",
            "description": "Production (Render)"
        }
    ],
)

# existing route includes remain unchanged
