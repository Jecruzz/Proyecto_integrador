from django.contrib import admin
from .models import Profile, Event, Participation, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'fecha_ingreso']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'hora', 'ubicacion', 'creador')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'ubicacion', 'creador__username')

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'confirmado')
    list_filter = ('confirmado',)
    search_fields = ('usuario__username', 'evento__titulo')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('autor', 'evento', 'fecha')
    search_fields = ('autor__username', 'evento__titulo', 'contenido')
    list_filter = ('fecha',)
