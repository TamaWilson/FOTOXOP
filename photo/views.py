from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, render_to_response
from PIL import Image
import PIL.ImageOps
from PIL import ImageEnhance


#Função chamada ao requisitar a view do index
def index(request):

    #rendezira o template da index
    return render(request, 'photo/index.html')


#Função chamada ao requisitar a view de uploar
def upload(request):

    #checa que se a requisição veio via POST e se o arquivo existe
    if request.method == 'POST' and request.FILES.get('myfile', False): #se não houver a chave 'myfile' o valor padrão é False

        #instancia uma variavel com o conteúdo do dicionario de arquivos
        myfile = request.FILES['myfile']

        #instancia um objeto para manipular o armazenamento de arquivos
        fs = FileSystemStorage()

        #salva o arquivo enviado com o nome original
        filename = fs.save(myfile.name, myfile)

        #SALVA UMA COPiA DO ARQUIVO ORIGINAL
        original_file = fs.base_location + "\\ORIGINAL_" + myfile.name

        fs.save(original_file, myfile)

        #captura a url do arquivo
        uploaded_file_url = fs.url(filename)

        #abre o arquivo com PIL passando o caminho absoluto para o arquivo no servidor
        image = Image.open(fs.base_location + "\\" + filename)


        #utiliza a propriedade size para retornar a altura e largura da imagem
        #image.size retorna uma tupla
        width, height = image.size

        #cria um dicionário com as variaveis de contexto
        context = {
            'uploaded_file_url': uploaded_file_url, #caminho para o arquivo
            'uploaded_filename' : filename, #nome do arquivo
            'width' : width, #largura
            'height' : height #altura
        }

        return render(request, 'photo/canvas.html', context) #renderiza o template com o contexto
    return redirect('/fotoxop') #Caso a condicao do IF seja falsa, retorna para a página inicial

@csrf_exempt #ignora a exigência do csrf cookie - apenas para fins didáticos
def rotate(request):
    #Checa se a requisição veio via POST
    if request.method == 'POST':

        #Lê o filename do dicionário POST
        myfile = request.POST['filename']

        #Lê o ângulo do dicionário POST
        angle = int(request.POST['angle'])

        #Instancia do objeto de manipulação do armazenamento
        fs = FileSystemStorage()

        #Monta o caminho absoluto para o arquivo
        filename = fs.base_location + "\\" + myfile

        #Abre a imagem com PILLOW
        image = Image.open(filename)

        #Rotaciona a imagem com o ângulo indicado
        #expand=true - o tamanho é ajustado para as novas dimensões após a rotação
        #caso expand=false os valores de altura x largura permanecem inalterados
        rotated = image.rotate(angle, expand=True)

        #salva a imagem rotacionada por cima da original
        rotated.save(filename)

        #monta a url para o arquivo
        uploaded_file_url = fs.url(myfile)

        #retorna com a renderização do template de atualização e o filename do arquivo
        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop') #Se a requisição não veio via POST retorna redirecionara para a index

@csrf_exempt #ignora a exigência do csrf cookie - apenas para fins didáticos
def invert(request):
    # Checa se a requisição veio via POST
    if request.method == 'POST':
        # Lê o filename do dicionário POST
        myfile = request.POST['filename']

        # Instancia do objeto de manipulação do armazenamento
        fs = FileSystemStorage()

        # Monta o caminho absoluto para o arquivo
        filename = fs.base_location + "\\" + myfile

        # Abre a imagem com PILLOW
        image = Image.open(filename)

        #Inverte as cores
        inverted = PIL.ImageOps.invert(image)

        #Salva a imagem invertida por cima da original
        inverted.save(filename)

        # monta a url para o arquivo
        uploaded_file_url = fs.url(myfile)

        # retorna com a renderização do template de atualização e o filename do arquivo
        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop') #Se a requisição não veio via POST retorna redirecionara para a index

@csrf_exempt
def contrast(request):
    if request.method == 'POST':
        myfile = request.POST['filename']

        # Lê o level passado pelo usuário, divide por a escala em HTML varia de 0 a 100.
        # A posição padrão do level é no 50 no html é 50, divimos por esse valo para o Pillow entender como 1.0
        level = float(request.POST['level'])/50


        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        #Instanciando um objeto da classe ImageEnhance.Constrast, passando a imagem a ser manipulada
        enh = ImageEnhance.Contrast(image) #0 = imagem sem contraste, 1.0= Nível Padrão (Nada alterado), 2.0 = Contraste máximo permitido

        #Aplica o contraste com o level indicado pelo usuário
        contrast = enh.enhance(level)

        #Salva a imagem alterada por cima da original
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

        #Objeto do timpo ImageEnhance.Brightness - BRILHO
        enh = ImageEnhance.Brightness(image)
        brightness = enh.enhance(level) #0 nenhum brilho, 1.0 = Nenhuma alteração, 2.0 = brilho máximo permitido

        brightness.save(filename)

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

        #Objeto de manipulação da cor
        enh = ImageEnhance.Color(image)
        color = enh.enhance(level) #0 Sem cor = Cinza, 1.0 - não altera, 2.0 cor no máximo permitido

        color.save(filename)

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

        #Objeto recebendo a imagem em escala de cinza
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
        width = int(request.POST['width']) #captura do dicionário POST a largura
        height = int(request.POST['height']) #captura do dicionário POST a altura

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        image = Image.open(filename)

        #Image.Image.resize = redimensionar a imagem com os valores coloados pelo usuário
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
        value = request.POST['channel'] #Verifica o canal a ser exibido
        #R - Red
        #G - Green
        #B - Blue
        #RGB - Recuperado no javascript

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        #monta um novo filename
        newFilename = fs.base_location + "\\CHANNEL" + myfile

        image = Image.open(filename)

        #Cria um dicionario com as chaves de cada cor
        colors = { 'R' : 0, 'B': 0, 'G': 0 }

        #Image.Image.Split retorna uma tupla com 3 imagens, uma para cada canal
        #As imagens são atribuidas cada uma para uma chave do dicionário Colors
        colors['R'], colors['G'], colors['B'] = Image.Image.split(image)

        #Splited recebe um valor de Colors de acordo com o valor atribuido para Value (R, G ou B)
        splited = colors[value] #colors['B'] = retorna o canal Blue

        #salva uma nova imagem
        splited.save(newFilename)


        #retorna a url do novo arquivo
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

        #Aplica a inversão na imagem
        mirrored = PIL.ImageOps.mirror(image)

        mirrored.save(filename)

        uploaded_file_url = fs.url(myfile)

        return render_to_response('photo/updated.html',  {
            'uploaded_file_url': uploaded_file_url
        })
    return redirect('/fotoxop')

@csrf_exempt
def reset(request):
    if request.method == 'POST':
        myfile = request.POST['filename']

        fs = FileSystemStorage()
        filename = fs.base_location + "\\" + myfile

        original_filename = fs.base_location + "\\ORIGINAL_" + myfile

        original_file = fs.open(original_filename)

        fs.delete(filename)

        fs.save(filename, original_file)

        uploaded_file_url = fs.url(filename)

        return render_to_response('photo/updated.html', {
            'uploaded_file_url': uploaded_file_url
        })