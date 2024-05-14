from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import animal, catalog, admin, inventory, user, fight, leaderboard
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
DASS Fighting Madness Is HERE!!
"""

app = FastAPI(
    title="DASS Fighting Madness",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "names": "Sophia Chang, Angela Chen, Dale Percelay, Srish Maulik",
        "emails": "schan100@calpoly.edu, achen313@calpoly.edu, dpercela@calpoly.edu, sguhamau@calpoly.edu",
    },
)

"""origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)"""

app.include_router(inventory.router)
app.include_router(catalog.router)
app.include_router(user.router)
app.include_router(animal.router)
app.include_router(admin.router)
app.include_router(leaderboard.router)
app.include_router(fight.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fighting Madness!"}
