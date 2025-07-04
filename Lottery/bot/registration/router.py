import random

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from registration.keyboard import get_check_subscribe_keyboard, get_sex_keyboard, lottery_keyboard
from registration.state import RegistrationState
from repository.user_repository import UserRepository
from schema.user import SexEnum, CreateUserSchema, UserSchema, UpdateUserSchema

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, repository = UserRepository()):
    user = await repository.get_one_by_tg_id(message.from_user.id)
    if user:
        await message.answer(text="Вы уже прошли этап регистрации")
    else:
        await message.answer(
            text=f"Привет {message.from_user.username}!\n\nЧтобы участвовать в розыгрыше убедись, что ты подписан на наш канал: https://t.me/molodnv ☺️",
            reply_markup=get_check_subscribe_keyboard())


@router.callback_query(F.data == "check_subscribe")
async def check_subscribe(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    member = await bot.get_chat_member("-1001858677023", callback.from_user.id)
    if member.status == 'left':
        await callback.answer(
            "К сожалению вы не подписались на указанные каналы. Подпишитесь и попробуйте еще раз",
            show_alert=True
        )
    else:
        await callback.message.answer(text="Увидел твою подписку! Давай продолжим знакомиться ☺️\nУкажите ваше имя")
        await state.set_state(RegistrationState.name)


@router.message(RegistrationState.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("А теперь укажите вашу фамилию")
    await state.set_state(RegistrationState.last_name)


@router.message(RegistrationState.last_name)
async def set_last_name(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer("Отлично! Последний этап - укажите ваш пол", reply_markup=get_sex_keyboard())
    await state.set_state(RegistrationState.sex)


@router.callback_query(RegistrationState.sex, F.data.startswith("sex_"))
async def set_sex(callback: CallbackQuery, state: FSMContext, repository = UserRepository()):
    await callback.answer()
    sex = callback.data.split("_")[1]
    if callback.data == "male":
        sex = SexEnum.male
    else:
        sex = SexEnum.female

    user_data = await state.get_data()
    user = CreateUserSchema(
        tg_id=callback.from_user.id,
        name=user_data['name'],
        last_name=user_data['last_name'],
        sex=sex
    )
    user = await repository.create(user)
    await state.clear()
    await callback.message.answer(f"Спасибо за регистрацию!\nВаш уникальный номер в розыгрыше: <b>{user.id}</b>!")
    await callback.message.answer(f"Ждем вас у сцены в момент розыгрыша. В случае выигрыша я уведомлю вас ️☺️")


@router.message(Command("count"))
async def count_users(message: Message, repository = UserRepository()):
    users = await repository.get_all()
    count = len(users)
    await message.answer(f"Зарегистрировано {count} человек")

@router.message(Command("Adm1n"))
async def admin_panel(message: Message):
    await message.answer(text="Добро пожаловать", reply_markup=lottery_keyboard())

@router.message(F.text == "Выявить победителя")
async def lottery(message: Message, repository = UserRepository(), bot = Bot):
    users = await repository.get_not_winners()
    users = [UserSchema.from_orm(user) for user in users]
    if len(users) == 0:
        await message.answer("Нет людей на розыгрыш")
    else:
        winner = random.choice(users)
        winner = await repository.update(winner.id, UpdateUserSchema(is_winner=True))
        sex = ""
        if winner.sex == "male":
            sex = "Мужской"
        else:
            sex = "Женский"
        await message.answer(f"Победитель\nНомер: {winner.id}\nИмя: {winner.name} {winner.last_name}\nПол: {sex}")
        try:
            await bot.send_message(chat_id=winner.tg_id, text="Поздравляю! Вы выиграли в розыгрыше, прошу подойти к сцене!")
        except:
            pass

