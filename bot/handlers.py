# bot/handlers.py

import html
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import get_main_menu, get_admin_keyboard, get_language_kb
from bot.config import ADMIN_ID, ADMIN_GROUP_ID, CARD_NUMBER, CHANNEL_ID
from bot.strings import TEXTS

router = Router()

# ─── Хранилище языков пользователей (в памяти) ───────────────────────────────
user_languages = {}

def get_lang(user_id: int) -> str:
    return user_languages.get(user_id, 'ru')

# ─── FSM состояния ────────────────────────────────────────────────────────────
class DeclineState(StatesGroup):
    waiting_for_reason = State()   # Ждём, когда админ напишет причину


# ─── Команда /start ────────────────────────────────────────────────────────────
@router.message(Command("start"))
async def start_cmd(message: Message):
    """Показываем выбор языка при старте."""
    await message.answer(
        TEXTS['ru']['select_lang'] + "\n" + TEXTS['uz']['select_lang'],
        reply_markup=get_language_kb()
    )

# ─── Выбор языка ──────────────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    """Сохраняем язык и показываем главное меню."""
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang

    await callback.message.delete()
    await callback.message.answer(
        TEXTS[lang]['lang_selected'],
        reply_markup=get_main_menu(lang)
    )
    await callback.message.answer(TEXTS[lang]['welcome'], parse_mode="HTML")
    await callback.answer()

# ─── Вспомогательная команда: узнать ID чата ──────────────────────────────────
@router.message(Command("get_id"))
async def get_id_cmd(message: Message):
    await message.answer(f"🆔 ID этого чата: <code>{message.chat.id}</code>", parse_mode="HTML")

# ─── О курсе ──────────────────────────────────────────────────────────────────
@router.message(lambda m: m.text in [TEXTS['ru']['btn_about'], TEXTS['uz']['btn_about']])
async def about_course(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['about'], parse_mode="HTML")

# ─── Бесплатный канал ─────────────────────────────────────────────────────────
@router.message(lambda m: m.text in [TEXTS['ru']['btn_free'], TEXTS['uz']['btn_free']])
async def free_channel(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['free'], parse_mode="HTML")

# ─── Купить курс ──────────────────────────────────────────────────────────────
@router.message(lambda m: m.text in [TEXTS['ru']['btn_buy'], TEXTS['uz']['btn_buy']])
async def buy_course(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(
        TEXTS[lang]['buy'].format(card_number=CARD_NUMBER),
        parse_mode="HTML"
    )

# ─── Получение чека ───────────────────────────────────────────────────────────
@router.message(F.photo)
async def handle_receipt(message: Message, bot: Bot):
    """Пользователь прислал фото чека — уведомляем и пересылаем в группу."""
    lang = get_lang(message.from_user.id)
    await message.answer(TEXTS[lang]['waiting'], parse_mode="HTML")

    try:
        username = html.escape(message.from_user.username) if message.from_user.username else "Unknown"
        await bot.send_photo(
            chat_id=ADMIN_GROUP_ID,
            photo=message.photo[-1].file_id,
            caption=(
                TEXTS[lang]['admin_new'].format(username=username, user_id=message.from_user.id)
                + f"\n🌍 Язык: {lang.upper()}"
            ),
            reply_markup=get_admin_keyboard(message.from_user.id),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"ОШИБКА ПРИ ОТПРАВКЕ В ГРУППУ: {e}")

# ─── Кнопка «Одобрить» ────────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("approve_"))
async def approve_payment(callback: CallbackQuery, bot: Bot):
    """Создаём одноразовую ссылку и отправляем пользователю."""
    user_id = int(callback.data.split("_")[1])
    admin_user = callback.from_user
    lang = get_lang(user_id)

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )

        # Сообщение пользователю
        await bot.send_message(
            user_id,
            TEXTS[lang]['approved'].format(invite_link=invite_link.invite_link),
            parse_mode="HTML"
        )

        # Отчёт в группу
        admin_mention = f"@{admin_user.username}" if admin_user.username else f"ID {admin_user.id}"
        await bot.send_message(
            ADMIN_GROUP_ID,
            (
                f"{TEXTS[lang]['sep']}\n"
                f"✅ <b>ОДОБРЕНО</b>\n"
                f"Адм: {html.escape(admin_mention)}\n"
                f"Юзер ID: {user_id}\n"
                f"Ссылка отправлена.\n"
                f"{TEXTS[lang]['sep']}"
            ),
            parse_mode="HTML"
        )

        # Помечаем фото как обработанное
        await callback.message.edit_caption(
            caption=callback.message.caption + f"\n\n✅ Одобрено: {admin_mention}",
        )
        await callback.answer("✅ Одобрено!")
    except Exception as e:
        print(f"ERROR IN APPROVE: {e}")
        await callback.answer(f"Ошибка: {e}", show_alert=True)

