from django.shortcuts import render
from markdown2 import Markdown  
from . import util
import random

def md_to_html(title):
    md = Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    return md.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    return render(request, "encyclopedia/article.html", {
        "article": md_to_html(title),
        "title":title
    })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        article_list = util.list_entries()
        found = []
        for t in article_list:
            if title == t:
                return render(request, "encyclopedia/article.html", {
                    "article": md_to_html(title),
                    "title": title,
                })
            elif title.lower() in t.lower():
                found.append(t)
        return render(request, "encyclopedia/search_results.html", {
            "found":found,
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    elif request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        titleExists = util.get_entry(title)
        if titleExists != None:
            return render(request, "encyclopedia/already_present.html", {
                "title": title,
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/article.html", {
                "article": md_to_html(title),
                "title": title,
            })

def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        return render(request, "encyclopedia/edit.html", {
            "article": util.get_entry(title),
            "title":title,

        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/article.html", {
            "article": md_to_html(title),
            "title": title,
        })

def random_page(request):
    list = util.list_entries()
    random_number = random.randint(0, len(list)-1)
    return render(request, "encyclopedia/article.html", {
        "article": md_to_html(list[random_number]),
        "title": list[random_number],
    })