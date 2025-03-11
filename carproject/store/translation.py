from modeltranslation.translator import TranslationOptions,register
from .models import (Category, Car)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Car)
class CarTranslationOptions(TranslationOptions):
    fields = ('description',)