import telebot 
from telebot import types 
import psycopg2
from config import host, user, password, db_name
import time
import utils

admin = 5359516739
variable = utils.Variable()
bot = telebot.TeleBot("6530283151:AAGIjz4ckeRUTa9znRu1aSVrlrDVEn2ZkDc")

@bot.message_handler(commands=['start'])
def stttt(message):
  k = types.InlineKeyboardMarkup()
  k1 = types.InlineKeyboardButton(text="WEB APP", web_app=types.WebAppInfo(url="https://main--dancing-cheesecake-968061.netlify.app"))
  k.add(k1)
  bot.send_message(message.chat.id, text= "Приложение тут", reply_markup=k)



@bot.message_handler(commands=['admin'])
def admmmmin(message):
  
  kb_ad = types.InlineKeyboardMarkup(row_width=2)
  k1 = types.InlineKeyboardButton(text="КУРС",callback_data="curs")
  k2 = types.InlineKeyboardButton(text="ТРЕК",callback_data="trek")   
  kb_ad.add(k1,k2) 
  bot.send_message(message.chat.id, "Вы попали в меню администратора\nИсползуйте кнопки ниже",reply_markup=kb_ad)

@bot.callback_query_handler(func = lambda call: True)
def print_all_commands(call): 
  if call.data == "curs":
    
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
    connection.autocommit = True

    # #     connection.commit()
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT course FROM yuan"""
        )    
        qe = (cursor.fetchone()[0])
        
    kb_change_curs = types.InlineKeyboardMarkup(row_width=1)
    k1 = types.InlineKeyboardButton(text="СМЕНА",callback_data="cc")
    k2 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_curs.add(k1,k2)
    bot.send_message(call.message.chat.id, f"Актуальный курс - {qe}",reply_markup=kb_change_curs)
    
  if call.data == "trek":
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k1 = types.InlineKeyboardButton(text="ДОБАВИТЬ",callback_data="at") 
    k2 = types.InlineKeyboardButton(text="ПОИСК",callback_data="ft") 
    k3 = types.InlineKeyboardButton(text="УДАЛИТЬ",callback_data="dt") 
    k4 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k1,k2,k3,k4)
    bot.send_message(call.message.chat.id, f"Меню Треккинга заказов",reply_markup=kb_change_trak)
  if call.data == "back":
    variable.set_action(call.message.chat.id, 0)
    kb_ad = types.InlineKeyboardMarkup(row_width=2)
    k1 = types.InlineKeyboardButton(text="КУРС",callback_data="curs")
    k2 = types.InlineKeyboardButton(text="ТРЕК",callback_data="trek")   
    kb_ad.add(k1,k2) 
    bot.send_message(call.message.chat.id, "Вы попали в меню администратора\nИсползуйте кнопки ниже",reply_markup=kb_ad)
  # Закончил выполнение меню панели, далее все идет на запросах к бд и используя varrible все работает кайф 
  if call.data == "dt":
    variable.set_action(call.message.chat.id, 5)
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    bot.send_message(call.message.chat.id, "Введите трек номер заказа для удаления трек номера",reply_markup=kb_change_trak)

  if call.data == "cc":
    variable.set_action(call.message.chat.id, 1)
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    bot.send_message(call.message.chat.id, "Введите новый курс",reply_markup=kb_change_trak)
  if call.data == "at":
    variable.set_action(call.message.chat.id, 2)
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    bot.send_message(call.message.chat.id, "Введите новый трек номер и его статус через пробел\n\nПример (AE14713894 1)\n\n1. Выкуплен, в пути склад\n2. Принят на складе, оформляется\n3. Заказ в пути\n4. Сортируется в Москве be\n5. Передан в СДЭК\n6. Получен клиентом",reply_markup=kb_change_trak)
  if call.data == "ft":
    variable.set_action(call.message.chat.id, 3)
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    bot.send_message(call.message.chat.id, "Введите трек номер заказа для смены статуса",reply_markup=kb_change_trak)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
  global treknom
  text = message.text
  action = int(variable.get_action(message.chat.id))


  if action == 1:
    curs = message.text
    connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name    
    )
    connection.autocommit = True
    try:
      with connection.cursor() as cursor:
          cursor.execute(
              f"""UPDATE yuan SET course = {message.text}"""
          )

      #     connection.commit()
      with connection.cursor() as cursor:
          cursor.execute(
              """SELECT course FROM yuan"""
          )    
          print(cursor.fetchone()[0])
          
          kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
          k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
          kb_change_trak.add(k3)
          bot.send_message(message.chat.id, f"Актуальный курс - {message.text}",reply_markup=kb_change_trak)
          variable.set_action(message.chat.id, 0)
    except:
      variable.set_action(message.chat.id, 1)
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      bot.send_message(message.chat.id, "Введите новый курс\nПример 13.5",reply_markup=kb_change_trak)
  
  
  if action == 2:
    try:
      trak = message.text.split(" ")[0]
      status = message.text.split(" ")[1]
      print(trak,status)
      connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name    
      )
      connection.autocommit = True
      try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT status FROM orders WHERE track = '{trak}'"""
            )
            a = cursor.fetchone()[0]
            variable.set_action(message.chat.id, 2)
            kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
            k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
            kb_change_trak.add(k3)
            bot.send_message(message.chat.id, "УЖЕ СУЩЕСТВУЕТ\nВведите новый трек номер и его статус через пробел\n\nПример (AE14713894 1)\n\n1. Выкуплен, в пути склад\n2. Принят на складе, оформляется\n3. Заказ в пути\n4. Сортируется в Москве be\n5. Передан в СДЭК\n6. Получен клиентом",reply_markup=kb_change_trak)
      except:
        with connection.cursor() as cursor:
            cursor.execute(
              f"""INSERT INTO orders (track,status) VALUES ('{trak}',{status})"""
            )



        variable.set_action(message.chat.id, 0)
        kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
        k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
        kb_change_trak.add(k3)
        bot.send_message(message.chat.id, "Успешно добавлен трек номер",reply_markup=kb_change_trak)


    except:
      variable.set_action(message.chat.id, 2)
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      bot.send_message(message.chat.id, "Введите новый трек номер и его статус через пробел\n\nПример (AE14713894 1)\n\n1. Выкуплен, в пути склад\n2. Принят на складе, оформляется\n3. Заказ в пути\n4. Сортируется в Москве be\n5. Передан в СДЭК\n6. Получен клиентом",reply_markup=kb_change_trak)
 
  if action == 3:
    try:
      # поиск по номеру заказа 
      connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name    
      )
      connection.autocommit = True
      trak = message.text
      treknom = message.text
      with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT status FROM orders WHERE track = '{trak}';"""
        )
        
        a = cursor.fetchone()
        print(a)
        kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
        k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
        kb_change_trak.add(k3)
        variable.set_action(message.chat.id, 4)
        bot.send_message(message.chat.id, f"трек номер {trak}\nСтатус - {a[0]}\nВведите новый статус заказа ",reply_markup=kb_change_trak)
    except:
      variable.set_action(message.chat.id, 3)
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      bot.send_message(message.chat.id, "Введите трек номер заказа для смены статуса",reply_markup=kb_change_trak)
  if action == 4:
    stat = message.text
    connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name    
    )
    connection.autocommit = True
    
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE orders SET status = {message.text} WHERE track = '{treknom}'"""
        )
    variable.set_action(message.chat.id, 0)
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    bot.send_message(message.chat.id, "Успешно добавлен трек номер",reply_markup=kb_change_trak)
  if action == 5:
    trak = message.text
    treknom = message.text
    try:
      # поиск по номеру заказа 
      connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name    
      )
      connection.autocommit = True
      
      with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT status FROM orders WHERE track = '{trak}';"""
        )
        a = cursor.fetchone()[0]
        cursor.execute(
            f"""DELETE FROM orders WHERE track = '{trak}';"""
        ) 
        kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
        k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
        kb_change_trak.add(k3)
        variable.set_action(message.chat.id, 0)
        bot.send_message(message.chat.id, f"УСПЕШНО УДАЛЕНО",reply_markup=kb_change_trak)
    except:
      variable.set_action(message.chat.id, 5)
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      bot.send_message(message.chat.id, "Введите трек номер заказа для удаления трек номера",reply_markup=kb_change_trak)


while True:
  try:
    bot.polling(non_stop=True)
  except:
    bot.stop_polling()
    time.sleep(5)

