from aiogram import types

class key:
  start = types.ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=False).add('Cutt.ly', 'TinyURL.com').add('Da.gd', 'Is.gd').add('Bit.ly (📊статистика)')
  cut_menu = types.ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True).add('🛠Сменить сервис')
  cut_menu_stat = types.ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True).add('🛠Сменить сервис', '📊Статистика')
