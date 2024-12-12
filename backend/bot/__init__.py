from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, Update
from aiogram.utils.deep_linking import create_start_link, decode_payload
from bot.routers.base import router as base_router
from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH
from database.requests import get_user, set_referral, set_user
from fastapi import Request

async def create_ref_link(user_id):
    link = await create_start_link(bot, str(user_id), encode=True)

    return link


async def extract_referrer(message_text: str):
    try:
        payload = message_text.removeprefix('/start').strip()

        if not payload:
            raise Exception('No payload')

        payload_user_id = decode_payload(payload)
        referrer = await get_user(user_id=payload_user_id)
        return referrer
    except Exception as e:
        pass


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str: Any],
    ) -> Any:

        if not event.chat.type == 'private':
            return

        user = await get_user(user_id=event.from_user.id)

        if not user:
            referrer = await extract_referrer(event.text)
            user = await set_user(user_id=event.from_user.id, username=event.from_user.username)

            if referrer:
                await set_referral(referrer_id=referrer.id, referral_id=user.id)

        data['user'] = user

        return await handler(event, data)


async def run_bot_webhook():
    me = await bot.get_me()
    print(me.username)

    await bot.set_webhook(f'{WEBHOOK_HOST}/{WEBHOOK_PATH}', drop_pending_updates=True, allowed_updates=["message", "edited_channel_post", "callback_query"])


async def run_bot_polling():
    me = await bot.get_me()
    print(me.username)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(base_router)
dp.message.middleware(RegisterUserMiddleware())


async def process_update(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
