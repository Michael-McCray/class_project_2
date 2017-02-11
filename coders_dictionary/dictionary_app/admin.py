from django.contrib import admin

# Register your models here.
from models import Definition, Word, UserProfile, Language

# class LanguageAdmin(admin.ModelAdmin):
# 	prepopulate

# class WordAdmin(admin.ModelAdmin):
# 	prepopulate

admin.site.register(Definition)
admin.site.register(Word)
admin.site.register(UserProfile)
admin.site.register(Language)
