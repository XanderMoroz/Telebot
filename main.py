import telebot                                   # Модуль из библиотеки pytelegrambotapi для создания бота.
from config import exchanges, TOKEN              # Импорт из собственного файла 'config' с константами.
from extensions import Convertor, APIException   # Импорт из собственного файла 'extensions' с исключениями и классами.
bot = telebot.TeleBot(TOKEN)                     # Инициализация бота.

@bot.message_handler(commands=['start', 'help']) # Обработчик сообщений. Реагирует на команды 'start', 'help'.
def start(message: telebot.types.Message):
    text = "Здравствуйте! Чтобы начать работу введите команду в следующем формате: \n " \
           "<начальная валюта> /" \
           "<валюта в которую вы хотите конвертировать>" \
           "<количество которое вы хотите конвертировать>"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values']) # Обработчик сообщений. Реагирует на команду 'values'.
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ]) # Обработчик сообщений. Реагирует на контент типа 'text'.
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        quote, base, amount = values
        new_price = Convertor.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message.chat.id, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} : {new_price}"
        bot.send_message(message.chat.id, text)


bot.polling() # Команда для постоянной работы скрипта.
