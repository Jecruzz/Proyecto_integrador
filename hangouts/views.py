from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "dashboard.html")


def events(request):
    return render(request, "events.html")


def create_event(request):
    return render(request, "create_event.html")


def profile(request):
    return render(request, "profile.html")


def register(request):
    return render(request, 'register.html')


