from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator
import urllib2
from bs4 import BeautifulSoup
import sunburnt


def index(request):
	links = []
	si = sunburnt.SolrInterface("http://localhost:8080/solr/linkPad/")	

	# hand paginated
	##################################
	# response = si.query(id="*").paginate(start=0,rows=20).sort_by("-last_modified").execute()		
	# print "Num Results:",response.result.numFound	
	# for each in response:
	# 	links.append(each)
	
	# template = loader.get_template('index.html')	
	# context = RequestContext(request, {
	# 	'links': links,
	# })	
	# print context
	# return HttpResponse(template.render(context))


	# Sunburnt / Django paginated
	##################################
	paginator = Paginator(si.query(id="*").sort_by("-last_modified"), 5) 
	
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

	template = loader.get_template('index.html')	
	context = RequestContext(request, {
		'links': links,
	})	
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
	
	# index in Solr
	document = {
		"id":"horsegoober",
		"linkTitle":page_title,
		"linkURL":add_url,
		"last_modified":"NOW"
	}
	si.add(document)
	si.commit()

	return HttpResponse("Added!")

	
	

