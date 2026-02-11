#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install python-telegram-bot==13.15

import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# ================= НАСТРОЙКИ =================

TOKEN = os.environ.get("TOKEN")
MANAGER_USERNAME = "katemirrel"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= КАТАЛОГ (ВСЕ 13 ПОЗИЦИЙ) =================

catalog = {
    "новинки": {
        "футболка_citcit": {
            "название": "Детская футболка CitCit (Турция)",
            "цена": "380₽",
            "фото": "https://ibb.co/SDMPWSk5",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Гипоаллергенная, дышащая, принт устойчив к стиркам",
            "размеры": {
                "92 (2 года)": "✅",
                "98 (3 года)": "✅",
                "104 (4 года)": "✅",
                "110 (5 лет)": "✅"
            }
        },
        "футболка_baitatex": {
            "название": "Детская футболка Baitatex",
            "цена": "370₽",
            "фото": "https://ibb.co/1Ys3BdVm",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Мягкая, идеальна для жары",
            "размеры": {
                "86 (1-2 года)": "✅",
                "92 (2-3 года)": "✅",
                "98 (3-4 года)": "✅",
                "104 (4-5 лет)": "✅"
            }
        },
        "поло_silversun": {
            "название": "Рубашка-поло Silversun",
            "цена": "480₽",
            "фото": "https://ibb.co/hJXXHPc2",
            "состав": "100% хлопок",
            "особенности": "Стильный дизайн, летний вариант",
            "размеры": {
                "128": "✅",
                "140": "✅",
                "152": "✅"
            }
        },
        "футболка_galilatex": {
            "название": "Футболка Galilatex с динозавром",
            "цена": "330₽",
            "фото": "https://ibb.co/HDj4Dq5j",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Мягкая, эластичная",
            "размеры": {
                "86": "✅",
                "92": "✅",
                "98": "✅",
                "104": "✅"
            }
        },
        "футболка_cegisa_olive": {
            "название": "Футболка Cegisa оливковая",
            "цена": "770₽",
            "фото": "https://ibb.co/Kcw0brb1",
            "состав": "100% хлопок",
            "особенности": "Модный цвет, прямой крой",
            "размеры": {
                "92": "✅",
                "98": "✅",
                "104": "✅",
                "110": "✅"
            }
        },
        "халат_miniworld": {
            "название": "Банный халат MiniWorld",
            "цена": "900₽",
            "фото": "https://ibb.co/3yPNfCJj",
            "состав": "100% хлопок",
            "особенности": "Махровый, с капюшоном",
            "размеры": {
                "86": "✅",
                "92": "✅",
                "98": "✅",
                "104": "✅"
            }
        },
        "футболка_starfilex": {
            "название": "Футболка Starfilex с платьем",
            "цена": "520₽",
            "фото": "https://ibb.co/cScq1kG4",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Съёмное платье на липучке",
            "размеры": {
                "104": "✅",
                "110": "✅",
                "116": "✅",
                "122": "✅"
            }
        },
        "поло_blueland": {
            "название": "Поло Blueland красное",
            "цена": "380₽",
            "фото": "https://ibb.co/C3KD0tyG",
            "состав": "95% хлопок + 5% лайкра",
            "особенности": "Классическое поло",
            "размеры": {
                "110": "✅",
                "116": "✅",
                "122": "✅",
                "128": "✅"
            }
        }
    },
    "eckin": {
        "футболка_жираф": {
            "название": "ECKIN с жирафом",
            "цена": "450₽",
            "фото": "https://ibb.co/5WHBwWq7",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Принт не линяет",
            "размеры": {
                "86": "✅",
                "92": "✅",
                "98": "✅",
                "104": "✅"
            }
        },
        "футболка_динозавр": {
            "название": "ECKIN с динозавром",
            "цена": "620₽",
            "фото": "https://ibb.co/9kFCs75b",
            "состав": "95% хлопок + 5% эластан",
            "особенности": "Свободная посадка",
            "размеры": {
                "104": "✅",
                "110": "✅",
                "116": "✅",
                "122": "✅",
                "128": "✅"
            }
        }
    },
    "cegisa": {
        "подростковая_принт": {
            "название": "Подростковая Cegisa",
            "цена": "590₽",
            "фото": "https://ibb.co/kkBkdQr",
            "состав": "100% хлопок",
            "особенности": "Принт на груди и спине",
            "размеры": {
                "140": "✅",
                "146": "✅",
                "152": "✅"
            }
        },
        "оверсайз": {
            "название": "Cegisa оверсайз",
            "цена": "630₽",
            "фото": "https://ibb.co/bcP9BJX",
            "состав": "100% хлопок",
            "особенности": "Оверсайз крой",
            "размеры": {
                "140": "✅",
                "146": "✅",
                "152": "✅"
            }
        }
    },
    "first_kids": {
        "деним": {
            "название": "First Kids деним",
            "цена": "580₽",
            "фото": "https://ibb.co/kg9bRZzN",
            "состав": "100% хлопок",
            "особенности": "Стиль деним",
            "размеры": {
                "134": "✅",
                "140": "✅",
                "146": "✅",
                "152": "✅"
            }
        }
    }
}

