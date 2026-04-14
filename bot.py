"""
bot.py — Telegram-бот для продажи курса «ЗАКВАСКАЛИ НОН»
Запуск: python bot.py
Переменные окружения (Render → Environment Variables):
  BOT_TOKEN, ADMIN_GROUP_ID, CHANNEL_ID, CARD_NUMBER
"""

import asyncio
import html
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

# ──────────────────────────────────────────────────────────────────────────────
# Конфигурация — читаем из переменных окружения
# ──────────────────────────────────────────────────────────────────────────────
BOT_TOKEN      = os.getenv("BOT_TOKEN", "")
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))
CHANNEL_ID     = int(os.getenv("CHANNEL_ID", "0"))
CARD_NUMBER    = os.getenv("CARD_NUMBER", "0000 0000 0000 0000")

# ──────────────────────────────────────────────────────────────────────────────
# Тексты (RU & UZ — HTML-форматирование)
# ──────────────────────────────────────────────────────────────────────────────
TEXTS = {
    "ru": {
        "select_lang":    "🌍 Выберите язык / Tilni tanlang:",
        "lang_ok":        "✅ Язык изменён на Русский!",
        "welcome":        "🌟 <b>Добро пожаловать в «ЗАКВАСКАЛИ НОН»!</b> 🥖\n\nВыберите раздел 👇",
        "about":          "📚 <b>О курсе «ЗАКВАСКАЛИ НОН»</b>\n\n🔹 <b>Программа:</b>\n— Пошаговые видео-уроки\n— Пшеничная и ржаная закваска\n— Техника Stretch &amp; Fold\n— Формирование красивого хлеба\n\n✅ Для новичков\n✅ Поддержка кураторов\n✅ Гарантированный результат!",
        "free":           "🎁 <b>Бесплатный канал</b>\n\nПодписывайтесь: [ССЫЛКА] 📢",
        "buy":            (
            "💎 <b>Купить курс «ЗАКВАСКАЛИ НОН»</b>\n\n"
            "💵 <b>Цена:</b>\n"
            "❌ <s>1 000 000 сум</s>\n"
            "✅ <b>800 000 сум</b> 💸\n\n"
            "💳 Карта для оплаты:\n<code>{card}</code>\n\n"
            "📸 <b>После оплаты</b> пришлите скриншот чека прямо сюда!"
        ),
        "waiting":        "⏳ <b>Чек принят!</b>\n\nАдмин проверит оплату в течение 24 часов и вам придёт ссылка-приглашение. 🔔",
        "approved":       "✅ <b>Поздравляем!</b>\n\nОплата подтверждена 🎉\n\n🔗 {link}\n\nДобро пожаловать! 🔥",
        "declined":       "❌ <b>Оплата не подтверждена</b>\n\n📋 <b>Причина:</b> {reason}\n\nСвяжитесь с @support_handle",
        "admin_new":      "🔔 <b>НОВАЯ ЗАЯВКА</b>\n\nПользователь: @{username}\nID: <code>{uid}</code>\nЯзык: RU\n\n👇 Проверьте чек:",
        "sep":            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "ask_reason":     "✏️ <b>Напишите причину отказа</b> — она будет переслана пользователю:",
        "reason_sent":    "✅ Причина отправлена пользователю.",
        "btn_about":      "📚 О курсе",
        "btn_free":       "📢 Бесплатный канал",
        "btn_buy":        "💳 Купить курс",
        "btn_admin":      "🆘 Админ",
    },
    "uz": {
        "select_lang":    "🌍 Выберите язык / Tilni tanlang:",
        "lang_ok":        "✅ Til o'zbekchaga o'zgartirildi!",
        "welcome":        "🌟 <b>«ЗАКВАСКАЛИ НОН» akademiyasiga xush kelibsiz!</b> 🥖\n\nBo'limni tanlang 👇",
        "about":          "📚 <b>«ЗАКВАСКАЛИ НОН» kursi haqida</b>\n\n🔹 <b>Dastur:</b>\n— Qadam-baqadam video darslar\n— Bug'doy va javdar zakvaskasi\n— Stretch &amp; Fold texnikasi\n— Chiroyli non shakllantirish\n\n✅ Yangi boshlovchilar uchun\n✅ Kuratorlar yordami\n✅ Kafolatlangan natija!",
        "free":           "🎁 <b>Bepul kanal</b>\n\nObuna bo'ling: [LINK] 📢",
        "buy":            (
            "💎 <b>«ЗАКВАСКАЛИ НОН» kursini sotib olish</b>\n\n"
            "💵 <b>Narxi:</b>\n"
            "❌ <s>1 000 000 so'm</s>\n"
            "✅ <b>800 000 so'm</b> 💸\n\n"
            "💳 To'lov kartasi:\n<code>{card}</code>\n\n"
            "📸 <b>To'lovdan so'ng</b> chek rasmini shu yerga yuboring!"
        ),
        "waiting":        "⏳ <b>Chek qabul qilindi!</b>\n\nAdmin 24 soat ichida to'lovni tekshiradi va sizga havola yuboradi. 🔔",
        "approved":       "✅ <b>Tabriklaymiz!</b>\n\nTo'lov tasdiqlandi 🎉\n\n🔗 {link}\n\nXush kelibsiz! 🔥",
        "declined":       "❌ <b>To'lov tasdiqlanmadi</b>\n\n📋 <b>Sabab:</b> {reason}\n\n@support_handle bilan bog'laning",
        "admin_new":      "🔔 <b>YANGI ARIZA</b>\n\nFoydalanuvchi: @{username}\nID: <code>{uid}</code>\nTil: UZ\n\n👇 Chekni tekshiring:",
        "sep":            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "ask_reason":     "✏️ <b>Rad etish sababini yozing</b> — u foydalanuvchiga yuboriladi:",
        "reason_sent":    "✅ Sabab foydalanuvchiga yuborildi.",
        "btn_about":      "📚 Kurs haqida",
        "btn_free":       "📢 Bepul kanal",
        "btn_buy":        "💳 Kursni sotib olish",
        "btn_admin":      "🆘 Admin",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# Хранилище языков пользователей (в памяти)
# ──────────────────────────────────────────────────────────────────────────────
user_lang: dict[int, str] = {}

def get_lang(uid: int) -> str:
    return user_lang.get(uid, "ru")

# ──────────────────────────────────────────────────────────────────────────────
# FSM: ожидание причины отказа от Admin
# ──────────────────────────────────────────────────────────────────────────────
class DeclineState(StatesGroup):
    waiting_for_reason = State()

# ──────────────────────────────────────────────────────────────────────────────
# Клавиатуры
# ──────────────────────────────────────────────────────────────────────────────
def lang_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇷🇺 Русский",    callback_data="lang_ru"),
        InlineKeyboardButton(text="🇺🇿 O'zbek",     callback_data="lang_uz"),
    ]])

