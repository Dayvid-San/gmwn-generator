# ================================
# IMPORTAÇÕES

# Dependências FastAPI
from fastapi import FastAPI, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# Dependências
from markdown_it import MarkdownIt
from typing import Optional
from colorama import Fore 
from pathlib import Path
import frontmatter
import os

# ================================
# CONSTANTES

folder = "static"
templates = Jinja2Templates(directory="public")

# ================================
# FUNÇÕES

def static_directory(folder:str):
    return StaticFiles(directory=folder)

def response(html: str, request: Request, **kwargs):
    context = {"request": request}
    context.update(kwargs)
    return templates.TemplateResponse(html, context)


def HTML_render(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    md = MarkdownIt()
    return md.render(markdown)

def markdown_files_names(folder):
    file_tree = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):            
                file_tree.append(file.split('.md')[0])
    return file_tree

def markdown_files_path(folder):
    file_tree = []
    for root, dirs, files in os.walk(folder):
        # Ignorar pastas que começam com um ponto
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                file_tree.append(file_path)
    return file_tree

def frontmatter_hunter(folder: Path, key: str, value: str):
    matched_files = []
    markdown_file_paths = markdown_files_path(folder)
    for file_path in markdown_file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            if key in post and post[key] == value:
                matched_files.append([file_path, post.content])
            if len(matched_files) > 1:
                raise Exception(Fore.RED + f"More than one file containing the '{key}' property." + Fore.RESET)
    return matched_files

# ================================
# APLICAÇÃO FASTAPI

app = FastAPI()
app.mount(
    path=f"/{folder}", 
    app=static_directory(folder),
    name=folder)

# ================================
# ROTAS E REQUISIÇÕES FASTAPI

# CONSTANTES DE CONFIGURAÇÃO DAS REQUISIÇÕES
markdown_folder = Path(r"static\markdown")
file_name_list = markdown_files_names(markdown_folder)
file_path_list = markdown_files_path(markdown_folder)
html_content = "content"

# REQUISIÇÕES HTTP
@app.get('/')
async def homepage(request: Request):
    md_home = frontmatter_hunter(markdown_folder, 'home', True)
    home_path, home_content = md_home[0]
    
    for name in file_name_list:
        name = str(name)
        home_path = str(home_path)
        if name in home_path:
            return RedirectResponse(url=f'/{name}')

@app.get('/{file}')
async def file_access(file: str, request: Request):
    html_content = "content"
    for file_path in file_path_list:
        str_path = str(file_path)
        if file in str_path:    
            with open(str_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f).content
            html_content = MarkdownIt().render(post)
    return response(
        "index.html",
        request,
        content=html_content,
        file_list=file_name_list
    )