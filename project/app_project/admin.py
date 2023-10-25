from django.contrib import admin
from .models import Advertisement
from django.utils.html import format_html


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id','smallimg','title','description','price','created_date','update_date','auction']
    list_filter = ['auction','created_at','price']
    actions = ['make_auction_false','make_auction_true']
    fieldsets = (
        ('Общее', {
            'fields':('title', 'description','image')
        }),
        ('Финансы', {
            'fields': ('price','auction'),
            'classes' : ['collapse']
        })
    )

    @admin.action(description = "Убрать торг")
    def make_auction_false(self, request, queryset):
        queryset.update(auction=False)

    @admin.action(description="Добавить торг")
    def make_auction_true(self, request, queryset):
        queryset.update(auction=True)

    @admin.display(description='Картинка')
    def smallimg(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="35" height="30" />', obj.image.url)
        else:
            return format_html('<img src="static/img/adv.png" width="35" height="30" />')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Advertisement, AdvertisementAdmin)
