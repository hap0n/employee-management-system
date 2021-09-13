import os

import uvicorn
from fastapi import FastAPI


async def app():
    return FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs/", redoc_url="/api/redoc/")


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("EMP_SYS_API_PORT")), loop="asyncio")


if __name__ == "__main__":
    main()
