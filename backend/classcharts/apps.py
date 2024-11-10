from django.apps import AppConfig
import threading

class ClasschartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classcharts'

    def ready(self):
        from .tasks import daily_task
        # Start the background thread
        threading.Thread(target=daily_task, daemon=True).start()
