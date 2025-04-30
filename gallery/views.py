from django.shortcuts import render, redirect
from .models import GalleryImage
from .forms import GalleryImageForm


# Create your views here.
def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, "gallery/index.html", {"images": images})