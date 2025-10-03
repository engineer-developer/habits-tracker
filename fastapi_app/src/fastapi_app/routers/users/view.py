from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    name="Get all users",
    description="Get all users from database",
    response_class=JSONResponse,
    responses={400: {"description": "No content"}},
)
async def get_all_users():
    # users_dao = fetch_users_from_db()
    users = [
        {"name": "Bob"},
        {"name": "Jack"},
        {"name": "Piter"},
    ]
    content = {"users": users}
    if content:
        return JSONResponse(content)
    else:
        raise HTTPException(400, "No content")
