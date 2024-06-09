import re
import os
from pathlib import Path
import frontmatter
from typing import List, Optional
from colorama import Fore 

# ============================================
# FUNÇÕES

def markdown_files_path(folder):
    """
    Gera uma lista de caminhos completos para todos os arquivos markdown (.md) em um diretório e seus subdiretórios.

    Parâmetros:
    folder (str): O caminho para o diretório onde a busca pelos arquivos markdown começará.

    Retorna:
    List[Path]: Uma lista de objetos Path representando os caminhos completos dos arquivos markdown encontrados.

    Explicação:
    - A função usa `os.walk` para percorrer recursivamente o diretório especificado por `folder` e todos os seus subdiretórios.
    - Para cada diretório visitado, a lista `dirs` é modificada para ignorar diretórios que começam com um ponto (.), como '.git' ou '.vscode'.
    - Para cada arquivo encontrado no diretório atual:
      - Se o arquivo termina com '.md' (indicando que é um arquivo markdown), o caminho completo para o arquivo é construído e adicionado à lista `file_tree`.
    - No final, a função retorna a lista `file_tree`, que contém os caminhos completos para todos os arquivos markdown encontrados.
    
    Exemplo de uso:
    - Suponha que a estrutura do diretório seja:
    /example_folder
    ├── file1.md
    ├── subfolder
    │   └── file2.md
    └── .hidden_folder
        └── file3.md
    
    Output: [Path('/example_folder/file1.md'), Path('/example_folder/subfolder/file2.md')]
    ```
    """
    file_tree = []
    for root, dirs, files in os.walk(folder):
        # Ignorar pastas que começam com um ponto
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                file_tree.append(file_path)
    return file_tree

def create_hierarchy_from_paths(paths: List[Path]):
    """
    Cria uma hierarquia de diretórios e arquivos a partir de uma lista de caminhos.

    Parâmetros:
    paths (List[Path]): Uma lista de objetos Path representando os caminhos dos arquivos.

    Retorna:
    List[Dict[str, Any]]: Uma lista de dicionários representando a hierarquia de diretórios e arquivos.

    Explicação:
    - A função define uma função interna `add_to_tree` para adicionar recursivamente caminhos à hierarquia.
    - `add_to_tree`:
      - Se `components` tiver apenas um item, adiciona-o como um arquivo à lista `children`.
      - Caso contrário, trata o primeiro componente como um diretório e verifica se ele já existe na árvore.
      - Se o diretório não existir, cria uma nova entrada para ele e o adiciona à lista `children`.
      - Ordena a lista `children` para garantir que os diretórios apareçam antes dos arquivos.
      - Chama-se recursivamente com os componentes restantes do caminho.
    - Inicializa a estrutura `hierarchy` com uma raiz vazia.
    - Para cada caminho em `paths`, remove o prefixo do caminho base para começar a partir da pasta especificada e divide o caminho em componentes.
    - Chama `add_to_tree` para adicionar cada caminho à hierarquia.
    - Retorna a lista `children` da raiz da hierarquia, representando a estrutura final.
    
    Exemplo de uso:
    
    Suponha que os caminhos sejam:
    /example_folder/file1.md
    /example_folder/subfolder/file2.md
    /example_folder/subfolder/subsubfolder/file3.md

    Output:
    [
        {'id': 'example_folder', 'children': [
            {'id': 'file1.md'},
            {'id': 'subfolder', 'children': [
                {'id': 'file2.md'},
                {'id': 'subsubfolder', 'children': [
                    {'id': 'file3.md'}
                ]}
            ]}
        ]}
    ]
    """
    def add_to_tree(tree, components):
        if len(components) == 1:
            tree['children'].append({'id': components[0]})
        else:
            folder_name = components[0]
            remaining_components = components[1:]
            # Verificar se a pasta já está na árvore
            folder = next((item for item in tree['children'] if item['id'] == folder_name and 'children' in item), None)
            if folder is None:
                folder = {'id': folder_name, 'children': []}
                tree['children'].append(folder)
                # Reorganizar para manter pastas antes dos arquivos
                tree['children'].sort(key=lambda x: ('children' not in x, x['id']))
            # Recursivamente adicionar os componentes restantes
            add_to_tree(folder, remaining_components)
    
    # Estrutura inicial da árvore
    hierarchy = {'id': 'root', 'children': []}
    
    for path in paths:
        # Ignorar o prefixo do caminho base para começar a partir da pasta especificada
        components = path.relative_to(path.anchor).parts
        add_to_tree(hierarchy, components)
    
    return hierarchy['children']

def compose_path(filename: str, path_list: List[str]) -> Optional[str]:
    """
    Procura um arquivo em uma lista de caminhos e retorna o caminho completo se encontrado.

    Parâmetros:
    filename (str): O nome do arquivo a ser procurado.
    path_list (List[str]): Uma lista de strings representando os caminhos dos arquivos.

    Retorna:
    Optional[str]: O caminho completo do arquivo encontrado, ou None se não for encontrado.

    Explicação:
    - A função compila uma expressão regular a partir do `filename` usando `re.escape` para tratar o `filename` como uma string literal.
    - Itera sobre cada `path` na `path_list`:
      - Converte o `path` para string, caso não seja.
      - Usa `re.search` para verificar se o `filename` está presente no `path`.
      - Se encontrado, retorna o `path` completo.
    - Retorna None ao final, indicando que a busca terminou e o arquivo não foi encontrado.
    
    Exemplo de uso:
    
    Suponha que a lista de caminhos seja:
    ```python
    paths = ['/path/to/mdown.md', '/another/path/to/somefile.txt']
    result = compose_path('mdown.md', paths)
    ```
    Output: '/path/to/mdown.md' (Se o caminho for encontrado, caso contrário None)
    """
    if filename is None:
        return None
    pattern = re.compile(re.escape(filename))  # Usar re.escape para evitar problemas com caracteres especiais
    for path in path_list:
        path = str(path)
        if re.search(pattern, path):
            return path
    return None  # Adicionar retorno explícito caso não encontre



def frontmatter_hunter(folder: Path, key: str, value: str):
    """
    Procura arquivos markdown em um diretório que contenham uma chave e valor específicos no frontmatter.

    Parâmetros:
    folder (Path): O caminho para o diretório onde a busca pelos arquivos markdown começará.
    key (str): A chave do frontmatter a ser procurada.
    value (str): O valor associado à chave do frontmatter a ser procurado.

    Retorna:
    List[List[Any]]: Uma lista contendo sublistas com o caminho do arquivo e o conteúdo do arquivo markdown correspondente.

    Levanta:
    Exception: Se mais de um arquivo contiver a chave especificada no frontmatter.
    
    Explicação:
    - A função começa chamando `markdown_files_path` para obter uma lista de todos os arquivos markdown no diretório e subdiretórios especificados.
    - Inicializa uma lista `matched_files` para armazenar os arquivos que correspondem aos critérios de busca.
    - Para cada caminho de arquivo markdown encontrado:
      - Abre o arquivo e carrega seu conteúdo usando `frontmatter`.
      - Verifica se a chave especificada está presente no frontmatter e se o valor corresponde.
      - Se uma correspondência for encontrada, adiciona o caminho do arquivo e seu conteúdo à lista `matched_files`.
      - Se mais de um arquivo corresponder aos critérios, lança uma exceção indicando a duplicidade.
    - Retorna a lista de arquivos correspondentes.
    """
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
