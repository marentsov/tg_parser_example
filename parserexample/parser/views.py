from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView
from django.conf import settings
from asgiref.sync import async_to_sync
from telethon import TelegramClient
from telethon.sessions import StringSession

from parserexample.parser.forms import ChannelParseForm
from parserexample.parser.parser import tg_parser
from parserexample.parser.models import TelegramChannel, ChannelStats



class ParserView(FormView):
    form_class = ChannelParseForm
    template_name = 'parse_channel.html'
    success_url = reverse_lazy('parser/channels_list.hrml')

    def get_telegram_client(self):
        """ Получаем клиент телеграма для работы парсера """
        return TelegramClient(
            StringSession(settings.TELEGRAM_SESSION_STRING),
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )

    async def async_tg_parser(self, url, limit=10):
        """ Обертка для парсера """
        client = self.get_telegram_client()
        try:
            return await tg_parser(url, client, limit)
        finally:
            await client.disconnect()

    def save_channel(self, data):
        """Создаем или обновляем канал"""
        return TelegramChannel.objects.update_or_create(
            channel_id=data['channel_id'],
            title=data['title'],
            username=data['username'],
            description=data['description'],
            participants_count=data['participants_count'],
            last_messages=data['last_messages'],
        )

    def save_stats(self, channel, stats):
        """Создаем запись статистики с расчетом прироста"""
        last_stats = ChannelStats.objects.filter(channel=channel).order_by('-parsed_at').first()
        daily_growth = stats['participants_count'] - last_stats.participants_count if last_stats else 0

        ChannelStats.objects.create(
            channel=channel,
            participants_count=stats['participants_count'],
            daily_growth=daily_growth
        )


    def form_valid(self, form):
        """ Обработка формы """
        identifier = form.cleaned_data['channel_identifier']
        limit = form.cleaned_data['limit']

        try:
            # Запуск асинхронной функции парсинга
            async_parser = async_to_sync(self.async_tg_parser)
            parsed_data = async_parser(identifier, limit)

            # Сохранение полученных данных
            channel, created = self.save_channel(parsed_data)
            self.save_stats(channel, parsed_data['stats'])

            # Составление сообщения для пользователя
            message = f'Новый канал добавлен: {channel.title}' \
                if created \
                else f'Канал обновлен: {channel.title}'
            messages.success(self.request, message)

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)













class ParserListView(ListView):
    pass
# Create your views here.
