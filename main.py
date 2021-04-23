#!/usr/bin/python3
# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from keyboard import key
from shorteners import short
from sqldata import sqldata
import config, logging, time

dp = Dispatcher(bot := Bot(token=config.API_BOT))
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.INFO, filename='cutter_bot.log', format="%(asctime)s [%(levelname)s] %(message)s")
#logging.getLogger().addHandler(logging.StreamHandler())
db = sqldata('cuter_db.db')
db.init_bd()
kb = key()
s = short()

@dp.message_handler(text=['🛠Сменить сервис'])
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  db.add_user(message.from_user.id,message.from_user.first_name,message.from_user.full_name,message.from_user.username,message.from_user.language_code,time.time(),time.time())
  db.insert_cutter(message.from_user.id,'None')
  db.add_last_date(time.time(),message.from_user.id)
  print(message.date, message.from_user.id, message.from_user.first_name, message.text)
  await bot.send_message(98684080, f"{message.date}, {message.from_user.id}, {message.from_user.first_name}, {message.text}", parse_mode= 'HTML')
  await message.answer("✂️Для начала работы с ботом выберете сервис. \n\nВыбранное имя(<b>URL</b>) сервиса будет в начале короткого имени.\nСервис <b>Bit.ly</b> поддерживает статистику по кликам! ", parse_mode= 'HTML', reply_markup=kb.start)

@dp.message_handler(text=['Cutt.ly', 'TinyURL.com', 'Da.gd', 'Is.gd', 'Bit.ly (📊статистика)'])
async def cutter_menu(message: types.Message):
  if message.text == 'Bit.ly (📊статистика)':
    db.insert_cutter(message.from_user.id,'Bit.ly')
  else:
    db.insert_cutter(message.from_user.id,message.text)

  print(message.date, message.from_user.id, message.from_user.first_name, message.text)
  await bot.send_message(98684080, f"{message.date}, {message.from_user.id}, {message.from_user.first_name}, {message.text}", parse_mode= 'HTML')
  keyboard = kb.cut_menu_stat if message.text == 'Bit.ly (📊статистика)' else kb.cut_menu
  await message.answer(f"Текущий сервис для укорачивания ссылок: {message.text} \n\nВведите <b>URL</b> который хотите <b>укоротить/распаковать</b> и отправьте его боту (<b>URL</b> должен начинаться с символов: <b>HTTP</b>, или <b>HTTPS</b>): ", parse_mode= 'HTML', reply_markup=keyboard)

@dp.message_handler(text=['📊Статистика'])
async def cutter_menu(message: types.Message):
    urls = db.select_stat_url(message.from_user.id,db.select_cutter(message.from_user.id)[1])
    result = ""
    for x in urls:
      result += x[0]+"  |  "+str(s.bitly(config.API_BITLY, x[0], 'clicks'))+'  |  '+time.strftime('%Y-%m-%d', time.localtime(float(x[1])-3600*3))+'\n'

    await message.answer(f"Ваша статистика по кликам сервиса: <b>Bit.ly</b>\n<b>URL</b>  |  <b>Кол-во кликов</b>  |  <b>Дата создания</b>\n{result}", parse_mode= 'HTML', disable_web_page_preview = True, reply_markup=kb.cut_menu_stat)

@dp.message_handler()
async def cutter_menu(message: types.Message):
  db.add_last_date(time.time(),message.from_user.id)
  print(message.date, message.from_user.id, message.from_user.first_name, message.text)
  await bot.send_message(98684080, f"{message.date}, {message.from_user.id}, {message.from_user.first_name}, {message.text}", parse_mode= 'HTML')
  service = db.select_cutter(message.from_user.id)[1]
  if service == 'None':
    return await message.answer("❗️Необходимо выбрать сервис, перед тем как начинать укорачивать ссылки(<b>URL</b>)", parse_mode= 'HTML')

  if len(message.text) < 6:
    return await message.answer("❗️Cсылка(<b>URL</b>) слишком короткая (минимум 6 символов).", parse_mode= 'HTML')

  if message.text.startswith('@'):
    message.text = f"https://t.me/{message.text[1:]}"

  if s.valid(message.text):
    print(message.text)
    print(service)
    txt = s.tinyurl(message.text)
    if len(message.text) < 6:
      return await message.answer("❗️Cсылка(<b>URL</b>) слишком короткая.", parse_mode= 'HTML')

    if 'cutt.ly' in message.text.lower():
      await message.answer("Развёрнутая ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(s.cuttly(config.API_CUTTLY, config.URL_CUTTLY, message.text), disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if message.text.lower().count('/') == 3 and txt.lower() != message.text.lower():
      await message.answer("Развёрнутая ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(txt, disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if service == 'Cutt.ly':
      await message.answer("Ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(s.cuttly(config.API_CUTTLY, config.URL_CUTTLY, message.text, act = 'short'), disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if service == "TinyURL.com":
      await message.answer("Ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(s.tinyurl(message.text, act = 'short'), disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if service == "Da.gd":
      await message.answer("Ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(s.dagd(message.text, act = 'short'), disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if service == "Is.gd":
      await message.answer("Ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      return await message.answer(s.isgd(message.text, act = 'short'), disable_web_page_preview = True, reply_markup=kb.cut_menu)

    if service == "Bit.ly":
      print(service)
      await message.answer("Ссылка готова!", disable_web_page_preview = True, reply_markup=kb.cut_menu)
      to_url = s.bitly(config.API_BITLY, message.text, act = 'short')
      db.add_stat_url(message.from_user.id,service,to_url,time.time())
      return await message.answer(to_url, disable_web_page_preview = True, reply_markup=kb.cut_menu_stat)

  else:
    return await message.answer("❗️Бот не может распознать команду, возможно некорректно введён <b>URL</b>.\nURL должен начинаться с символов: HTTP, или HTTPS.", disable_web_page_preview = True, parse_mode= 'HTML')

if __name__ == '__main__':
#	dp.loop.create_task(scheduled(10))
	executor.start_polling(dp, skip_updates=False)
