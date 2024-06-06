import frontmatter
from pathlib import Path
import os
from colorama import Fore

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

markdown_folder = Path(r"static\markdown")
md_home = frontmatter_hunter(markdown_folder, 'home', True)
path, content = md_home[0]
