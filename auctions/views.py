from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm, TextInput, NumberInput, URLInput, Textarea
from .models import User,Auctions,Bids,Watchlist,Comments,Categories
import datetime


class NewForm(ModelForm):
    class Meta:
        model = Auctions
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'title': TextInput(attrs={
                'class': "form-new",
                'placeholder': 'Title',
                'style': 'max-width: 300px;'
                }),
            'description': Textarea(attrs={
                'class': "form-control-big",
                'placeholder': 'Description',
                'style': 'max-width: 300px;'
                }),
            'starting_bid': NumberInput(attrs={
                'class': "form-new", 
                'style': 'max-width: 300px;',
                'placeholder': 'price'
                }),
            'image': URLInput(attrs={
                'class': "form-new", 
                'style': 'max-width: 300px;',
                'placeholder': 'Image URL (optional)'
                }), 
            'category': TextInput(attrs={
                'class': "form-new", 
                'style': 'max-width: 300px;',
                'placeholder': 'Category (Optional)'
                }), 
             
        }

class BidForm(forms.Form):
    bid=forms.FloatField( min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'BID', 
        'style': 'width: 300px;', 
        'class': 'form-bid'
        }))

class CommentForm(forms.Form):
    comment=forms.CharField( widget=forms.Textarea(attrs={
        'placeholder': 'Comment', 
        'style':  'TextMode=MultiLine;', 
        'class': 'form-comment',
        }))

    
