from django.contrib import admin
from .models import Series, Match, Message

admin.site.register(Series)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'opponents', 'series')
admin.site.register(Match,MatchAdmin)

class MessageAdmin(admin.ModelAdmin):
	list_display = ('date', 'match', 'message')
admin.site.register(Message, MessageAdmin)
