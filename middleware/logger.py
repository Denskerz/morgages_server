from loguru import logger
from fastapi import Request


logger.add("debug.log", format="{time:HH:mm:ss} {level} {message}", rotation="10 MB", compression="zip")


async def log_requests_dependency(request: Request):
    params = {name: value for name, value in request.path_params.items()}
    headers = {name: value for name, value in request.headers.items()}
    body = await request.body()
    log_str = f"""
    {request.method} {request.url}
    Params:
    {params}
    Headers:
    {headers}
    Body:
    {body}
    """
    logger.debug(log_str)


async def log_errors_middleware(request: Request, call_next):
    @logger.catch(reraise=True)
    async def _call_next():
        return await call_next(request)

    response = await _call_next()

    return response

