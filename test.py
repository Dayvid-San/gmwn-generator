import os
from pathlib import Path
import frontmatter
from markdown_it import MarkdownIt

def markdown_files(folder):
    file_tree = []
    for root, dirs, files in os.walk(folder):
        # Ignorar pastas que começam com um ponto
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                file_tree.append(file_path)
    return file_tree

path = r"static\markdown"
for files in markdown_files(path):
    print(files)

# def frontmatter_hunter(folder: Path, key: str, value: str):
#     matched_files = []
#     markdown_file_paths = markdown_files(folder)
#     for file_path in markdown_file_paths:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             post = frontmatter.load(f)
#             if key in post and post[key] == value:
#                 matched_files.append((file_path, post.content))
#     return matched_files

# def HTML_render(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         markdown = f.read()
#     md = MarkdownIt()
#     return md.render(markdown)


# Exemplo de uso
# folder = Path(r"C:\Users\Guilherme Freire\Guilhermwn's Garden")

# folder = Path(r"static\markdown")
# matched_files = frontmatter_hunter(folder, 'home', True)
# # print(matched_files)


# for file_path, content in matched_files:
#     print(HTML_render(file_path))
#     print(content)
#     print("\n" + "="*50 + "\n")

# content = frontmatter.load("")