# bot/strings.py

TEXTS = {
    'ru': {
        'welcome': "🌟 <b>Добро пожаловать в Академию «ЗАКВАСКАЛИ НОН»!</b> 🌟\n\nЗдесь вы научитесь печь настоящий, полезный и ароматный хлеб на закваске в домашних условиях. 🥖✨\n\nЧтобы продолжить, выберите нужный раздел: 👇",
        'about': "📚 <b>О нашем курсе «ЗАКВАСКАЛИ НОН»</b>\n\nЭтот курс — ваш путеводитель в мир домашнего пекарства! 🚀\n\n🔹 <b>Что вас ждет:</b>\n— Пошаговые видео-уроки\n— Уход за пшеничной и ржаной закваской\n— Техника Stretch & Fold\n— Секреты формирования красивого хлеба\n\n🔸 <b>Преимущества:</b>\n✅ Подходит для новичков\n✅ Поддержка в «Bratskiy Chat»\n✅ Помощь кураторов\n✅ Гарантированный результат!\n\nСтаньте мастером своего дела вместе с нами! ✨",
        'free': "🎁 <b>Бесплатные материалы</b>\n\nПодписывайтесь на наш канал, где мы делимся рецептами и секретами выпечки: [ССЫЛКА] 📢",
        'buy': "💎 <b>Запись на курс «ЗАКВАСКАЛИ НОН»</b>\n\n💵 <b>Стоимость:</b>\n❌ <s>1 000 000 сум</s>\n✅ <b>800 000 сум</b> 💸\n\n🛡 <i>В стоимость входит:</i> все видео-уроки, доступ в закрытый чат и поддержка экспертов.\n\n📍 <b>Для оплаты:</b>\nПереведите <b>800 000 сум</b> на карту:\n💳 <code>{card_number}</code>\n\n📸 <b>ПОСЛЕ ОПЛАТЫ:</b>\nОбязательно пришлите скриншот или фото чека сюда, чтобы мы открыли вам доступ! 👇",
        'waiting': "⏳ <b>Ваш чек получен и отправлен на проверку!</b>\n\nНаши кураторы проверят платеж в течение часа. Как только всё подтвердится, я пришлю вам ссылку на обучение! 🔔",
        'approved': "✅ <b>Поздравляем!</b>\n\nВаша оплата успешно подтверждена. 🎉\nВот ваша персональная ссылка на закрытый канал курса:\n\n🔗 {invite_link}\n\nДобро пожаловать в команду! 🔥",
        'declined': "❌ <b>Оплата не подтверждена</b>\n\nК сожалению, мы не смогли подтвердить ваш платеж. 😔 Пожалуйста, проверьте данные или свяжитесь с поддержкой: @support_handle",
        'admin_new': "🔔 <b>НОВАЯ ЗАЯВКА</b>\n\nПользователь: @{username}\nID: {user_id}\n\nПожалуйста, проверьте чек ниже. 👇",
        'lang_selected': "✅ Язык успешно изменен на Русский!",
        'select_lang': "🌍 Выберите язык / Tilni tanlang:",
        'btn_about': "📚 О курсе",
        'btn_free': "📢 Бесплатный канал",
        'btn_buy': "💳 Купить",
        'btn_admin': "🆘 Админ",
        'sep': "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    },
    'uz': {
        'welcome': "🌟 <b>«ЗАКВАСКАЛИ НОН» akademiyasiga xush kelibsiz!</b> 🌟\n\nBu yerda siz uy sharoitida haqiqiy, sog'lom va xushbo'y zakvaskali non pishirishni o'rganasiz. 🥖✨\n\nDavom etish bo'limni tanlang: 👇",
        'about': "📚 <b>«ЗАКВАСКАЛИ НОН» kursi haqida</b>\n\nUshbu kurs — uyda non pishirish olamiga sizning yo'lboshchingiz! 🚀\n\n🔹 <b>Sizni nimalar kutmoqda:</b>\n— Qadam-baqadam video darslar\n— Bug'doy va javdar zakvaskasini boqish\n— Stretch & Fold texnikasi\n— Chiroyli non shakllantirish sirlari\n\n🔸 <b>Afzalliklar:</b>\n✅ Yangi boshlovchilar uchun ham mos\n✅ «Bratskiy Chat»da doimiy muloqot\n✅ Kuratorlar yordami\n✅ Kafolatlangan natija!\n\nHunaringizni biz bilan birga oshiring! ✨",
        'free': "🎁 <b>Bepul materiallar</b>\n\nFoydali maslahatlar va retseptlar kanalimizga obuna bo'ling: [LINK] 📢",
        'buy': "💎 <b>«ЗАКВАСКАЛИ НОН» kursiga yozilish</b>\n\n💵 <b>Kurs narxi:</b>\n❌ <s>1 000 000 so‘m</s>\n✅ <b>800 000 so‘m</b> 💸\n\n🛡 <i>Narx ichida:</i> barcha video darslar, yopiq chatga kirish va ekspertlar yordami.\n\n📍 <b>To'lov uchun:</b>\n<b>800 000 so‘m</b>ni quyidagi kartaga o'tkazing:\n💳 <code>{card_number}</code>\n\n📸 <b>TO'LOVDAN SO'NG:</b>\nAlbatta to'lov cheki rasmini (skrinshot) shu yerga yuboring, biz sizga kursga ruxsat beramiz! 👇",
        'waiting': "⏳ <b>Chekingiz qabul qilindi va tekshirishga yuborildi!</b>\n\nKuratorlarimiz bir soat ichida to'lovni tekshirishadi. Hammasi tasdiqlangach, sizga o'quv havolasini yuboraman! 🔔",
        'approved': "✅ <b>Tabriklaymiz!</b>\n\nTo'lovingiz muvaffaqiyatli tasdiqlandi. 🎉\nKursning yopiq kanaliga havola:\n\n🔗 {invite_link}\n\nXush kelibsiz! 🔥",
        'declined': "❌ <b>To'lov tasdiqlanmadi</b>\n\nAfsuski, biz to'lovingizni tasdiqlay olmadik. 😔 Iltimos, ma'lumotlarni tekshiring yoki yordam bo'limiga murojaat qiling: @support_handle",
        'admin_new': "🔔 <b>YANGI ARIZA</b>\n\nFoydalanuvchi: @{username}\nID: {user_id}\n\nIltimos, chekni tekshiring. 👇",
        'lang_selected': "✅ Til muvaffaqiyatli O'zbek tiliga o'zgartirildi!",
        'select_lang': "🌍 Выберите язык / Tilni tanlang:",
        'btn_about': "📚 Kurs haqida",
        'btn_free': "📢 Bepul kanal",
        'btn_buy': "💳 Sotib olish",
        'btn_admin': "👤 Admin",
        'sep': "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    }
}
