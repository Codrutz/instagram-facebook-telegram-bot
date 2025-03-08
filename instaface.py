import telebot
import yt_dlp
import os

# Токен вашего бота
bot = telebot.TeleBot('')

# Функция для скачивания видео
def download_video(url):
    ydl_opts = {
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # Скачиваем видео
            return ydl.prepare_filename(info)           # Возвращаем путь к файлу
    except Exception as e:
        print(f"Ошибка загрузки видео: {e}")
        return None

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Отправь мне ссылку на видео из Instagram или Facebook, и я его скачаю."
    )

# Обработка текстовых сообщений (ссылок)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()  # Получаем текст сообщения
    if any(domain in url for domain in ['facebook.com', 'instagram.com']):
        bot.send_message(message.chat.id, "Видео загружается, подождите немного...")

        # Скачиваем видео
        video_path = download_video(url)

        if video_path:
            with open(video_path, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)  # Отправляем видео пользователю
            os.remove(video_path)  # Удаляем файл после отправки
        else:
            bot.send_message(message.chat.id, "Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, отправьте ссылку на видео из Instagram или Facebook."
        )

# Создаем папку для скачивания, если она не существует
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Запускаем бота
bot.polling(non_stop=True)
