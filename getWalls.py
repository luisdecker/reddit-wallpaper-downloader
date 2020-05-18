#--------------------------------------
#Este script é uma reprodução
#descarada de um script que achei
#no reddit. Somente para estudar um
#pouco das interface web e essas coisas
#que não são de deus. 
#--------------------------------------

################################
#         CONFIGURACAO         #
################################

#Diretório ao qual serão salvas as imagens
directory = '/home/decker/Wallpapers'
#Subreddit padrão para baixar as imagens
subreddit = 'HDR'
#Largura mínima da imagem
min_width = 1920
#Altura mínima da imagem
min_height = 1080
#Quantos posts obter por request (Max 100)
json_limit = 100
#Numero de iteracoes
loops = 2

HEADERS = {'User-agent':'getWallpapers'}

################################
#           IMPORTS            #
################################

import os
from os.path import expanduser
import sys
import requests
import urllib
from PIL import ImageFile
import socket


################################
#           FUNÇÕES            #
################################

""" Retorna falso em caso de código de erro """
def valid_URL(URL):
    return (requests.get(URL,headers=HEADERS).status_code != 404)

""" Cria o diretório de destino """
def prepare_directory(directory):
    if not os.path.exists(directory):
        print("Path '{}' dosn't exist, creating it!".format(directory))
        os.makedirs(directory)

""" Verifica se o sub existe """
def verify_subereddit(subreddit):
    URL = 'https://reddit.com/r/{}.json'.format(subreddit)
    try:
        requests.get(URL,headers=HEADERS).json()['error']
        return False
    except:
        return True

""" Retorna uma lista de posts de um sub como um json """
def get_posts(subreddit,loops,after):#TODO: talvez retornar somente os validos?
    all_posts = []

    i = 0
    for i in range(loops):
        URL = 'https://reddit.com/r/{}/top/.json?t=all&limit={}&after={}'.format(subreddit, json_limit, after)
        posts = requests.get(URL,headers=HEADERS).json()
        all_posts += posts['data']['children']
        after = posts['data']['after']
    return all_posts
""" Verifica se o URL é uma imagem """
def is_image(URL:str):
    return URL.endswith(('.png','.jpg','.jpeg'))

def is_HD(URL,min_width,min_height):
    file = urllib.request.urlopen(URL)
    size = file.headers.get("content-lenght")
    if size: size = int(size)
    p = ImageFile.Parser()
    while(True):
        data = file.read(1024)
        if not data:
            file.close()
            return False
        p.feed(data)
        if p.image:
            #file.close() #Maybe this wont work
            return (p.image.size[0] >= min_width and p.image.size[1] >= min_height)

""" Checa se a imagem é paisagem """
def is_landscape(URL):
    file = urllib.request.urlopen(URL)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            # return p.image.size
            if p.image.size[0] >= p.image.size[1]:
                return True
                break
            else:
                return False
                break
    file.close()
    return False

""" Checa se a imagem já foi baixada """
def already_dowloaded(URL):
    img_name = os.path.basename(URL)
    local_file_path = os.path.join(directory,img_name)
    return os.path.isfile(local_file_path)

""" Checa se a imagem vem do imgur ou reddit """
def known_URL(post):
    return post.lower().startswith('https://i.redd.it/') or post.lower().startswith('https://i.imgur.com/') or post.lower().startswith('http://i.imgur.com/') or post.lower().startswith('http://imgur.com')

""" Verifica se a imagem da URL etá armazenada localmente """
def store_img(post):
    return urllib.request.urlretrieve(post, os.path.join(directory, os.path.basename(post)))


################################
#            CORES             #
################################
DARK = '\033[1;30m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
ORANGE = '\033[1;33m'
PURPLE = '\033[1;35m'
NC = '\033[0m'


################################
#             MAIN             #
################################

#Cria o diretório
directory = expanduser(directory)
prepare_directory(directory)

#Verifica se é um sub válido
if not verify_subereddit(subreddit):
    print ("Você tem certeza que {} é um subreddit?".format(subreddit))
    sys.exit()

#Começa na primeira página
after = ''

#Armazena os posts
posts = get_posts(subreddit,loops,after)

#Numero da operacao
index = 1

#Numero de imagens baixadas
downdoaded = 0

#Mensagem inicial
print()
print(DARK + '--------------------------------------------' + NC)
print(PURPLE + 'Downloading to      : ' + ORANGE + directory + NC)
print(PURPLE + 'From r/             : ' + ORANGE + subreddit + NC)
print(PURPLE + 'Minimum resolution  : ' + ORANGE + str(min_width) + 'x' + str(min_height) + NC)
print(PURPLE + 'Maximum downloads   : ' + ORANGE + str(json_limit*loops) + NC)
print(DARK + '--------------------------------------------' + NC)
print()

#Percorre todos os posts
for post in posts:
    try:
        #Pegando a URL
        URL = post['data']['url']
        title = post['data']['title']

        #Ignora caso 404
        if not valid_URL(URL):
            print(RED + '{}) 404 error'.format(index) + NC)
            print(RED + '{})'.format(title) + NC + '\n')
            index += 1
            continue
        #Ignora url desconhecida
        if not known_URL(URL):
            print(RED + '{}) Skipping unknown URL'.format(index) + NC)
            print(RED + '{})'.format(URL) + NC)
            print(RED + '{})'.format(title) + NC + '\n')
            index += 1
            continue
        #Ignora retrato
        if not is_landscape(URL):
            print(RED + '{}) Skipping portrait image'.format(index) + NC)
            print(RED + '{})'.format(title) + NC + '\n')
            index += 1
            continue
        #Ignora imagens pequenas
        if not is_HD(URL,min_width,min_height):
            print(RED + '{}) Skipping low resolution image'.format(index) + NC)
            print(RED + '{})'.format(title) + NC + '\n')
            index += 1
            continue
        #Ignora se já foi baixada
        if already_dowloaded(URL):
            print(RED + '{}) Skipping already downloaded image'.format(index) + NC)
            print(RED + '{})'.format(title) + NC + '\n')
            index += 1
            continue
        #Baixa uma imagem nova válida
        if store_img(URL):
            print(GREEN + '{}) Downloaded {}'.format(index, os.path.basename(URL)) + NC)
            print(GREEN + '{})'.format(title) + NC + '\n')
            downdoaded += 1
            index += 1
        else:
            print(RED + 'Unexcepted error' + NC + "\n")
            index += 1
    except requests.exceptions.ConnectionError:
        print(RED + 'Unexcepted error' + NC + "\n")
    
#Mostra estatísticas da sessão
print("{} imagens do {} baixadas na pasta {}".format(downdoaded,subreddit,directory))    
    



