from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Upload, Token
from PIL import Image
from django.conf import settings
import zipfile
from os.path import basename
from django.http import FileResponse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
import PIL
from PIL import ExifTags

# Create your views here.


def home(request):
    return render(request, 'size_reducer/home.html')


def compressImage(image, quality):
    imageTemproary = Image.open(image)
    try:
        if hasattr(imageTemproary, '_getexif'):
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            e = imageTemproary._getexif()
            if e is not None:
                exif = dict(imageTemproary._getexif().items())

                if exif[orientation] == 3:
                    imageTemproary = imageTemproary.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    imageTemproary = imageTemproary.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    imageTemproary = imageTemproary.rotate(90, expand=True)

    except:
        print('except')
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream, format='JPEG', quality=quality)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split(
            '.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image
    else:
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
            token = request.session['tabid']
            del request.session['tabid']
        except:
            return render(request, 'size_reducer/size_reducer_list.html')
        images = Upload.objects.filter(token__token=token)
        ctx = {'images': images}
        return render(request, 'size_reducer/size_reducer_list.html', ctx)

    def post(self, request):
        quality = 0
        myimage = request.FILES['myimage']
        image_size = (myimage.size)/1024
        token = request.POST['tabID']
        request.session['tabid'] = token
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
        for i in range(1, 11):
            img = compressImage(myimage, i*quality)
            obj = Upload(image=img, token=token)
            obj.save()
        return redirect('size_reducer:all')


class MakeZip(View):
    def get(self, request):
        print(request.method)
        images = Upload.objects.all()
        with zipfile.ZipFile('images.zip', 'w', compression=zipfile.ZIP_DEFLATED) as my_zip:
            for img in images:
                my_zip.write(img.image.path, basename(img.image.path))
        zipPath = os.path.join(settings.BASE_DIR, 'images.zip')
        print(zipPath)
        zip_file = open(zipPath, 'rb')
        return FileResponse(zip_file)


def data_delete(request, tabid):
    data = {'abcd': 'abcd'}
    Token.objects.get(token=tabid).delete()
    return JsonResponse(data)
