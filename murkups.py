import cachetools
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ikb_next_step(next_step: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="*", callback_data=f"step_{next_step}")]
    ])

    return ikb


def ikb_answer_options(answer_options: str, step: int) -> InlineKeyboardMarkup:
    buttons = []
    for answer in answer_options.split(","):
        buttons.append([InlineKeyboardButton(text=answer, callback_data=f"answer_{answer}_{step}")])
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return ikb
