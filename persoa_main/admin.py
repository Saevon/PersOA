from django.contrib import admin

from persoa_main.models.choice import BasicChoice, LinearChoice
from persoa_main.models.trait import BasicTrait, LinearTrait

class BasicChoiceInline(admin.TabularInline):
    model = BasicChoice
    extra = 2
    fields = ['name', 'defn']
    ordering = ['name']

class LinearChoiceInline(admin.TabularInline):
    model = LinearChoice
    extra = 1
    max_num = 10
    fields = ['name', 'defn', 'side']
    ordering = ['side']

class LinearTraitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Description', {'fields': ['defn', 'desc']}),
        ('Side', {'fields': ['pos_name', 'neg_name']}),
    ]
    inlines = [LinearChoiceInline]

class BasicTraitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Description', {'fields': ['defn', 'desc']}),
        ('Default Number', {'fields': ['default_num']}),
    ]
    inlines = [BasicChoiceInline]

admin.site.register(LinearTrait, LinearTraitAdmin)
admin.site.register(LinearChoice)

admin.site.register(BasicChoice)
admin.site.register(BasicTrait, BasicTraitAdmin)

