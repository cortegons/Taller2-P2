from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.
def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
        
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title("Movies per year")
    plt.xlabel("Year")
    plt.ylabel("Number of movies")
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode("utf-8")
    
    ################################################
    
    matplotlib.use('Agg')
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    movie_counts_by_genre = {}
    for genre in genres:
        first_genre = genre.split(", ")
        
        if first_genre[0]:
            movies_in_genre = Movie.objects.filter(genre=first_genre[0])
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            first_genre = "None"
        count = movies_in_genre.count()
        movie_counts_by_genre[first_genre[0]] = count
        
    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_genre))
    
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title("Movies per genre")
    plt.xlabel("Genre")
    plt.ylabel("Number of movies")
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    
    image_png1 = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png1)
    graphic1 = graphic1.decode("utf-8")
    
    
    return render(request, 'statistics.html', {"graphic": graphic, "graphic1": graphic1})
    
def home(request):
    #return HttpResponse('<h1>Welcome to home page</h1>')
    #return render(request, 'home.html', {'name': 'Camilo Ortegón Saugster'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    #movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    return render(request, 'about.html',)