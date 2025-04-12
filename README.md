# 🛒 Commerce - Online Auction Platform

This project is an online auction site similar to eBay, built with Django. Users can create auction listings, place bids, leave comments, and manage a personal watchlist.

---

## ⚙️ Features

- User authentication (register, login, logout)
- Create auction listings with:
  - Title, description, starting bid
  - Optional image and category
- View active listings
- View details of a specific listing
- Place bids (only if higher than current)
- Add or remove items from personal watchlist
- Comment on listings
- Auction creators can close auctions and declare a winner

---

## 🚀 How to Run

Make sure you have Python and Django installed.

```bash
# Step 1: Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Step 2: Run the development server
python manage.py runserver
