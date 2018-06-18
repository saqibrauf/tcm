from datetime import datetime
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Series, Match, Message

admin.site.register(Series)

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    ordering = ['-date']

class MessageAdmin(admin.ModelAdmin):
	list_display = ('date', 'match', 'message')
admin.site.register(Message, MessageAdmin)


class MatchListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Sort Matches')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'now'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Todays', _('Todays Matches')),
            ('Upcoming', _('Upcoming Matches')),
            ('Recent', _('Recent Matches')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        now = datetime.today()
        if self.value() == 'Todays':
            return queryset.filter(date__day=now.day, date__month=now.month, date__year=now.year)
        if self.value() == 'Upcoming':
            return queryset.filter(date__gt=now)
        if self.value() == 'Recent':
            return queryset.filter(date__lt=now)

class MatchAdmin(admin.ModelAdmin):

    list_display = ('date', 'time', 'opponents', 'series')
    list_filter = (MatchListFilter,)

    inlines = [
        MessageInline,
    ]

admin.site.register(Match,MatchAdmin)
