from django.contrib import admin

from parserexample.parser.models import TelegramChannel, ChannelStats


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id', 'username', 'title')

@admin.register(ChannelStats)
class ChannelStatsAdmin(admin.ModelAdmin):
    list_display = ('channel__username', 'channel__title')

# Register your models here.
