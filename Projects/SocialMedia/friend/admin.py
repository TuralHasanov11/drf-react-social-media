from django.contrib import admin

from .models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    list_display = ('id','user',)
    search_fields = ('user',)
    readonly_fields = ('user',)
    list_filter = ('user',)

    class Meta:
        model = FriendList


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver',)
    search_fields = ('sender__username','sender__email','receiver__username','receiver__email',)
    list_filter = ('sender','receiver',)

    class Meta:
        model = FriendRequest


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)