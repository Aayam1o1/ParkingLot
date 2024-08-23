from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class RestApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rest_api"

    def ready(self):
        try:
            from modeltranslation.translator import translator
            from rest_api.models import Parking
            from rest_api.translation import ParkingTranslationOptions

            # Ensure the translation options are registered
            translator.get_options_for_model(Parking)
        except Exception as e:
            logger.error(f"Error during modeltranslation registration: {e}")
            raise
