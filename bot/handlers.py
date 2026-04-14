# bot/handlers.py

import html
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards import get_main_menu, get_admin_keyboard, get_language_kb
from bot.config import ADMIN_ID, ADMIN_GROUP_ID, CARD_NUMBER, CHANNEL_ID
from bot.strings import TEXTS

router = Router()
user_languages = {} # Temporary in-memory storage for user language

def get_lang(user_id):
    return user_languages.get(user_id, 'ru')

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        TEXTS['ru']['select_lang'] + "\n" + TEXTS['uz']['select_lang'],
        reply_markup=get_language_kb()
    )

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang
    
    await callback.message.delete()
    await callback.message.answer(
        TEXTS[lang]['lang_selected'],
        reply_markup=get_main_menu(lang)
    )
    await callback.message.answer(TEXTS[lang]['welcome'], parse_mode="HTML")
    await callback.answer()

@router.message(Command("get_id"))
async def get_id_cmd(message: Message):
    await message.answer(f"🆔 ID этого чата: <code>{message.chat.id}</code>", parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS['ru']['btn_about'], TEXTS['uz']['btn_about']])
async def about_course(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['about'], parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS['ru']['btn_free'], TEXTS['uz']['btn_free']])
async def free_channel(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['free'], parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS['ru']['btn_buy'], TEXTS['uz']['btn_buy']])
async def buy_course(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(
        TEXTS[lang]['buy'].format(card_number=CARD_NUMBER),
        parse_mode="HTML"
    )

@router.message(F.photo)
async def handle_receipt(message: Message, bot: Bot):
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['waiting'], parse_mode="HTML")
    
    try:
        # Отправляем в группу админов
        username = html.escape(message.from_user.username) if message.from_user.username else "Unknown"
        await bot.send_photo(
            chat_id=ADMIN_GROUP_ID,
            photo=message.photo[-1].file_id,
            caption=TEXTS[lang]['admin_new'].format(
                username=username,
                user_id=message.from_user.id
            ) + f"\n🌍 Язык: {lang.upper()}",
            reply_markup=get_admin_keyboard(message.from_user.id),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"ОШИБКА ПРИ ОТПРАВКЕ В ГРУППУ: {e}")

@router.callback_query(F.data.startswith("approve_"))
async def approve_payment(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[1])
    admin_user = callback.from_user
    lang = get_lang(user_id)
    
    try:
        # Создаем ссылку
        invite_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )
        
        await bot.send_message(
            user_id,
            TEXTS[lang]['approved'].format(invite_link=invite_link.invite_link),
            parse_mode="HTML"
        )
        
        # Отчет в группу
        admin_mention = f"@{admin_user.username}" if admin_user.username else f"ID: {admin_user.id}"
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"{TEXTS[lang]['sep']}\n✅ <b>ОДОБРЕНО</b>\nАдм: {html.escape(admin_mention)}\nЮзер ID: {user_id}\nСсылка отправлена.\n{TEXTS[lang]['sep']}",
            parse_mode="HTML"
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption + f"\n\n✅ ОДОБРЕНО АДМИНОМ {admin_mention}",
            parse_mode=None
        )
        await callback.answer("Одобрено!")
    except Exception as e:
        print(f"ERROR IN APPROVE: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)

@router.callback_query(F.data.startswith("decline_"))
async def decline_payment(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split("_")[1])
    admin_user = callback.from_user
    lang = get_lang(user_id)
    
    try:
        await bot.send_message(
            user_id,
            TEXTS[lang]['declined'],
            parse_mode="HTML"
        )
        
        # Отчет в группу
        admin_mention = f"@{admin_user.username}" if admin_user.username else f"ID: {admin_user.id}"
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"{TEXTS[lang]['sep']}\n❌ <b>ОТКЛОНЕНО</b>\nАдм: {html.escape(admin_mention)}\nЮзер ID: {user_id}\n{TEXTS[lang]['sep']}",
            parse_mode="HTML"
        )
        
        await callback.message.edit_caption(
            caption=callback.message.caption + f"\n\n❌ ОТКЛОНЕНО АДМИНОМ {admin_mention}",
            parse_mode=None
        )
        await callback.answer("Отклонено.")
    except Exception as e:
        print(f"ERROR IN DECLINE: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)

@router.message(lambda m: m.text in [TEXTS['ru']['btn_admin'], TEXTS['uz']['btn_admin']])
async def admin_info(message: Message):
    lang = get_lang(message.from_user.id)
    if message.from_user.id == ADMIN_ID:
        await message.answer("🛠 <b>Вы зашли как администратор.</b>\nВсе чеки приходят в вашу группу.", parse_mode="HTML")
    else:
        await message.answer("👨‍💻 <b>Связь с администратором:</b> @your_admin_handle", parse_mode="HTML")
