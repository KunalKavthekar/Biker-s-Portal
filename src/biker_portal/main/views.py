from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Item, Search
from .forms import CreateNewList
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
import json
import time
import urllib.request
# Create your views here.

@login_required
def index(response, id):
	ls = ToDoList.objects.get(id=id)

	if ls in response.user.todolist.all():

		if response.method == "POST":
			print(response.POST)
			if response.POST.get("save"):
				for item in ls.item_set.all():
					if response.POST.get("c" + str(item.id)) == "clicked":
						item.complete = True
					else:
						item.complete = False

					item.save()

			elif response.POST.get("newItem"):
				txt = response.POST.get("new")

				if len(txt) > 2:
					ls.item_set.create(text=txt, complete=False)
				else:
					print("invalid")

		return render(response, "main/list.html", {"ls":ls})
	return render(response, "main/view.html", {})

@login_required
def home(response):
	return render(response, "main/home.html", {})

@login_required
def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST)

		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()
			response.user.todolist.add(t)

		return HttpResponseRedirect("/%i" %t.id)

	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form":form})

@login_required
def view(response):
	return render(response, "main/view.html", {})

@login_required
def about(response):
	return render(response, "main/about.html", {})

@login_required
def getLocation(response):
	if response.method == "POST":
		if response.POST["btn"] == "location":
			source = response.POST['source']
			destination = response.POST['destination']
			t = ToDoList(src=source)
			print("CHECKING! {}".format(t))
			# t1 = ToDoList(dest=destination)
			t.save()
			# t1.save()

			response.user.todolist.add(t)
			# response.user.todolist.add(t1)

		loc = {
				"source":source,
				"destination":destination
			}
		return render(response, "main/getData.html", loc)

	context = {
		"form": ""
	}

	return render(response, "main/getData.html", context)



# def login(response):
# 	return render(response, "main/login.html")

# BASE_AMAZON_URL = 'https://www.amazon.in/s?k={}}&ref=nb_sb_noss_2'
# BASE_EBAY_URL_TRY = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={}'
BASE_SNAP_URL = 'https://www.snapdeal.com/search?keyword={}&sort=rlvncy'
BASE_FLIP_YRL = 'https://www.flipkart.com/search?q={}'


@login_required
def new_search(request):
	search = request.POST.get('search')
	search = " "
	Search.objects.create(search=search)

	if request.method == "POST":
		sname = request.POST["search"]
	
		final_url = BASE_FLIP_YRL.format(quote_plus(sname))
		response = requests.get(final_url)
		data = response.text
		soup = BeautifulSoup(data, features='html.parser')
		post_titles = soup.find_all('a',{'class': '_2cLu-l'})
		post_prices = soup.find_all('div',{'class': '_1vC4OE'})
		post_images = soup.find_all('div',{'class': '_3BTv9X'})


		final_postings = []

		for i in range(0,len(post_titles)):
			pTitle = post_titles[i].text
			pLink = 'https://www.flipkart.com' + str(post_titles[i].get('href'))
			pImage = str(post_images[i].get('src'))
			
			if post_prices[i]:
				pPrice = post_prices[i].text
			else:
				pPrice = 'N/A'
	
			final_postings.append((pTitle, pLink, pPrice, pImage))

	

		stuff_for_frontend = {
			'search': search,
			'final_postings': final_postings,
		}

		return render(request, "main/new_search.html", stuff_for_frontend)
	return render(request, "main/new_search.html", {})


@login_required
def getWeather(request):
	place = ""
	if request.method == "POST":
		place = request.POST["place"]
		print("Place is {}".format(place))
		# Search.objects.create(search=search)

		address = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=hSC1IXjw3yXMcgALMjOS44tYbjEQkGbv&q={}&language=en-us&details=true".format(place)
		search_address = address
		print(search_address)

		with urllib.request.urlopen(search_address) as search_address:
			data=json.loads(search_address.read().decode())

		location_key = data[0]['Key']
		forecastUrl = "http://dataservice.accuweather.com/currentconditions/v1/{}?apikey=hSC1IXjw3yXMcgALMjOS44tYbjEQkGbv"
		daily_forecastUrl = forecastUrl.format(quote_plus(location_key))

		with urllib.request.urlopen(daily_forecastUrl) as daily_forecastUrl:
			data=json.loads(daily_forecastUrl.read().decode())

		weather = []
		temp = str(data[0]['Temperature']['Metric']['Value'])
		icontext = str(data[0]['WeatherText'])
		weather.append(( temp, icontext ))

		variables = {
			'place': place,
			'weather': weather,
		}

		return render(request, "main/getWeather.html", variables)
	return render(request, "main/getWeather.html", {})