from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bs4 import BeautifulSoup
import datetime
import json
import sunburnt

def searchDB(request,constructed_query):
	links = []
	
	# si = sunburnt.SolrInterface("http://localhost:8080/solr/linkPad/")
	# Sunburnt / Django paginated
	##################################
	# paginator = Paginator(si.query(id="*").sort_by("-last_modified"), 10) 
	paginator = Paginator(constructed_query, 10) 
	
	 # Make sure page request is an int. If not, deliver first page.
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	# If page request (9999) is out of range, deliver last page of results.
	try:
		links = paginator.page(page)
	except (EmptyPage, InvalidPage):
		links = paginator.page(paginator.num_pages)
	
	context = RequestContext(request, {
		'links': links,
		'params':request.GET,
	})	

	return context


def index(request):

	si = sunburnt.SolrInterface("http://localhost:8080/solr/linkPad/")
	constructed_query = si.query(id="*").sort_by("-last_modified")

	context = searchDB(request,constructed_query)
	template = loader.get_template('index.html')	
	
	# print context
	return HttpResponse(template.render(context))



# add link to solr
def addLink(request):
	try:
		add_url = request.GET['url']
	except:
		print "Uh-oh."
		return HttpResponse("No url bonehead.")

	si = sunburnt.SolrInterface("http://localhost:8080/solr/linkPad/")

	# get page title
	soup = BeautifulSoup(urllib2.urlopen(add_url))
	page_title = soup.title.string

	# set date
	current_date = datetime.datetime.now().isoformat()
	
	# index in Solr
	document = {		
		"linkTitle":page_title,
		"linkURL":add_url,
		"last_modified":current_date
	}
	si.add(document)
	si.commit()

	return HttpResponse("Added!")

	

def search(request):
	# search string
	search_string = request.GET['q']

	si = sunburnt.SolrInterface("http://localhost:8080/solr/linkPad/")
	constructed_query = si.query(search_string).sort_by("-last_modified")

	context = searchDB(request,constructed_query)
	template = loader.get_template('index.html')	
	
	# print context
	return HttpResponse(template.render(context))
