__version__ = (1, 2, 3)

#        █████  ██████   ██████ ███████  ██████  ██████   ██████ 
#       ██   ██ ██   ██ ██      ██      ██      ██    ██ ██      
#       ███████ ██████  ██      █████   ██      ██    ██ ██      
#       ██   ██ ██      ██      ██      ██      ██    ██ ██      
#       ██   ██ ██       ██████ ███████  ██████  ██████   ██████

#              © Copyright 2025
#           https://t.me/apcecoc
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @apcecoc
# scope: hikka_only
# scope: hikka_min 1.2.10

import aiohttp
import os
import asyncio
from telethon.tl.types import Message
from .. import loader, utils


@loader.tds
class TikTokDownloaderMod(loader.Module):
    """Download TikTok videos and audio using API"""

    strings = {
        "name": "TikTokDownloader",
        "processing": "🔄 <b>Fetching TikTok content...</b>",
        "invalid_url": "❌ <b>Invalid TikTok URL provided.</b>",
        "error": "❌ <b>Error occurred while processing your request. Retrying...</b>",
        "max_retries": "❌ <b>Failed to download after 3 attempts.</b>",
        "video_success": "🎥 <b>Video downloaded successfully:</b>",
        "audio_success": "🎵 <b>Audio downloaded successfully:</b>",
    }

    strings_ru = {
        "processing": "🔄 <b>Загружаю данные из TikTok...</b>",
        "invalid_url": "❌ <b>Указана недействительная ссылка TikTok.</b>",
        "error": "❌ <b>Произошла ошибка при обработке запроса. Повторяю...</b>",
        "max_retries": "❌ <b>Не удалось скачать после 3 попыток.</b>",
        "video_success": "🎥 <b>Видео успешно скачано:</b>",
        "audio_success": "🎵 <b>Аудио успешно скачано:</b>",
        "_cls_doc": "Скачивает видео и аудио из TikTok через API",
    }

    @loader.command(ru_doc="<Ссылка на TikTok> Скачать видео с TikTok или ответить на сообщение с ссылкой")
    async def tiktokvid(self, message: Message):
        """<TikTok Link> Download a TikTok video or reply to a message with a link"""
        await self._download_content(message, "video")

    @loader.command(ru_doc="<Ссылка на TikTok> Скачать аудио с TikTok или ответить на сообщение с ссылкой")
    async def tiktokaudio(self, message: Message):
        """<TikTok Link> Download TikTok audio or reply to a message with a link"""
        await self._download_content(message, "audio")

    async def _download_content(self, message: Message, content_type: str):
        args = utils.get_args_raw(message)
        if not args and message.is_reply:
            reply = await message.get_reply_message()
            args = reply.raw_text if reply and reply.raw_text else ""

        if not args or not args.startswith("http"):
            await utils.answer(message, self.strings("invalid_url"))
            return

        await utils.answer(message, self.strings("processing"))

        api_url = f"https://api.paxsenix.biz.id/dl/tiktok?url={args}"
        headers = {"accept": "*/*"}
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()

                            if not data.get("ok", False):
                                raise Exception("API returned unsuccessful response")

                            downloads = data.get("downloadUrls", {})
                            file_url = (
                                downloads.get("video_standard")
                                if content_type == "video"
                                else downloads.get("music")
                            )

                            if not file_url:
                                raise Exception("No download URL found")

                            async with session.get(file_url) as file_resp:
                                if file_resp.status == 200:
                                    file_name = file_url.split("/")[-1]
                                    file_path = f"/tmp/{file_name}"
                                    with open(file_path, "wb") as file:
                                        file.write(await file_resp.read())

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

                                    if os.path.exists(file_path):
                                        os.remove(file_path)

                                    await message.delete()
                                    return
                                else:
                                    raise Exception("Failed to download file")
                        else:
                            raise Exception("API request failed")
            except Exception as e:
                attempt += 1
                if attempt < max_retries:
                    await utils.answer(message, self.strings("error"))
                    await asyncio.sleep(1)
                else:
                    await utils.answer(message, self.strings("max_retries"))
                continue