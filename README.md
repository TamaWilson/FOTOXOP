# FOTOXOP

Projeto desenvolvido para seminário da disciplina Processamento de Imagens da UNDB.

# UTILIZADO

- Python 3.5
- Django 1.10 - Framework Python para web
- HTML, Jquery, CSS Bootstrap
- PILLOW - Fork da Pil para python 3.X


# Arquivos importantes

- VIEWS.PY (photo/views.py)
- URLS.py (fotoxop/urls.py e photo/ulrs.py)
- Tudo dentro da pasta /photo/templates/photo/

# + - como o Django funciona

Ao abrir uma URL é gerado uma requisição para o servidor, essa requisição é tratada pelos arquivos URLS.py, cada URL direciona para uma função diferente do VIEWS.py
Cada função do VIEWS.py retorna um template com um dicionario de contextos contendo as informações a serem renderizadas no navegador

Cada botão do sistema possui está atrelado a um listener do JQuery, para ser chamado no "On CLick", o botão invoca o ajax e manda a requisição necessária para o servidor tratar

* Dicionário em python nada mais é que um Hashmap com um outro nome
