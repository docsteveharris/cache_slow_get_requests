"""
Entry point and main file for the FastAPI backend
"""

import time

import arrow
from fastapi import FastAPI 

app = FastAPI()


@app.get("/ping/slow")
def pong() -> str:
    notnow = arrow.utcnow().format("YYYY-MM-DD HH:mm:ss.SSS")
    time.sleep(5)
    return notnow


@app.get("/ping/fast")
def pong() -> str:
    now = arrow.utcnow().format("YYYY-MM-DD HH:mm:ss.SSS")
    return now
