from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import Upload, Token
from PIL import Image
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.conf import settings
import zipfile
from os.path import basename
from django.http import FileResponse
from django.forms import modelformset_factory
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def home(request):
    return render(request, 'size_reducer/home.html')


def compressImage(image, quality):
    imageTemproary = Image.open(image)
    imageTemproary = imageTemproary.convert('RGB')
    outputIoStream = BytesIO()
    imageTemproary.save(outputIoStream, format='JPEG', quality=quality)
    outputIoStream.seek(0)
    image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split(
        '.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
    return image


class MainView(View):
    def get(self, request):
        try:
            token = request.COOKIES['csrftoken']
            images = Upload.objects.filter(token__token=token)
        except:
            return render(request, 'size_reducer/size_reducer_list.html')
        ctx = {'images': images}
        return render(request, 'size_reducer/size_reducer_list.html', ctx)

    def post(self, request):
        quality = 0
        if request.FILES['myimage']:
            myimage = request.FILES['myimage']
            image_size = (myimage.size)/1024
            token = request.COOKIES['csrftoken']
            token = Token(token=token)
            token.save()

            if image_size > 100 and image_size < 400:
                quality = 5
            elif image_size > 400 and image_size < 700:
                quality = 6
            elif image_size > 700 and image_size < 1000:
                quality = 7
            elif image_size > 1000 and image_size < 2000:
                quality = 8
            else:
                quality = 9
            print(image_size)
            print(quality)
            for i in range(1, 11):
                img = compressImage(myimage, i*quality)
                obj = Upload(image=img, token=token)
                obj.save()
            return redirect('size_reducer:all')


def ImageDelete(request):
    success_url = 'size_reducer:all'
    if request.method == 'POST':
        token = request.COOKIES['csrftoken']
        Token.objects.get(token=token).delete()
    return redirect(success_url)


def MakeZip(request):
    images = Upload.objects.all()
    with zipfile.ZipFile('images.zip', 'w', compression=zipfile.ZIP_DEFLATED) as my_zip:
        for img in images:
            my_zip.write(img.image.path, basename(img.image.path))
    zipPath = os.path.join(settings.BASE_DIR, 'images.zip')
    print(zipPath)
    zip_file = open(zipPath, 'rb')
    return FileResponse(zip_file)


def data_delete(request):
    data = {'abcd': 'abcd'}
    token = request.COOKIES['csrftoken']
    Token.objects.get(token=token).delete()
    return JsonResponse(data)
