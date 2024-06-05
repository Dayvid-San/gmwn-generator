# ================================
# IMPORTAÇÕES

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from markdown_it import MarkdownIt

# ================================
# CONSTANTES

folder = "static"
templates = Jinja2Templates(directory="public")

# ================================
# FUNÇÕES

def static_directory(folder:str):
    return StaticFiles(directory=folder)

def response(html:str, request:Request, content:str):
    return templates.TemplateResponse(html, {"request": request, "content": content})

def HTML_render(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    md = MarkdownIt()
    return md.render(markdown)

# ================================
# APLICAÇÃO FASTAPI

app = FastAPI()
app.mount(
    path=f"/{folder}", 
    app=static_directory(folder),
    name=folder)

# ================================
# ROTAS E REQUISIÇÕES FASTAPI

@app.get("/")
async def index(request: Request):
    html_content = HTML_render(r'.\static\markdown\nota.md')
    return response("index.html", request, html_content)