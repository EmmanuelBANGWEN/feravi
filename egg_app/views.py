from django.shortcuts import render, redirect
from .models import Data
from .forms import DataForm
import plotly.express as px
import pandas as pd
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def home(request):
    # Récupération de toutes les données de la base
    dataset = Data.objects.all().order_by('-date')  # Trier par date décroissante

    paginator = Paginator(dataset, 5)
    page = request.GET.get('page')
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger :
        dataset = paginator.page(1)
    except EmptyPage :
        dataset = paginator.page(paginator.num_pages)
        
    context = {
        'dataset' : dataset,
        'page'  : page,

}

    return render(request, "home.html", context)

def add_data(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_data")  # Redirige vers la même page après soumission
    else:
        form = DataForm()
    
    return render(request, "add_data.html", {"form": form})


def dashboard(request):
    # Récupération des données
    dataset = Data.objects.all()
    
    # Transformation en DataFrame pandas
    df = pd.DataFrame(list(dataset.values()))
    
    # Vérifier si le DataFrame n'est pas vide
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])  # Convertir en format datetime
        df = df.sort_values(by="date")  # Trier par date croissante

        # Graphique de l'évolution de la température
        # fig_temp = px.line(df, x="date", y="temperature", title="Évolution de la Température")
        fig_temp = px.line(df, x="date", y="temperature")

        # Graphique de l'humidité
        # fig_humidity = px.line(df, x="date", y="humidity", title="Évolution de l’Humidité")
        fig_humidity = px.line(df, x="date", y="humidity")

        # Graphique du nombre d'œufs
        # fig_eggs = px.bar(df, x="date", y="egg_count", title="Production d'œufs quotidienne")
        fig_eggs = px.bar(df, x="date", y="egg_count")

        # Conversion en JSON pour Plotly
        temp_graph = fig_temp.to_html(full_html=False)
        humidity_graph = fig_humidity.to_html(full_html=False)
        egg_graph = fig_eggs.to_html(full_html=False)
        
    else:
        temp_graph = humidity_graph = egg_graph = "<p class='text-center'>Aucune donnée disponible</p>"

    return render(request, "dashboard.html", {
        "temp_graph": temp_graph,
        "humidity_graph": humidity_graph,
        "egg_graph": egg_graph,
    })



def documentation(request):
    return render(request, "documentation.html")

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect 


def delete(request, date):
    try:
        enregistrement = Data.objects.get(date=date)
        enregistrement.delete()
        messages.success(request, "L'animal a été supprimé avec succès.")
    except Data.DoesNotExist:
        messages.error(request, "Cet animal n'existe pas ou ne vous appartient pas.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
