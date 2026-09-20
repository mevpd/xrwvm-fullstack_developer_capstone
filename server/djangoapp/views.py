# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer, Review, CarModel, CarMake
from .restapis import analyze_review_sentiments, get_request


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    if request.method == "GET":
        return redirect("/login/")

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
@csrf_exempt
def registration(request):
    if request.method == "GET":
        return redirect("/register/")
    context = {}

    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    data = {"userName": ""}
    return JsonResponse(data)
    

def fetch_all_dealers():
    data = get_request('/fetchDealers')
    if data is None:
        return []
    return [{
        'id': d['id'],
        'full_name': d['full_name'],
        'city': d['city'],
        'address': d['address'],
        'zip': d['zip'],
        'state': d['state'],
    } for d in data]


def get_dealerships(request):
    return JsonResponse({"dealers": fetch_all_dealers(), "status": 200})


def get_dealer_details(request, dealer_id):
    all_dealers = fetch_all_dealers()
    dealers = [d for d in all_dealers if d['id'] == int(dealer_id)]
    return JsonResponse({"dealer": dealers, "status": 200})


def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related('user_profile')
    out = [{
        'review': r.review,
        'sentiment': r.sentiment,
        'car_make': r.car_make,
        'car_model': r.car_model,
        'car_year': r.car_year,
        'name': r.user_profile.get_full_name() or r.user_profile.username,
    } for r in reviews]
    return JsonResponse({"reviews": out, "status": 200})


def get_cars(request):
    cars = CarModel.objects.select_related('car_make').values('car_make__name', 'name')
    out = [{"CarMake": c['car_make__name'], "CarModel": c['name']} for c in cars]
    return JsonResponse({"CarModels": out, "status": 200})


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    dealer_id = data['dealership']
    username = request.session.get('username') or data.get('name')

    user = User.objects.filter(username=username).first()
    if user is None:
        return JsonResponse({"status": 401, "error": "Not authenticated"}, status=401)

    sentiment = analyze_review_sentiments(data['review'])

    Review.objects.create(
        user_profile=user,
        dealer_id=dealer_id,
        review=data['review'],
        purchase=data.get('purchase', False),
        purchase_date=data.get('purchase_date'),
        car_make=data.get('car_make'),
        car_model=data.get('car_model'),
        car_year=data.get('car_year'),
        sentiment=sentiment,
    )
    return JsonResponse({"status": 200})
