# Team 1-39, Microdonations and Microvolunteering #
# Split-Coin #
# Creators: Hisham Assana, Christopher Lee, Nikhil Mahajan, Nasrat Alam #

## Summary ##

https://split-coin.herokuapp.com/

Split Coin is a web app designed to allow volunters and event organizers to find each other in one, unified expererience. Volunteers and donators may seek out opportunities to work for or financially contribute to, and organizers are allowed to create and schedule events for users to find. Upon first entering the site, users are presented with a Google login page. After logging in and selecting their account preference (Volunteer or Submitter), they are free to browse the website. This includes browsing for events and donation opportunities, viewing and editing your profile, checking the schedule of events you've signed onto, and more.

On the home page, users are presented with a timeline populated by various events submitted by other users, sorted in chronological order from the earliest to the latest.

## Volunteer and Submitter ##
Volunteers and Submitters may choose their account usage preference upon logging in for the first time, and may change it at any other time in the future via navigating to the "Profile" tab of the home navigation bar, and clicking the "Edit Profile" option on the page. Each type of user will see slightly different versions of the site.

### Volunteer Experience ###
Volunteers on the site may donate to events requesting financial contribution, or agree to volunteer at an event. When Donating (events and denoted by ), users are presented with a slider to control how much money they donate, in increments of $.25 ranging from the $.50 to $100, as well an entry field to fill out the credit card information (further details can be found under "How to Navigate Credit Card API"). 

When selecting an event to Volunteer for, the user will be shown the relevant information regarding the event as well as have the option to "accept" the event, signing them up for it.

### Submitter Experience ###
Submitters on the site may generate events for users to contribute to. This can be either Volunteering events, where users pledge to attend events for a certain amount of time on a particular date, or donate money to a cause.
## How to Navigate Credit Card API ##
For the credit card number, you can input any valid VISA and MasterCard number (e.g 4242 4242 4242 4242 which is the test card we charge in the backend) with valid expiration dates and random Zip Code and CVV. The donation is charged to the card above and you will be awarded XP based of the amount charged.

## Gamified Interface (How XP works?) ##
You earn XP by donating money to the donation events and you also earn XP when you accept a volunteering event. XP scales with length of the event and the amount donated. You will gain a level every 1000 EXP and you can check your total EXP and rank on the leaderboard page of the site which will show the top 10 users with the highest EXP.

## How Submitted Event Tab works ##
Creators will have acces to a Submitted Events tab which will allow them to view their created events. For their volunteering events, clicking on an event will show them who has signed up for the event. For their donation events, the site will display the total amount of money donated to the cause.

## How Schedule Tab works ##
The schedule tab will show a user a list of the upcoming VOLUNTEER events that they have signed up for. Donation events will not be shown here.

## How Profile Tab works ##
This tab will show your current account information (email address and phone number) as well as a list of past opportunities that the user has signed up for. The user's EXP and level will also be viewable on this page as well as the option to edit their profile. 

On the Edit Profile page, a user can change from Volunteer to Submitter (or vice versa) as well as update their current account information.

### Licensing and Dependencies ###

Django is used under the BSD-3
https://github.com/django/django/blob/master/LICENSE

Stripe is used under the Stripe Service Agreement
https://stripe.com/ssa

SQLite is used under public domain
https://www.sqlite.org/copyright.html

Gunicorn is used under the MIT License
https://github.com/benoitc/gunicorn/blob/master/LICENSE

PostgreSQL is used under the PostgreSQL License
https://www.postgresql.org/about/licence/
