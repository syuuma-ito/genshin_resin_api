from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from get_resin import get_resin
from get_status import get_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def remove_none_values(d):
    result = {key: value for key, value in d.items() if value is not None}
    return result


class Cookie(BaseModel):
    ltuid: int | None
    ltoken: str | None
    ltuid_v2: int | None
    ltoken_v2: str | None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_resin")
async def get_resin_data(uid: int, cookies: Cookie):
    try:
        cookies = remove_none_values(dict(cookies))
        return await get_resin(cookies, uid)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=424, detail="Argument values are incorrect")


@app.post("/get_status")
async def get_status_data(uid: int, cookies: Cookie):
    try:
        cookies = remove_none_values(dict(cookies))
        return await get_status(cookies, uid)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=424, detail="Argument values are incorrect")
