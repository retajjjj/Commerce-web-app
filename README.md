# Commerce - Online Auction Platform

## Overview
Commerce is an online auction site built using Django, allowing users to create listings, place bids, and leave comments. Users can also maintain a watchlist and browse listings by categories.

## Features
- **User Authentication:** Register, login, and logout functionality.
- **Create Listings:** Users can create new auction listings with a title, description, starting bid, optional image URL, and category.
- **Active Listings Page:** Displays all currently active auction listings.
- **Listing Page:** Shows details of a specific auction listing, including:
  - Bidding functionality.
  - Ability to add/remove items from the watchlist.
  - Option to close the auction for the listing creator.
  - Comments section where users can leave and view comments.
- **Watchlist:** Users can maintain a watchlist of listings they are interested in.
- **Categories:** View listings categorized into different sections (e.g., Fashion, Electronics, Home, etc.).
  

## Installation

### Steps
1. Apply database migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Run the server:
   ```sh
   python manage.py runserver
   ```
3. Open a web browser and visit `http://127.0.0.1:8000/`
   
## Demo
https://youtu.be/-E_IGE_rk_0

## Project Structure
```
commerce/
│── auctions/          # Main Django app
│   ├── migrations/    # Database migrations
│   ├── static/        # Static files (CSS, JS, images)
│   ├── templates/     # HTML templates
│   ├── urls.py        # URL routing
│   ├── views.py       # Application logic
│   ├── models.py      # Database models
│── commerce/          # Project configuration
│── manage.py          # Django management script
```

## Usage
1. Register an account via `/register`.
2. Create a new auction listing via `/create`.
3. Browse and bid on active listings.
4. Add items to the watchlist for future reference.
5. Close auctions to declare a winner.
6. Leave comments on listings.


