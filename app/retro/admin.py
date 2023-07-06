from django.contrib import admin
from retro.models import RetroSession, RetroCard, CardGroup, RetroReaction

class RetroSessionAdmin(admin.ModelAdmin):
    model = RetroSession
    fields = ['id', 'board', 'attendees', 'admin', 'vote_limitation', 'retro_step']
    readonly_fields = ['id']


class RetroCardAdmin(admin.ModelAdmin):
    model = RetroCard
    fields = ['id', 'card_group', 'text', 'is_positive']
    readonly_fields = ['id']


class CardGroupAdmin(admin.ModelAdmin):
    model = CardGroup
    fields = ['id', 'name', 'retro_session', 'is_discussed']
    readonly_fields = ['id']


class RetroReactionAdmin(admin.ModelAdmin):
    model = RetroReaction
    fields = ['id', 'card_group', 'reactor', 'count']
    readonly_fields = ['id']


admin.site.register(RetroSession, RetroSessionAdmin)
admin.site.register(RetroCard, RetroCardAdmin)
admin.site.register(CardGroup, CardGroupAdmin)
admin.site.register(RetroReaction, RetroReactionAdmin)
