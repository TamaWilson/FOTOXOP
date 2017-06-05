from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
from PIL import Image
import PIL.ImageOps
from PIL import ImageEnhance





def index(request):
    return render(request, 'photo/index.html')


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()


        filename = fs.save(myfile.name, myfile,)
        uploaded_file_url = fs.url(filename)

        image = Image.open(fs.base_location + "\\" + filename)

        width, height = image.size

        context = {
            'uploaded_file_url': uploaded_file_url,
            'uploaded_filename' : filename,
            'width' : width,
            'height' : height
        }

        return render(request, 'photo/canvas.html', context)
    return redirect('/fotoxop')

@csrf_exempt
def rotate(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        angle = int(request.POST['angle'])


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        rotated = image.rotate(angle, expand=True)

        rotated.save(filename)

        uploaded_file_url = fs.url(myfile)
        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def invert(request):
    if request.method == 'POST':
        myfile = request.POST['filename']

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)
        inverted = PIL.ImageOps.invert(image)

        inverted.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def contrast(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        level = float(request.POST['level'])/50


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        enh = ImageEnhance.Contrast(image)
        contrast = enh.enhance(level)

        contrast.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')


@csrf_exempt
def bright(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        level = float(request.POST['level'])/50


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        enh = ImageEnhance.Brightness(image)
        contrast = enh.enhance(level)

        contrast.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')




@csrf_exempt
def color(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        level = float(request.POST['level'])/50


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        enh = ImageEnhance.Color(image)
        contrast = enh.enhance(level)

        contrast.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def grey(request):
    if request.method == 'POST':
        myfile = request.POST['filename']

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        grScale = PIL.ImageOps.grayscale(image)

        grScale.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def resize(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        width = int(request.POST['width'])
        height = int(request.POST['height'])

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        resized = Image.Image.resize(image,(width,height))

        resized.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')


@csrf_exempt
def channel(request):
    if request.method == 'POST':
        myfile = request.POST['filename']
        value = request.POST['channel']


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile
        newFilename = fs.base_location + "\\CHANNEL" + myfile
        image = Image.open(filename)

        colors = { 'R' : 0, 'B': 0, 'G': 0 }

        colors['R'], colors['G'], colors['B'] = Image.Image.split(image)

        splited = colors[value]


        splited.save(newFilename)

        uploaded_file_url = fs.url("CHANNEL" + myfile)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def mirror(request):
    if request.method == 'POST':
        myfile = request.POST['filename']

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)
        mirrored = PIL.ImageOps.mirror(image)

        mirrored.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')
