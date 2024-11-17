__version__ = (1, 2, 1)

#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2024
#           https://t.me/apcecoc
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://example.com/tiktok_icon.png
# meta banner: https://example.com/tiktok_banner.jpg
# meta developer: @apcecoc
# scope: hikka_only
# scope: hikka_min 1.2.10

import aiohttp
from telethon.tl.types import Message
from telethon.utils import get_display_name
from .. import loader, utils

@loader.tds
class TikTokDownloaderMod(loader.Module):
    """Download TikTok videos and audio using API"""

    strings = {
        "name": "TikTokDownloader",
        "processing": "🔄 <b>Fetching TikTok content...</b>",
        "invalid_url": "❌ <b>Invalid TikTok URL provided.</b>",
        "error": "❌ <b>Error occurred while processing your request.</b>",
        "video_success": "🎥 <b>Video downloaded successfully:</b>",
        "audio_success": "🎵 <b>Audio downloaded successfully:</b>",
    }

    strings_ru = {
        "processing": "🔄 <b>Загружаю данные из TikTok...</b>",
        "invalid_url": "❌ <b>Указана недействительная ссылка TikTok.</b>",
        "error": "❌ <b>Произошла ошибка при обработке запроса.</b>",
        "video_success": "🎥 <b>Видео успешно скачано:</b>",
        "audio_success": "🎵 <b>Аудио успешно скачано:</b>",
        "_cls_doc": "Скачивает видео и аудио из TikTok через API",
    }

    @loader.command(ru_doc="<Ссылка на TikTok> Скачать видео с TikTok")
    async def tiktokvid(self, message: Message):
        """<TikTok Link> Download a TikTok video"""
        await self._download_content(message, "video")

    @loader.command(ru_doc="<Ссылка на TikTok> Скачать аудио с TikTok")
    async def tiktokaudio(self, message: Message):
        """<TikTok Link> Download TikTok audio"""
        await self._download_content(message, "audio")

    async def _download_content(self, message: Message, content_type: str):
        args = utils.get_args_raw(message)
        if not args or not args.startswith("http"):
            await utils.answer(message, self.strings("invalid_url"))
            return

        await utils.answer(message, self.strings("processing"))

        api_url = f"https://api.paxsenix.biz.id/dl/tiktok?url={args}"
        headers = {"accept": "*/*"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()

                        if not data.get("ok", False):
                            await utils.answer(message, self.strings("error"))
                            return

                        downloads = data.get("downloadsUrl", {})
                        file_url = (
                            downloads.get("video")
                            if content_type == "video"
                            else downloads.get("music")
                        )

                        if not file_url:
                            await utils.answer(message, self.strings("error"))
                            return

                        # Скачивание файла
                        async with session.get(file_url) as file_resp:
                            if file_resp.status == 200:
                                file_name = file_url.split("/")[-1]
                                file_path = f"/tmp/{file_name}"
                                with open(file_path, "wb") as file:
                                    file.write(await file_resp.read())

                                # Проверка размера файла
                                if file_resp.content_length is None or file_resp.content_length < 1:
                                    await utils.answer(message, self.strings("error"))
                                    return

                                caption = (
                                    self.strings("video_success")
                                    if content_type == "video"
                                    else self.strings("audio_success")
                                )

                                await message.client.send_file(
                                    message.peer_id,
                                    file_path,
                                    caption=caption,
                                )
                                await message.delete()
                            else:
                                await utils.answer(message, self.strings("error"))
                    else:
                        await utils.answer(message, self.strings("error"))
        except Exception as e:
            await utils.answer(message, self.strings("error"))
            raise e
