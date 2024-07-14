from django.apps import AppConfig
import joblib
import os

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'myown.pkl')
        self.model = joblib.load(model_path)
        




   