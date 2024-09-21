from django.contrib import admin
from .models import User,Auctions,Bids,Comments, Watchlist,Categories

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "email")
class BidsAdmin(admin.ModelAdmin):
    list_display=("id" , "auction_id" , "user_id", "price")
    list_editable=("auction_id" , "user_id", "price")
class AuctionsAdmin(admin.ModelAdmin):
    list_display=("id" , "user_id" , "title" , "description" , "starting_bid" , "image" , "category" , "date", "closed") 
    list_editable = ("title" ,'description',"starting_bid" , "image" , "category" , "date", "closed",)
class WatchlistAdmin(admin.ModelAdmin):
    list_display=("id" , "auction_id" ,"user_id")
class CommentsAdmin(admin.ModelAdmin):
    list_display=("id" ,"user_id" , "auction_id" , "comment")
    list_editable=("user_id" , "auction_id" , "comment")
class CategoriesAdmin(admin.ModelAdmin):
    list_display=("id" , "a_id" , "category_name")
admin.site.register(User, UserAdmin)
admin.site.register(Auctions, AuctionsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments , CommentsAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Categories, CategoriesAdmin)