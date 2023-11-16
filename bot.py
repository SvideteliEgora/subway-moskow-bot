import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import gspread
from functions import data_converter, send_media

# get data from google sheets
gc = gspread.service_account(filename="venv/calm-vine-332204-924334d7332a.json")
sh_connection = gc.open_by_url('https://docs.google.com/spreadsheets/d/1fUu3aU7DhJoZl6X_KAX0GQVGvhqCW9f5iI0GbPPI5OA/edit')
worksheet1 = sh_connection.sheet1
list_of_lists = worksheet1.get_all_values()

data_gs = data_converter(list_of_lists)
media_dict = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(skip_updates=True)


# murkups
def ikb_next_step(next_step: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="*", callback_data=f"step_{next_step}")]
    ])

    return ikb


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    step = 0
    text = data_gs[step].get("Текст")
    next_step_method = data_gs[step].get("Способ перехода к следующему шагу")
    await message.answer(f'Привет,{message.from_user.full_name}')
    await message.answer(text)
    await send_media(message, data_gs, media_dict, step)
    await message.answer(next_step_method, reply_markup=ikb_next_step(step + 1))


@dp.callback_query(F.data.startswith("step_"))
async def cb_step(callback_query: types.CallbackQuery) -> None:
    step = int(callback_query.data.replace("step_", ""))
    text = data_gs[step].get("Текст")
    answer_options = data_gs[step].get("Варианты ответов")
    next_step_method = data_gs[step].get("Способ перехода к следующему шагу")
    if answer_options:
        buttons = []
        for answer in answer_options.split(","):
            buttons.append([InlineKeyboardButton(text=answer, callback_data=f"answer_{answer}_{step}")])
        ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback_query.message.answer(text, reply_markup=ikb)
        return
    await callback_query.message.answer(text)
    await send_media(callback_query.message, data_gs, media_dict, step)
    ikb = ikb_next_step(step + 1)
    if next_step_method == "Конец":
        ikb = None
    await callback_query.message.answer(next_step_method, reply_markup=ikb)


@dp.callback_query(F.data.startswith("answer_"))
async def cb_answer(callback_query: types.CallbackQuery) -> None:
    cb_data = callback_query.data.split("_")
    answer = cb_data[1]
    step = int(cb_data[2])
    correct_answer = data_gs[step].get("Правильный ответ")
    correct_answer_reaction = data_gs[step].get("Реакция на правильный ответ")
    incorrect_answer_reaction = data_gs[step].get("Реакция на неправильный ответ")
    next_step_method = data_gs[step].get("Способ перехода к следующему шагу")

    text = correct_answer_reaction if answer == correct_answer else incorrect_answer_reaction

    await callback_query.message.answer(text)
    await callback_query.message.answer(next_step_method, reply_markup=ikb_next_step(step + 1))


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