def main_menu(lang: str) -> ReplyKeyboardMarkup:
    t = TEXTS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_about"]),  KeyboardButton(text=t["btn_free"])],
            [KeyboardButton(text=t["btn_buy"]),    KeyboardButton(text=t["btn_admin"])],
        ],
        resize_keyboard=True,
    )

def admin_kb(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Одобрить",  callback_data=f"approve_{uid}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{uid}"),
    ]])

# ──────────────────────────────────────────────────────────────────────────────
# Роутер и хендлеры
# ──────────────────────────────────────────────────────────────────────────────
router = Router()

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(TEXTS["ru"]["select_lang"], reply_markup=lang_kb())

@router.message(Command("get_id"))
async def cmd_get_id(msg: Message):
    await msg.answer(f"🆔 ID этого чата: <code>{msg.chat.id}</code>", parse_mode="HTML")

@router.callback_query(F.data.startswith("lang_"))
async def cb_set_lang(cb: CallbackQuery):
    lang = cb.data.split("_")[1]
    user_lang[cb.from_user.id] = lang
    await cb.message.delete()
    await cb.message.answer(TEXTS[lang]["lang_ok"], reply_markup=main_menu(lang))
    await cb.message.answer(TEXTS[lang]["welcome"], parse_mode="HTML")
    await cb.answer()

@router.message(lambda m: m.text in [TEXTS[l]["btn_about"] for l in TEXTS])
async def cmd_about(msg: Message):
    lang = get_lang(msg.from_user.id)
    await msg.answer(TEXTS[lang]["about"], parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS[l]["btn_free"] for l in TEXTS])
async def cmd_free(msg: Message):
    lang = get_lang(msg.from_user.id)
    await msg.answer(TEXTS[lang]["free"], parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS[l]["btn_buy"] for l in TEXTS])
