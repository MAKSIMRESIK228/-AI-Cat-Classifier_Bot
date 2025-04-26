import telebot
from logic import detect_cat
import os

# Токен вашего бота
bot = telebot.TeleBot("....")

# Папка для сохранения изображений
if not os.path.exists('images'):
    os.makedirs('images')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(func=lambda message: True)
def cat_info(message):
    cat = message.text.strip()
    if cat == "Сфинкс":
        bot.reply_to(message, "Сфинкс: лысая кошка с дружелюбным и игривым характером. Любит есть тёплую и питательную пищу — индейку, курицу и специальные корма с повышенным содержанием энергии.")
    elif cat == "Мейн-кун":
        bot.reply_to(message, "Мейн-кун: крупная и пушистая кошка, известная своей ласковостью. Предпочитает мясо, влажные корма и куриные шейки.")
    elif cat == "Персидская кошка":
        bot.reply_to(message, "Персидская кошка: спокойная и аристократичная. Любит мягкие влажные корма, иногда балуется паштетом из рыбы или курицы.")
    elif cat == "Сиамская кошка":
        bot.reply_to(message, "Сиамская кошка: умная, разговорчивая и очень преданная. Обожает свежую рыбу, индейку и корм с высоким содержанием белка.")
    elif cat == "Шотландская вислоухая":
        bot.reply_to(message, "Шотландская вислоухая: милая и уравновешенная. Предпочитает разнообразные корма с рыбой, а также вкусняшки с говядиной.")
    elif cat == "Рэгдолл":
        bot.reply_to(message, "Рэгдолл: нежная, спокойная кошка. Любит влажные корма с кроликом, курицей и часто ест с удовольствием сухой премиум-корм.")
    else:
        bot.reply_to(message, "❓ Не удалось распознать породу кошки. Попробуй написать точное название.")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    # Проверяем, есть ли фотографии
    if not message.photo:
        return bot.send_message(message.chat.id, "Вы забыли загрузить картинку :(")

    # Получаем файл и сохраняем его
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split("/")[-1]

    # Загружаем файл и сохраняем
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f'images/{file_name}'
    with open(file_path, "wb") as new_file:
        new_file.write(downloaded_file)
    
    # Определяем породу кошки с помощью функции detect_cat
    breed = detect_cat(file_path)

    # Отправляем пользователю результат
    bot.reply_to(message, f"Порода кошки: {breed}")

# Запускаем бота
bot.polling()
