from modeltranslation.translator import TranslationOptions, register
from rest_api.models import Parking

@register(Parking)
class ParkingTranslationOptions(TranslationOptions):
    fields = ('wing_name',)