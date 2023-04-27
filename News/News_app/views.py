import csv
from django.shortcuts import render
from .models import Article

def render_content(filename):
    articles = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            article = Article(
                headline=row['headlines'],
                date = row['date'],
                time = row['time'],
                image_url=row['image_url'],
                text=row['summary'],
                read_more_url=row['read_more']
            )
            articles.append(article)
    return articles

def article_misc(request):
    file_misc =  'News/Backend/Static/output_misc_fin.csv'
    articles = render_content(file_misc)
    return render(request, 'index.html', {'articles': articles})
def article_pol(request):
    file_misc =  'News/Backend/Static/output_pol_fin.csv'
    articles = render_content(file_misc)
    return render(request, 'index.html', {'articles': articles})
def article_world(request):
    file_misc =  'News/Backend/Static/output_worl_fin.csv'
    articles = render_content(file_misc)
    return render(request, 'index.html', {'articles': articles})

def article_tech(request):
    file_misc =  'News/Backend/Static/output_tech_fin.csv'
    articles = render_content(file_misc)
    return render(request, 'index.html', {'articles': articles})