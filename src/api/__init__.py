from fastapi import APIRouter


from src.api.user.user import user_router
from src.api.message.message import mess_router
from src.api.botchat.botchat import chat_router
from src.api.payment.payment import payment_router
router = APIRouter()

router.include_router(user_router, prefix="/api/user", tags=["User"])
router.include_router(mess_router, prefix="/api/mess", tags=["Mess"])
router.include_router(chat_router, prefix="/api/chat", tags=["ChatBot"])
router.include_router(payment_router, prefix="/api/payment", tags=["Payment"])
__all__ = ["router"]