def index(request):
    
    return render(request, "auctions/index.html" , {
        "auctions": Auctions.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new(request):
    
    if(request.method== "POST"):
        form=NewForm(request.POST)
        if form.is_valid():
            user_id=User.objects.get(pk=request.user.id)
            title=form.cleaned_data["title"]
            description=form.cleaned_data["description"]
            bid= form.cleaned_data["starting_bid"]
            image=form.cleaned_data["image"]
            category=form.cleaned_data["category"]
        
            created_auction=Auctions.objects.create(user_id=user_id ,title=title , description=description , starting_bid=bid , image=image 
                                , category=category, date=datetime.datetime.now())

            #Categories.objects.create(a_id=created_auction.id , category_name=category )
            return redirect("index")
        return render(request ," auctions/new.html" , {"new_from":form})
    return render(request , "auctions/new.html" , {
        "new_form": NewForm() 
    })

@login_required(login_url='login')
def view_listing(request,auction_id):
    
    user_id=User.objects.get(pk=request.user.id)  
    #get all prices of the old bids on that auction
    auction=Auctions.objects.get(id=auction_id)
    prices=Bids.objects.filter(auction_id=auction.id).values_list("price", flat=True)
    original_price=auction.starting_bid
    auction_id=Auctions.objects.get(pk=auction_id)


    #user can close the bid or not
    if auction.user_id==request.user:
        can_close=True
    else:
        can_close=False
    
    # winner of the bid
    if Bids.objects.filter(auction_id=auction.id).count()>0:
        win_bids=Bids.objects.filter(auction_id=auction.id).order_by("-price")[0]
        winner=win_bids.user_id
    else:
        winner=user_id
    
    # closing the bid
    closed=False
    if(request.method== "POST") and "close" in request.POST:
        closed=True
        auction.closed=True
        auction.save()
        return redirect(request.META['HTTP_REFERER'])

    #watchlsit add or remove
    watchlist=Watchlist.objects.filter(user_id=user_id).values_list("auction_id", flat=True)
    if auction.id in watchlist:
        can_remove_from_watchlist= True
    else:
        can_remove_from_watchlist=False
    
    #Adding to watch list
    if( request.method== "POST" and "add_watchlist" in request.POST and closed==False):
        Watchlist.objects.create(auction_id=auction_id , user_id=user_id )
        return redirect(request.META['HTTP_REFERER'])

    #removing from watchlist
    if( request.method== "POST" and "remove_watchlist" in request.POST and closed==False):
        Watchlist.objects.filter(auction_id=auction_id).delete()
        return redirect(request.META['HTTP_REFERER'])

    
    """if auction_id in request.session["watchlist"]:
        can_remove_from_watchlist=True
    else:
        can_remove_from_watchlist=False"""
    
    

    """if "watchlist" not in request.session:
        print("yess")
        request.session["watchlist"] = []

    if request.method == "POST" and "add_watchlist" in request.POST and closed==False:
        request.session["watchlist"]+=[auction.id]
        request.session.modified = True
        return redirect(request.META['HTTP_REFERER'])
    
    if request.method == "POST" and "remove_watchlist" in request.POST and closed==False:
        request.session["watchlist"]-=[auction.id]
        request.session.modified = True
        return redirect(request.META['HTTP_REFERER'])"""
    

    
    #adding comment to the auction
    if(request.method== "POST") and "comment_form" in request.POST:
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment=comment_form.cleaned_data["comment"]
            Comments.objects.create(user_id=user_id, auction_id=auction_id , comment= user_comment)
            return redirect(request.META['HTTP_REFERER'])

    #display all comments
    comments_ids=Comments.objects.filter(auction_id=auction_id).values_list("id", flat=True)
    
    comment_list=[]
    username_list=[]
    for id in comments_ids:
        comment=Comments.objects.get(pk=id)
        comment_list.append(comment.comment)
        
    commenters=Comments.objects.filter(auction_id=auction_id).values_list("user_id", flat=True)
    for commenter in commenters:
       user= User.objects.get(id=commenter)
       username_list.append(user.username)

    comments = list(zip(username_list, comment_list))
    

    # form for bidding
    if(request.method== "POST") and "form" in request.POST:
        bid_form=BidForm(request.POST)
        if bid_form.is_valid():
            user_bid=bid_form.cleaned_data["bid"]
            if user_bid>=original_price:
                if len(prices)>0:
                    if(user_bid<max(prices)):
                        #cant bid with this price
                        return render(request ,"auctions/listing.html" , {
                            "comment_form":CommentForm(),
                            "bid_form":BidForm() ,
                            "auction":auction ,
                            "error":True ,
                            "watchlist_addremove": can_remove_from_watchlist,
                            "winner": winner,
                            "closed":closed ,
                            "user_id":user_id ,
                            "comments":comments 
                           
                          
                            
                            })
                Bids.objects.create(user_id=user_id , auction_id=auction_id , price=user_bid)
                auction.starting_bid=user_bid
                auction.save()
                # can bid with this price
                return render(request ,"auctions/listing.html" , {
                    "comment_form":CommentForm(),
                    "bid_form":BidForm() , 
                    "auction":auction  ,
                    "recorded":True , 
                    "can_close":can_close ,
                    "watchlist_addremove": can_remove_from_watchlist,
                    "winner": winner,
                    "closed":closed ,
                    "user_id":user_id ,
                    "comments":comments 
                    
                   
                    
                    })
            # if invalid form
            return render(request ,"auctions/listing.html" , {
                "comment_form":CommentForm(),
                "bid_form":bid_form , 
                "auction":auction ,
                "error":True ,
                "watchlist_addremove": can_remove_from_watchlist,
                "winner": winner , 
                "closed":closed ,
                "user_id":user_id ,
                "comments":comments 
                
                
                })
        
    # if it is not post
    return render(request , "auctions/listing.html", {
        "comment_form":CommentForm(),
        "bid_form":BidForm() , 
        "auction":auction , 
        "can_close":can_close,
        "watchlist_addremove": can_remove_from_watchlist,
        "winner": winner , 
        "closed":closed ,
        "user_id":user_id , 
        "comments":comments 
    })



def watchlist(request):
    user_id=User.objects.get(pk=request.user.id)
    watchlist_ids = Watchlist.objects.filter(user_id=user_id).values_list("auction_id" , flat=True)
    auction_list=[]
    for watchlist_id in watchlist_ids:
        auction=Auctions.objects.get(id=watchlist_id)
        auction_list.append(auction)
    return render(request , "auctions/watchlist.html" , {
        "auction_list":auction_list
        })
    

def category(request):
    categories=Auctions.objects.filter().values_list("category" , flat=True)
    category_set=set()
    for category in categories:
        if category!="":
            category_set.add(category)

    if request.method=="GET" and "q" in request.GET:
        q=request.GET.get("q", "")
        
        listings_ids=Auctions.objects.filter(category=q).values_list("id" , flat=True)
        auction_list=[]
        for id in listings_ids:
            auction=Auctions.objects.get(pk=id)
            auction_list.append(auction)
        
        return render(request, 'auctions/category.html', {
            "listings_ids": listings_ids ,
            "auction_list": auction_list
        })
    return render(request , "auctions/category.html" , {
        "category_set":category_set
    })
    
