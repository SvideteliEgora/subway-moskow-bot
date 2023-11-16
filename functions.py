from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder


def data_converter(data: list) -> list[dict]:
    row_with_headers = data[0][:len(data[0]) - 2]
    rows_with_data = data[1:]
    deleted_value_indexes = []
    headers = ['id']
    for ind, header in enumerate(row_with_headers):
        if header:
            headers.append(header)
            continue
        deleted_value_indexes.append(ind)
    data_id = 1
    res = []
    for row in rows_with_data:
        data_dict = {}
        i = 0
        for del_ind, item in enumerate(row[:len(row) - 2]):
            if i == 0:
                data_dict[headers[i]] = data_id
            elif del_ind in deleted_value_indexes:
                continue
            else:
                data_dict[headers[i]] = item
            i += 1
        res.append(data_dict)
        data_id += 1
    return res


async def send_media(message, data: list[dict], media: dict, step: int) -> None:
    img = data[step].get("Картинка")
    video_link = data[step].get("Видео / ссылка")
    audio = data[step].get("Аудио")

    if img:
        photo_id = media.get(img)
        album_builder = MediaGroupBuilder()
        if photo_id:
            for i in photo_id:
                album_builder.add_photo(media=i)
            await message.answer_media_group(media=album_builder.build())
        else:
            for i in img.split(";"):
                photo = FSInputFile(f"media\\{i}")
                album_builder.add_photo(media=photo)
            sent_photos = await message.answer_media_group(media=album_builder.build())
            media[img] = [i.photo[-1].file_id for i in sent_photos]

    if video_link:
        await message.answer(video_link)

    if audio:
        audio_id = media.get(audio)
        if audio_id:
            await message.answer_audio(audio_id)
        else:
            sound = FSInputFile(f"media\\{audio}")
            sent_audio = await message.answer_audio(sound)
            audio_id = sent_audio.audio.file_id
            media[audio] = audio_id
