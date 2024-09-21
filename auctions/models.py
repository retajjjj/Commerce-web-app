from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.id}"



class Auctions(models.Model):
    user_id=models.ForeignKey(User , on_delete=models.CASCADE, related_name= "selling")
    #watchlist=models.ForeignKey(Watchlist , on_delete=models.CASCADE , related_name="watchlist" )
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=1024)
    starting_bid=models.FloatField()
    image=models.URLField(blank=True)
    category=models.CharField(max_length=64, blank=True)
    date=models.DateTimeField()
    closed = models.BooleanField(default=False)
    def __str__(self):
        return  f"{self.id}"


class Bids(models.Model):
    auction_id=models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="prices")
    user_id=models.ForeignKey(User, on_delete=models.CASCADE , related_name="bidder")
    price=models.FloatField(default=0)
    def __str__(self):
        #return f"{self.price}"
        return f" auction_id: {self.auction_id}   user_id: {self.user_id}   price:{self.price}"

class Comments(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE , related_name="commenters")
    auction_id=models.ForeignKey(Auctions , on_delete=models.CASCADE , related_name="auctions")
    comment=models.CharField(max_length=100 , default=None)
    def __str__(self):
        return f"{self.id}"
    #auction_id}: {self.comment} by {self.user_id}
    def __int__(self):
        return self.user_id

class Watchlist(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE , related_name="watchers" , default=None )
    auction_id=models.ForeignKey(Auctions , on_delete=models.CASCADE , related_name="watchlist") 
    def __str__(self):
        return f"{self.id} : {self.auction_id} "

class Categories(models.Model):
    a_id=models.ForeignKey(Auctions , on_delete=models.CASCADE , related_name="categories")
    category_name=models.CharField(max_length=100 , default=None)
    def __str__(self):
        return f"{self.category_name} : {self.a_id}"