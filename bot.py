import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from murkups import ikb_next_step, ikb_answer_options
import config
import json
from functions import next_step


DATA = None
MEDIA = {}
json_file_path = "data.json"
if not DATA:
    with open(json_file_path, "r", encoding="UTF-8") as file:
        DATA = json.load(file)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(skip_updates=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    next_step_output = next_step()
    text = DATA[0].get("Текст")
    img = DATA[0].get("Картинка")
    next_step_method = DATA[0].get("Способ перехода к следующему шагу")

    await message.answer(f'Привет,{message.from_user.full_name}')
    await message.answer(text)

    if MEDIA.get(img):
        photo = MEDIA.get(img)
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    else:
        photo = FSInputFile(f"media\\{img}")
        result = await message.answer_photo(photo)
        photo_id = result.photo[-1].file_id
        MEDIA[img] = photo_id

    await message.answer(next_step_method, reply_markup=ikb_next_step(next_step_output))


@dp.callback_query(F.data.startswith("step_"))
async def cb_step(callback_query: types.CallbackQuery) -> None:
    if
    step = int(callback_query.data.replace("step_", ""))
    text = DATA[step].get("Текст")
    img = DATA[step].get("Картинка")
    link_on_video = DATA[step].get("Видео / ссылка")
    audio = DATA[step].get("Аудио")
    answer_options = DATA[step].get("Варианты ответов")
    next_step_method = DATA[step].get("Способ перехода к следующему шагу")

    if answer_options:
        await callback_query.message.answer(text, reply_markup=ikb_answer_options(answer_options, step))
    else:
        await callback_query.message.answer(text)
        if img:
            if MEDIA.get(img):
                photo = MEDIA.get(img)
                await callback_query.message.answer_photo(photo)
            else:
                photo = FSInputFile(f"media\\{img}")
                sent_photo = await callback_query.message.answer_photo(photo)
                photo_id = sent_photo.photo[-1].file_id
                MEDIA[img] = photo_id

        if link_on_video:
            await callback_query.message.answer(link_on_video)

        if audio:
            if MEDIA.get(audio):
                sound = MEDIA.get(img)
                await callback_query.message.answer_photo(sound)
            else:
                sound = FSInputFile(f"media\\{audio}")
                sent_audio = await callback_query.message.answer_audio(sound)
                audio_id = sent_audio.audio.file_id
                MEDIA[img] = audio_id

        ikb = ikb_next_step(next_step(step))
        if next_step_method == "Конец":
            ikb = None
        await callback_query.message.answer(next_step_method, reply_markup=ikb)


@dp.callback_query(F.data.startswith("answer_"))
async def cb_answer(callback_query: types.CallbackQuery) -> None:
    cb_data = callback_query.data.split("_")
    answer = cb_data[1]
    step = int(cb_data[2])
    correct_answer = DATA[step].get("Правильный ответ")
    correct_answer_reaction = DATA[step].get("Реакция на правильный ответ")
    incorrect_answer_reaction = DATA[step].get("Реакция на неправильный ответ")
    next_step_method = DATA[step].get("Способ перехода к следующему шагу")

    if answer == correct_answer:
        text = correct_answer_reaction
    else:
        text = incorrect_answer_reaction

    await callback_query.message.answer(text)
    await callback_query.message.answer(next_step_method, reply_markup=ikb_next_step(next_step(step)))


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