async def cmd_buy(msg: Message):
    lang = get_lang(msg.from_user.id)
    await msg.answer(TEXTS[lang]["buy"].format(card=CARD_NUMBER), parse_mode="HTML")

@router.message(lambda m: m.text in [TEXTS[l]["btn_admin"] for l in TEXTS])
async def cmd_admin(msg: Message):
    await msg.answer("👨‍💻 <b>Связь с администратором:</b> @your_admin_handle", parse_mode="HTML")

# ─── Получение чека ───────────────────────────────────────────────────────────
@router.message(F.photo)
async def cmd_photo(msg: Message, bot: Bot):
    lang = get_lang(msg.from_user.id)
    await msg.answer(TEXTS[lang]["waiting"], parse_mode="HTML")
    try:
        uname = html.escape(msg.from_user.username or "Unknown")
        caption = TEXTS[lang]["admin_new"].format(username=uname, uid=msg.from_user.id)
        await bot.send_photo(
            ADMIN_GROUP_ID,
            msg.photo[-1].file_id,
            caption=caption,
            reply_markup=admin_kb(msg.from_user.id),
            parse_mode="HTML",
        )
    except Exception as e:
        logging.error(f"send_photo error: {e}")

# ─── Одобрить ─────────────────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("approve_"))
async def cb_approve(cb: CallbackQuery, bot: Bot):
    uid = int(cb.data.split("_")[1])
    lang = get_lang(uid)
    admin = f"@{cb.from_user.username}" if cb.from_user.username else f"ID {cb.from_user.id}"
    try:
        inv = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
        await bot.send_message(uid, TEXTS[lang]["approved"].format(link=inv.invite_link), parse_mode="HTML")
        sep = TEXTS[lang]["sep"]
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"{sep}\n✅ <b>ОДОБРЕНО</b>\nАдм: {html.escape(admin)}\nЮзер: {uid}\n{sep}",
            parse_mode="HTML",
        )
        await cb.message.edit_caption(caption=cb.message.caption + f"\n\n✅ Одобрено: {admin}")
        await cb.answer("✅ Одобрено!")
    except Exception as e:
        logging.error(f"approve error: {e}")
        await cb.answer(str(e), show_alert=True)

# ─── Отклонить (шаг 1 — запрос причины) ──────────────────────────────────────
@router.callback_query(F.data.startswith("decline_"))
async def cb_decline(cb: CallbackQuery, state: FSMContext):
    uid = int(cb.data.split("_")[1])
    lang = get_lang(uid)
    admin = f"@{cb.from_user.username}" if cb.from_user.username else f"ID {cb.from_user.id}"
    await state.set_state(DeclineState.waiting_for_reason)
    await state.update_data(uid=uid, lang=lang, admin=admin,
                            caption=cb.message.caption,
                            msg_id=cb.message.message_id,
                            chat_id=cb.message.chat.id)
    await cb.message.reply(TEXTS[lang]["ask_reason"], parse_mode="HTML")
    await cb.answer()

# ─── Отклонить (шаг 2 — получить причину) ────────────────────────────────────
@router.message(DeclineState.waiting_for_reason)
async def get_reason(msg: Message, bot: Bot, state: FSMContext):
    d = await state.get_data()
    await state.clear()
    uid, lang, admin = d["uid"], d["lang"], d["admin"]
    reason = html.escape(msg.text)
    try:
        await bot.send_message(uid, TEXTS[lang]["declined"].format(reason=reason), parse_mode="HTML")
        sep = TEXTS[lang]["sep"]
        await bot.send_message(
            ADMIN_GROUP_ID,
            f"{sep}\n❌ <b>ОТКЛОНЕНО</b>\nАдм: {html.escape(admin)}\nЮзер: {uid}\nПричина: {reason}\n{sep}",
            parse_mode="HTML",
        )
        await bot.edit_message_caption(chat_id=d["chat_id"], message_id=d["msg_id"],
                                       caption=d["caption"] + f"\n\n❌ Отклонено ({admin}): {msg.text}")
        await msg.reply(TEXTS[lang]["reason_sent"])
    except Exception as e:
        logging.error(f"decline error: {e}")
        await msg.reply(f"Ошибка: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# Точка входа
# ──────────────────────────────────────────────────────────────────────────────
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                        format="%(asctime)s %(levelname)s %(message)s")
    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
