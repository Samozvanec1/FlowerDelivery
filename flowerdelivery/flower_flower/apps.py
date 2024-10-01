from django.apps import AppConfig
import threading

class FlowerFlowerConfig(AppConfig):
   default_auto_field = 'django.db.models.BigAutoField'
   name = 'flower_flower'

 # Переменная класса для отслеживания запуска бота
