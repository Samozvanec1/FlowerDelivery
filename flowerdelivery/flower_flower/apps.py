from django.apps import AppConfig
import threading

class FlowerFlowerConfig(AppConfig):
   default_auto_field = 'django.db.models.BigAutoField'
   name = 'flower_flower'

 # Переменная класса для отслеживания запуска бота
   _bot_started = False
   _lock = threading.Lock()

   def ready(self):
    # Используем блокировку, чтобы избежать гонки за ресурс
    with FlowerFlowerConfig._lock:
       if not FlowerFlowerConfig._bot_started:
            FlowerFlowerConfig._bot_started = True # Устанавливаем флаг в True
            thread = threading.Thread(target=self.start_bot_in_thread)
            thread.daemon = True # Обеспечиваем завершение потока при выходе из основного процесса
            thread.start()

    def start_bot_in_thread(self):
        import asyncio
        from bot import start_bot

 # Создаём новый событийный цикл и запускаем бота
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(start_bot())

 # Добавляем проверку перед запуском бота
        if not FlowerFlowerConfig._bot_started:
            FlowerFlowerConfig._bot_started = True
        else:
            print("Бот уже запущен")