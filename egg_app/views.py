from django.shortcuts import render, redirect
from .models import Data
import plotly.express as px
import pandas as pd
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from .forms import DataForm, CreateUserForm, LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    # Récupération de toutes les données de la base
    dataset = Data.objects.all().order_by("-date", "-time_slot")  # Trier par date et heure décroissantes


    paginator = Paginator(dataset, 6)
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

@login_required(login_url='login')
def add_data(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            time_slot = form.cleaned_data["time_slot"]

            # Vérifie si un relevé existe déjà pour ce créneau
            if Data.objects.filter(date=date, time_slot=time_slot).exists():
                messages.error(request, "Les données pour ce créneau horaire existent déjà !")
            else:
                form.save()
                messages.success(request, "Données enregistrées avec succès !")
            return redirect("add_data")  
    else:
        form = DataForm()

    return render(request, "add_data.html", {"form": form})

from .forms import DateFilterForm

def dashboard(request):
    form = DateFilterForm(request.GET)  # Récupération des valeurs du formulaire


    dataset = Data.objects.all().order_by("date", "time_slot")  # Trier par date et heure

    # Appliquer les filtres si présents
    if form.is_valid():
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        time_slot = form.cleaned_data.get("time_slot")

        if start_date:
            dataset = dataset.filter(date__gte=start_date)
        if end_date:
            dataset = dataset.filter(date__lte=end_date)
        if time_slot:  # Filtrer par créneau horaire
            dataset = dataset.filter(time_slot=time_slot)

    df = pd.DataFrame(list(dataset.values()))

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])  
        df = df.sort_values(by=["date", "time_slot"])  # Trier par date et créneau

        # Graphique des températures par créneau
        fig_temp = px.line(df, x="date", y="temperature", color="time_slot")
        fig_humidity = px.line(df, x="date", y="humidity", color="time_slot")
        fig_eggs = px.bar(df, x="date", y="egg_count", color="time_slot")
        # Nouveau graphique: Relation humidité vs production d'œufs
        fig_humidity_eggs = px.scatter(
            df,
            x="humidity",
            y="egg_count",
            color="time_slot",
            # title="Humidité vs Production d'œufs",
            labels={"humidity": "Humidité (%)", "egg_count": "Nombre d'œufs"}
        )
        humidity_eggs_graph = fig_humidity_eggs.to_html(full_html=False, config={"responsive": True})
        fig_temp_eggs = px.scatter(
            df,
            x="temperature",
            y="egg_count",
            color="time_slot",
            # title="temperature vs Production d'œufs",
            labels={"temperature": "temperature (celcius)", "egg_count": "Nombre d'œufs"}
        )
        temp_eggs_graph = fig_temp_eggs.to_html(full_html=False, config={"responsive": True})

        fig_temp_humidity = px.scatter(
            df,
            x="temperature",
            y="humidity",
            color="time_slot",  # pour distinguer les créneaux
            # title="Corrélation Température vs Humidité",
            labels={"temperature": "Température (°C)", "humidity": "Humidité (%)"},
        )
        temp_humidity_graph = fig_temp_humidity.to_html(full_html=False, config={"responsive": True})


        temp_graph = fig_temp.to_html(full_html=False, config={"responsive": True})
        humidity_graph = fig_humidity.to_html(full_html=False, config={"responsive": True})
        egg_graph = fig_eggs.to_html(full_html=False, config={"responsive": True})
    else:
        temp_graph = humidity_graph = egg_graph = "<p class='text-center'>Aucune donnée disponible</p>"

    return render(request, "dashboard.html", {
        "form": form,
        "temp_graph": temp_graph,
        "humidity_graph": humidity_graph,
        "egg_graph": egg_graph,
        "humidity_eggs_graph": humidity_eggs_graph,  
        "temp_eggs_graph": temp_eggs_graph,
        "temp_humidity_graph": temp_humidity_graph, 

    })



def documentation(request):
    return render(request, "documentation.html")


def login_view(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect("home")  # Redirection vers la page d'accueil
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    
    else:
        form = LoginUserForm()

    return render(request, "login.html", {"form": form})

def logout(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("login")

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous maintenant.")
            return redirect("login")
    else:
        form = CreateUserForm()

    return render(request, "register.html", {"form": form})