# ================= ИНФОРМАЦИЯ О ДОСТАВКЕ =================

delivery_info = """
🚚 **Условия доставки LaleKids:**

📍 **Самовывоз:** г. Санкт-Петербург, м. Московская, м. Электросила, м. Парк Победы - ежедневно по договоренности
🚗 **Курьер по Санкт-Петербургу:** от 15000₽, 1-2 дня
📦 **Почта России:** от 500₽, 3-7 дней
🚀 **СДЭК, Яндекс доставка:** от 1000₽, 2-5 дней

💰 **Бесплатная доставка** при заказе от 5000₽


❓ **Возврат:** В течение 14 дней, товар должен быть с бирками
"""


# ================= ФУНКЦИИ =================

def build_text(item):
    text = f"*{item['название']}*\n\n"
    text += f"💰 {item['цена']}\n"
    text += f"📦 {item['состав']}\n"
    text += f"✨ {item['особенности']}\n\n"
    text += "📏 *Размеры и наличие:*\n"
    
    for size, status in item["размеры"].items():
        text += f"• {size} — {status}\n"
    
    return text

def send_product(query, category, item_id):
    """Отправить товар с фотографией"""
    item = catalog[category][item_id]
    
    keyboard = [
        [InlineKeyboardButton("🛒 Заказать", url=f"https://t.me/{MANAGER_USERNAME}")],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"category_{category}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        query.message.delete()
    except:
        pass
    
    query.message.reply_photo(
        photo=item["фото"],
        caption=build_text(item),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ================= СТАРТОВОЕ МЕНЮ (ПОЛНОЕ) =================

def start(update: Update, context: CallbackContext):
    """Главное меню со всеми разделами"""
    user = update.effective_user
    first_name = user.first_name if user.first_name else "покупатель"
    
    welcome_text = f"""
👋 Добро пожаловать в **LaleKids** — магазин детской одежды из Турции!

Рады видеть тебя, {first_name}! 🎀

У нас только качественный турецкий трикотаж:
• ECKIN • CitCit • Cegisa • Silversun • Baitatex • First Kids • MiniWorld • Starfilex • Galilatex • Blueland

Что бы ты хотел(а) посмотреть?
    """
    
    keyboard = [
        [InlineKeyboardButton("🔥 НОВИНКИ", callback_data="novinki")],
        [InlineKeyboardButton("👕 ECKIN (Турция)", callback_data="brand_eckin"),
         InlineKeyboardButton("👕 Cegisa (Турция)", callback_data="brand_cegisa")],
        [InlineKeyboardButton("👕 CitCit & Baitatex", callback_data="brand_citcit_baitatex"),
         InlineKeyboardButton("👕 Другие бренды", callback_data="brand_others")],
        [InlineKeyboardButton("📏 Подобрать по возрасту", callback_data="age_search")],
        [InlineKeyboardButton("📏 Подобрать по размеру", callback_data="size_search")],
        [InlineKeyboardButton("🧖‍♂️ Банные халаты", callback_data="category_halaty")],
        [InlineKeyboardButton("👕 Поло", callback_data="category_polo")],
        [InlineKeyboardButton("🚚 Доставка и оплата", callback_data="delivery")],
        [InlineKeyboardButton("📞 Связаться с менеджером", url=f"https://t.me/{MANAGER_USERNAME}")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        try:
            update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
        except:
            update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= НОВИНКИ =================

def show_novinki(update: Update, context: CallbackContext):
    """Показать все новинки"""
    query = update.callback_query
    query.answer()
    
    text = "🔥 **НАШИ НОВИНКИ** 🔥\n\n"
    keyboard = []
    
    for item_id, item in catalog["новинки"].items():
        text += f"**{item['название']}**\n"
        text += f"💰 {item['цена']}\n"
        text += f"✨ {item['особенности'][:50]}...\n"
        text += "📏 В наличии: "
        sizes = list(item["размеры"].keys())
        text += f"{len(sizes)} размеров\n\n"
        
        keyboard.append([InlineKeyboardButton(f"🛒 {item['название']}", 
                                             callback_data=f"item_новинки_{item_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= БРЕНДЫ =================

def show_brand_eckin(update: Update, context: CallbackContext):
    """Показать товары ECKIN"""
    query = update.callback_query
    query.answer()
    
    text = "👕 **БРЕНД ECKIN (Турция)**\n\n"
    keyboard = []
    
    for item_id, item in catalog["eckin"].items():
        text += f"**{item['название']}**\n"
        text += f"💰 {item['цена']}\n"
        text += f"✨ {item['особенности']}\n"
        text += "📏 Размеры: "
        sizes = list(item["размеры"].keys())
        text += f"{', '.join(sizes[:3])}...\n\n"
        
        keyboard.append([InlineKeyboardButton(f"🛒 {item['название']}", 
                                             callback_data=f"item_eckin_{item_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_brand_cegisa(update: Update, context: CallbackContext):
    """Показать товары Cegisa"""
    query = update.callback_query
    query.answer()
    
    text = "👕 **БРЕНД Cegisa (Турция)**\n\n"
    keyboard = []
    
    for item_id, item in catalog["cegisa"].items():
        text += f"**{item['название']}**\n"
        text += f"💰 {item['цена']}\n"
        text += f"✨ {item['особенности']}\n"
        text += f"📏 Размеры: {', '.join(item['размеры'].keys())}\n\n"
        
        keyboard.append([InlineKeyboardButton(f"🛒 {item['название']}", 
                                             callback_data=f"item_cegisa_{item_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_brand_citcit_baitatex(update: Update, context: CallbackContext):
    """Показать товары CitCit и Baitatex"""
    query = update.callback_query
    query.answer()
    
    text = "👕 **БРЕНДЫ CitCit и Baitatex**\n\n"
    keyboard = []
    
    # CitCit
    citcit = catalog["новинки"]["футболка_citcit"]
    text += f"**{citcit['название']}**\n"
    text += f"💰 {citcit['цена']}\n"
    text += f"✨ {citcit['особенности']}\n"
    text += f"📏 Размеры: {', '.join(citcit['размеры'].keys())}\n\n"
    
    # Baitatex
    baitatex = catalog["новинки"]["футболка_baitatex"]
    text += f"**{baitatex['название']}**\n"
    text += f"💰 {baitatex['цена']}\n"
    text += f"✨ {baitatex['особенности']}\n"
    text += f"📏 Размеры: {', '.join(baitatex['размеры'].keys())}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🛒 CitCit", callback_data="item_новинки_футболка_citcit")],
        [InlineKeyboardButton("🛒 Baitatex", callback_data="item_новинки_футболка_baitatex")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_brand_others(update: Update, context: CallbackContext):
    """Показать другие бренды"""
    query = update.callback_query
    query.answer()
    
    text = "👕 **ДРУГИЕ БРЕНДЫ**\n\n"
    keyboard = []
    
    # First Kids
    first_kids = catalog["first_kids"]["деним"]
    text += f"**{first_kids['название']}**\n"
    text += f"💰 {first_kids['цена']}\n"
    text += f"✨ {first_kids['особенности']}\n"
    text += f"📏 Размеры: {', '.join(first_kids['размеры'].keys())}\n\n"
    
    # Starfilex
    starfilex = catalog["новинки"]["футболка_starfilex"]
    text += f"**{starfilex['название']}**\n"
    text += f"💰 {starfilex['цена']}\n"
    text += f"✨ {starfilex['особенности']}\n"
    text += f"📏 Размеры: {', '.join(starfilex['размеры'].keys())}\n\n"
    
    # Galilatex
    galilatex = catalog["новинки"]["футболка_galilatex"]
    text += f"**{galilatex['название']}**\n"
    text += f"💰 {galilatex['цена']}\n"
    text += f"✨ {galilatex['особенности']}\n"
    text += f"📏 Размеры: {', '.join(galilatex['размеры'].keys())}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🛒 First Kids деним", callback_data="item_first_kids_деним")],
        [InlineKeyboardButton("🛒 Starfilex с платьем", callback_data="item_новинки_футболка_starfilex")],
        [InlineKeyboardButton("🛒 Galilatex динозавр", callback_data="item_новинки_футболка_galilatex")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= КАТЕГОРИИ: ХАЛАТЫ И ПОЛО =================

def show_halaty(update: Update, context: CallbackContext):
    """Показать банные халаты"""
    query = update.callback_query
    query.answer()
    
    text = "🧖‍♂️🧖‍♀️ **ДЕТСКИЕ БАННЫЕ ХАЛАТЫ**\n\n"
    
    item = catalog["новинки"]["халат_miniworld"]
    text += f"**{item['название']}**\n"
    text += f"💰 {item['цена']}\n"
    text += f"✨ {item['особенности']}\n"
    text += f"📏 Размеры: {', '.join(item['размеры'].keys())}\n"
    text += f"📦 Наличие: {len(item['размеры'])} размера\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🛒 Заказать халат", callback_data="item_новинки_халат_miniworld")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_polo(update: Update, context: CallbackContext):
    """Показать поло"""
    query = update.callback_query
    query.answer()
    
    text = "👕 **СТИЛЬНЫЕ ПОЛО**\n\n"
    keyboard = []
    
    # Поло Silversun
    polo1 = catalog["новинки"]["поло_silversun"]
    text += f"**{polo1['название']}**\n"
    text += f"💰 {polo1['цена']}\n"
    text += f"✨ {polo1['особенности']}\n"
    text += f"📏 Размеры: {', '.join(polo1['размеры'].keys())}\n\n"
    
    # Поло Blueland
    polo2 = catalog["новинки"]["поло_blueland"]
    text += f"**{polo2['название']}**\n"
    text += f"💰 {polo2['цена']}\n"
    text += f"✨ {polo2['особенности']}\n"
    text += f"📏 Размеры: {', '.join(polo2['размеры'].keys())}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🛒 Поло Silversun", callback_data="item_новинки_поло_silversun")],
        [InlineKeyboardButton("🛒 Поло Blueland", callback_data="item_новинки_поло_blueland")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= ПОИСК ПО ВОЗРАСТУ =================

def age_search(update: Update, context: CallbackContext):
    """Поиск по возрасту"""
    query = update.callback_query
    query.answer()
    
    ages = ["1 год", "2 года", "3 года", "4 года", "5 лет", "6 лет", "7 лет", "8 лет", "9-10 лет", "10-11 лет", "11-12 лет", "12-13 лет"]
    
    text = "📏 **ПОДБОР ПО ВОЗРАСТУ**\n\nВыбери возраст ребенка:"
    keyboard = []
    
    row = []
    for age in ages:
        row.append(InlineKeyboardButton(age, callback_data=f"age_{age}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_by_age(update: Update, context: CallbackContext):
    """Показать товары по возрасту"""
    query = update.callback_query
    query.answer()
    
    age = query.data.replace("age_", "")
    found_items = []
    
    # Ищем по всему каталогу
    for brand, categories in catalog.items():
        if isinstance(categories, dict):
            for item_id, item in categories.items():
                if isinstance(item, dict) and "размеры" in item:
                    for size in item["размеры"].keys():
                        if age in size or age.replace(" ", "") in size.replace(" ", ""):
                            found_items.append({
                                "brand": brand,
                                "item": item,
                                "item_id": item_id,
                                "size": size
                            })
    
    if not found_items:
        text = f"😔 На возраст {age} сейчас нет товаров в наличии.\n\nПопробуй другой возраст или уточни у менеджера!"
        keyboard = [
            [InlineKeyboardButton("📞 Связаться с менеджером", url=f"https://t.me/{MANAGER_USERNAME}")],
            [InlineKeyboardButton("🔙 Назад к возрастам", callback_data="age_search")]
        ]
    else:
        text = f"📏 **Товары для возраста {age}:**\n\n"
        keyboard = []
        
        for item in found_items[:5]:
            text += f"**{item['item']['название']}**\n"
            text += f"💰 {item['item']['цена']}\n"
            text += f"📏 Размер: {item['size']}\n"
            text += f"📦 Наличие: {item['item']['размеры'][item['size']]}\n\n"
            
            callback = f"item_{item['brand']}_{item['item_id']}"
            keyboard.append([InlineKeyboardButton(f"🛒 Заказать", callback_data=callback)])
        
        keyboard.append([InlineKeyboardButton("🔙 Другие возраста", callback_data="age_search")])
    
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= ПОИСК ПО РАЗМЕРУ =================

def size_search(update: Update, context: CallbackContext):
    """Поиск по размеру"""
    query = update.callback_query
    query.answer()
    
    sizes = ["86", "92", "98", "104", "110", "116", "122", "128", "134", "140", "146", "152"]
    
    text = "📏 **ПОДБОР ПО РАЗМЕРУ**\n\nВыбери размер ребенка (рост в см):"
    keyboard = []
    
    row = []
    for size in sizes:
        row.append(InlineKeyboardButton(size, callback_data=f"size_{size}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def show_by_size(update: Update, context: CallbackContext):
    """Показать товары по размеру"""
    query = update.callback_query
    query.answer()
    
    size = query.data.replace("size_", "")
    found_items = []
    
    # Ищем по всему каталогу
    for brand, categories in catalog.items():
        if isinstance(categories, dict):
            for item_id, item in categories.items():
                if isinstance(item, dict) and "размеры" in item:
                    for item_size in item["размеры"].keys():
                        if size in item_size:
                            found_items.append({
                                "brand": brand,
                                "item": item,
                                "item_id": item_id,
                                "size": item_size
                            })
    
    if not found_items:
        text = f"😔 На размер {size} см сейчас нет товаров в наличии.\n\nПопробуй другой размер!"
        keyboard = [
            [InlineKeyboardButton("🔙 Назад к размерам", callback_data="size_search")]
        ]
    else:
        text = f"📏 **Товары размера {size} см:**\n\n"
        keyboard = []
        
        for item in found_items[:5]:
            text += f"**{item['item']['название']}**\n"
            text += f"💰 {item['item']['цена']}\n"
            text += f"📏 Полный размер: {item['size']}\n"
            text += f"📦 {item['item']['размеры'][item['size']]}\n\n"
            
            callback = f"item_{item['brand']}_{item['item_id']}"
            keyboard.append([InlineKeyboardButton(f"🛒 Заказать", callback_data=callback)])
        
        keyboard.append([InlineKeyboardButton("🔙 Другие размеры", callback_data="size_search")])
    
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ================= ДОСТАВКА =================

def show_delivery(update: Update, context: CallbackContext):
    """Информация о доставке"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📞 Задать вопрос о доставке", url=f"https://t.me/{MANAGER_USERNAME}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(delivery_info, reply_markup=reply_markup, parse_mode="Markdown")

# ================= КАТЕГОРИИ ТОВАРОВ =================

def show_category(update: Update, context: CallbackContext):
    """Показать товары в категории (бренде)"""
    query = update.callback_query
    query.answer()
    
    category = query.data.replace("category_", "")
    
    # Специальные категории
    if category == "halaty":
        show_halaty(update, context)
        return
    elif category == "polo":
        show_polo(update, context)
        return
    
    # Проверяем, существует ли такая категория
    if category not in catalog:
        start(update, context)
        return
    
    keyboard = []
    
    for item_id, item in catalog[category].items():
        keyboard.append([
            InlineKeyboardButton(item["название"], callback_data=f"item_{category}_{item_id}")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Удаляем старое сообщение и отправляем новое
    try:
        query.message.delete()
    except:
        pass
    
    query.message.reply_text(
        f"**{category.upper()}**\n\nВыберите товар:", 
        reply_markup=reply_markup, 
        parse_mode="Markdown"
    )

# ================= ПОКАЗ ТОВАРА (ДОБАВЛЕННАЯ ФУНКЦИЯ) =================

def show_item(update: Update, context: CallbackContext):
    """Показать конкретный товар с фото"""
    query = update.callback_query
    query.answer()
    
    # Разбираем callback_data: item_категория_id_товара
    parts = query.data.split("_", 2)
    if len(parts) < 3:
        return
    
    category = parts[1]
    item_id = parts[2]
    
    # Проверяем, существует ли такая категория и товар
    if category in catalog and item_id in catalog[category]:
        send_product(query, category, item_id)
    else:
        # Если товар не найден, показываем главное меню
        start(update, context)

# ================= ЗАПУСК БОТА =================

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Команды
    dp.add_handler(CommandHandler("start", start))
    
    # Навигация
    dp.add_handler(CallbackQueryHandler(start, pattern="^start$"))
    dp.add_handler(CallbackQueryHandler(show_novinki, pattern="^novinki$"))
    dp.add_handler(CallbackQueryHandler(show_brand_eckin, pattern="^brand_eckin$"))
    dp.add_handler(CallbackQueryHandler(show_brand_cegisa, pattern="^brand_cegisa$"))
    dp.add_handler(CallbackQueryHandler(show_brand_citcit_baitatex, pattern="^brand_citcit_baitatex$"))
    dp.add_handler(CallbackQueryHandler(show_brand_others, pattern="^brand_others$"))
    dp.add_handler(CallbackQueryHandler(show_halaty, pattern="^category_halaty$"))
    dp.add_handler(CallbackQueryHandler(show_polo, pattern="^category_polo$"))
    dp.add_handler(CallbackQueryHandler(show_category, pattern="^category_"))
    dp.add_handler(CallbackQueryHandler(show_item, pattern="^item_"))  # теперь функция определена!
    
    # Поиск
    dp.add_handler(CallbackQueryHandler(age_search, pattern="^age_search$"))
    dp.add_handler(CallbackQueryHandler(show_by_age, pattern="^age_"))
    dp.add_handler(CallbackQueryHandler(size_search, pattern="^size_search$"))
    dp.add_handler(CallbackQueryHandler(show_by_size, pattern="^size_"))
    
    # Информация
    dp.add_handler(CallbackQueryHandler(show_delivery, pattern="^delivery$"))
    
    updater.start_polling()
    logger.info("Бот LaleKids с полным меню запущен!")
    updater.idle()

if __name__ == "__main__":
    main()


# In[2]:


# СОЗДАЁМ ФАЙЛ requirements.txt
with open('requirements.txt', 'w') as f:
    f.write('python-telegram-bot==13.15\n')


# In[3]:


# СОЗДАЁМ ФАЙЛ Procfile (без расширения)
with open('Procfile', 'w') as f:
    f.write('web: python lale_kids_bot.py\n')