# ─── Кнопка «Отклонить» ───────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("decline_"))
async def decline_payment(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Переходим в FSM — просим Admin написать причину отказа."""
    user_id = int(callback.data.split("_")[1])
    admin_user = callback.from_user
    lang = get_lang(user_id)

    # Сохраняем данные в FSM
    await state.set_state(DeclineState.waiting_for_reason)
    await state.update_data(
        target_user_id=user_id,
        lang=lang,
        admin_mention=f"@{admin_user.username}" if admin_user.username else f"ID {admin_user.id}",
        original_caption=callback.message.caption,
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id
    )

    await callback.message.reply(
        "✏️ <b>Напишите причину отказа</b> — она будет переслана пользователю:",
        parse_mode="HTML"
    )
    await callback.answer()

# ─── Получение причины отказа от Admin ───────────────────────────────────────
@router.message(DeclineState.waiting_for_reason)
async def receive_decline_reason(message: Message, bot: Bot, state: FSMContext):
    """Admin написал причину — отправляем пользователю и завершаем FSM."""
    data = await state.get_data()
    user_id = data['target_user_id']
    lang = data['lang']
    admin_mention = data['admin_mention']
    original_caption = data['original_caption']
    original_msg_id = data['message_id']
    original_chat_id = data['chat_id']
    reason = html.escape(message.text)

    await state.clear()

    try:
        # Отправляем причину пользователю
        await bot.send_message(
            user_id,
            (
                f"{TEXTS[lang]['declined']}\n\n"
                f"📋 <b>Причина:</b> {reason}"
            ),
            parse_mode="HTML"
        )

        # Отчёт в группу
        await bot.send_message(
            ADMIN_GROUP_ID,
            (
                f"{TEXTS[lang]['sep']}\n"
                f"❌ <b>ОТКЛОНЕНО</b>\n"
                f"Адм: {html.escape(admin_mention)}\n"
                f"Юзер ID: {user_id}\n"
                f"Причина: {reason}\n"
                f"{TEXTS[lang]['sep']}"
            ),
            parse_mode="HTML"
        )

        # Помечаем фото как обработанное
        await bot.edit_message_caption(
            chat_id=original_chat_id,
            message_id=original_msg_id,
            caption=original_caption + f"\n\n❌ Отклонено ({admin_mention}): {message.text}"
        )

        await message.reply("✅ Причина отправлена пользователю.")
    except Exception as e:
        print(f"ERROR IN DECLINE REASON: {e}")
        await message.reply(f"Ошибка при отправке: {e}")

# ─── Кнопка «Админ» ───────────────────────────────────────────────────────────
@router.message(lambda m: m.text in [TEXTS['ru']['btn_admin'], TEXTS['uz']['btn_admin']])
async def admin_info(message: Message):
    lang = get_lang(message.from_user.id)
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🛠 <b>Вы зашли как администратор.</b>\nВсе чеки приходят в вашу группу.",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "👨‍💻 <b>Связь с администратором:</b> @your_admin_handle",
            parse_mode="HTML"
        )
