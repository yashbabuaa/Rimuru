from telethon import events, Button, types
from Rimuru import rimuru 
import youtube_dl
import logging
import os
import ffmpeg 
from youtube_search import YoutubeSearch
from telethon.utils import get_attributes

LOGS = logging.getLogger(__name__)

@rimuru.on(events.NewMessage(outgoing=True,pattern=r'^!s(.*)'))
async def songs(slime):
  opts = {
    "outtmpl": "%(title)s.mp3",
    "logger": LOGS,
    "writethumbnail": True,
    "format": "bestaudio/best",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
  }
  args = slime.message.text[2:]
  if args.startswith("https://"):
    url = args
  else:
    result = YoutubeSearch(args,max_results=1).to_dict()
    url = "https://youtu.be/" + result[0]['id']
  await slime.delete()
  print(url)
  with youtube_dl.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)
    dl = ydl.prepare_filename(info)
    ydl.download([url])
  m = await slime.respond("Download ho gaya, Ab uploading Chalu....")
  f = open(dl, 'rb')
  upload = await slime.client.upload_file(file=f)
  attributes, mime_type = get_attributes(str(dl))
  media = types.InputMediaUploadedDocument(
    file=upload,
    attributes=attributes,
    mime_type=mime_type,
    )
  async with rimuru.action(slime.chat_id, 'audio'):
    await rimuru.send_message(slime.chat_id, file=media, force_document=False)
  await m.delete()
  os.remove(dl)
