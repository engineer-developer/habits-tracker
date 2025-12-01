from fastapi.routing import APIRouter

router = APIRouter(prefix="/reminders", tags=["reminders"])



@router.get("/{job_id:str}/confirm/")
async def confirm_habit_success_done(
        user
):
    pass