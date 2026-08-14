from fastapi import APIRouter

router = APIRouter()

@router.get("/api/health")
async def health():

    ## another check here

    return "OK"
