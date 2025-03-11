from django.contrib import admin
from .models import (
    UserProfile, Client, Owner, CarMake, CarModel, Category, Car,
    CarImage, Cart, CartItem, Favorite, FavoriteItem, History
)
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

class ImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class GeneralMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Car)
class CategoryAdmin(TranslationAdmin, GeneralMedia):
    inlines = [ImageInline]

@admin.register(Category)
class CategoryAdmin(TranslationAdmin, GeneralMedia):
    pass





admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Owner)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(History)