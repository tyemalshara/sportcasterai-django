from django.shortcuts import render
# important for the submit button
from django.http import JsonResponse
# from .forms import UserForm
from deta import Deta

from django import forms

class UserForm(forms.Form):
  name = forms.CharField(max_length=100)
  email = forms.EmailField()

# Initialize with your Deta projekt key
deta = Deta("a0Yy6gYJLcQ_TobRutGjhCdDHEFvTc2qd594Ri21yQkC")  # xBbzEnGL_Zdd29Vs4CrAMHsr4mvVoQtYrk7bdevJH
db = deta.Base("beef")

# Create your views here.

def index(request):
  return render(request,"index.html", {})

def handler404(request, exception):
  # we add the path to the 404.html file here.
  # The name of our HTML file is 404.html
  return render(request, "404.html")

def submit(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      email = form.cleaned_data['email']
      # we save the data to the database
      db.insert({"name": name, "email": email})
      return JsonResponse({"message": "Data submitted successfully"}, status=200)
    else:
      return JsonResponse({"error": "Invalid form data"}, status=400)
  else:
    form = UserForm()
  return render(request, "form.html", {'form': form})

def login(request):
  return render(request, "login.html")