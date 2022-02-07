from django.contrib import admin

from .models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    search_fields = ('user')
    readonly_fields = ('user')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    class Meta:
        model = FriendList


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver')
    search_fields = ('sender__username','sender__email','receiver__username','receiver__email')

    filter_horizontal = ()
    list_filter = ('sender','receiver')
    fieldsets = ()

    class Meta:
        model = FriendRequest


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)