from django.http import HttpResponse
from django.utils.html import escape

from .models import Movies


def _movie_payloads():
	return [
		{
			"title": "The Phantom Menace",
			"episode_nb": 1,
			"opening_crawl": None,
			"director": "George Lucas",
			"producer": "Rick McCallum",
			"release_date": "1999-05-19",
		},
		{
			"title": "Attack of the Clones",
			"episode_nb": 2,
			"opening_crawl": None,
			"director": "George Lucas",
			"producer": "Rick McCallum",
			"release_date": "2002-05-16",
		},
		{
			"title": "Revenge of the Sith",
			"episode_nb": 3,
			"opening_crawl": None,
			"director": "George Lucas",
			"producer": "Rick McCallum",
			"release_date": "2005-05-19",
		},
		{
			"title": "A New Hope",
			"episode_nb": 4,
			"opening_crawl": None,
			"director": "George Lucas",
			"producer": "Gary Kurtz, Rick McCallum",
			"release_date": "1977-05-25",
		},
		{
			"title": "The Empire Strikes Back",
			"episode_nb": 5,
			"opening_crawl": None,
			"director": "Irvin Kershner",
			"producer": "Gary Kurtz, Rick McCallum",
			"release_date": "1980-05-17",
		},
		{
			"title": "Return of the Jedi",
			"episode_nb": 6,
			"opening_crawl": None,
			"director": "Richard Marquand",
			"producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
			"release_date": "1983-05-25",
		},
		{
			"title": "The Force Awakens",
			"episode_nb": 7,
			"opening_crawl": None,
			"director": "J. J. Abrams",
			"producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
			"release_date": "2015-12-11",
		},
	]


def populate(request):
	results = []
	for payload in _movie_payloads():
		try:
			Movies.objects.create(**payload)
			results.append("OK")
		except Exception as error:
			results.append(str(error))
	return HttpResponse("<br>".join(results))


def display(request):
	try:
		movies = Movies.objects.all().order_by("episode_nb")
		if not movies.exists():
			return HttpResponse("No data available")

		rows = []
		for movie in movies:
			rows.append(
				"<tr>"
				f"<td>{escape(str(movie.title))}</td>"
				f"<td>{escape(str(movie.episode_nb))}</td>"
				f"<td>{escape('' if movie.opening_crawl is None else str(movie.opening_crawl))}</td>"
				f"<td>{escape(str(movie.director))}</td>"
				f"<td>{escape(str(movie.producer))}</td>"
				f"<td>{escape(str(movie.release_date))}</td>"
				"</tr>"
			)

		html = (
			"<table border='1'>"
			"<thead><tr>"
			"<th>title</th><th>episode_nb</th><th>opening_crawl</th>"
			"<th>director</th><th>producer</th><th>release_date</th>"
			"</tr></thead>"
			"<tbody>"
			+ "".join(rows)
			+ "</tbody></table>"
		)
		return HttpResponse(html)
	except Exception:
		return HttpResponse("No data available")
