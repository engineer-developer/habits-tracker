from aiogram.dispatcher.router import Router
from .register import router as register_router
from .login import router as login_router

router = Router(name="auth")

router.include_router(register_router)
router.include_router(login_router)