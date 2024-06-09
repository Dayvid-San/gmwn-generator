# ============================================
# IMPORTAÇÕES

from nicegui import ui
from functions import *

# ============================================
# CONSTANTES
folder = 'markdown'  # Substitua pelo caminho da pasta desejada
paths = markdown_files_path(folder)
std_path = frontmatter_hunter(folder, 'home', True)[0]

current_note = None

# ============================================
# FUNÇÕES DE CONSTRUÇÃO

def mainlayout(paths_list):
    with ui.left_drawer() as left_drawer:
        hierarchy = create_hierarchy_from_paths(paths_list)
        # ESTILIZAÇÃO DA SIDEBAR
        left_drawer.classes('bg-slate-100')

        # CONTEÚDO DA SIDEBAR
        with ui.element().tooltip('Ir para página inicial'):
            ui.markdown('## Guilhermwn').on('click', lambda: ui.navigate.to('/'))
        with ui.row():
            ui.button('Back', on_click=ui.navigate.back)
            ui.button('Forward', on_click=ui.navigate.forward)
        
        # COMPONENTE ARVORE
        t = ui.tree(
            hierarchy,
            label_key='id',
            on_select=lambda element: ui.navigate.to(f'/{element.value}')
        ).expand()

    # COMPONENTE HEADER 
    with ui.header() as header:
        # TOGGLE DA SIDEBAR
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu')
# ============================================
# ROTAS DAS PÁGINAS

@ui.page('/')
async def index():
    mainlayout(paths)
    ui.markdown(std_path[1])

@ui.page('/{page}')
async def content_note(page):
    mainlayout(paths)
    page_path = compose_path(page, paths)
    with open(page_path, 'r', encoding='utf-8') as f:
        content = frontmatter.load(f).content
    ui.markdown(content)
    ui.label(page)
# ============================================
# EXECUÇÃO DO APP

ui.run(
    reload=True
)