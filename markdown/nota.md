# Descrição
HTMX é um framework para **html** que traz certas funcionalidades ao código html que atualmente só funcionariam com *javascript* incorporado.

## Funcionamento
Um exemplo básico do o que o HTMX proporciona:

Temos uma tag de âncora, um link comumente chamado.
```html
<a href="/blog">Blog</a>
```

Qual a funcionalidade que essa âncora faz, quando um usuário clica nele? A tag de âncora avisa ao navegador, para fazer uma requisição HTTP GET para o caminho "/blog", e carregar o conteúdo da resposta na janela.

Agora com HTMX temos mais algumas funcionalidades quando aplicamos ela às qualquer tag disponível:
```html
<button hx-post="/clicked" 
        hx-trigger="click" 
        hx-target="#parent-div" 
        hx-swap="outerHTML">
    Click Me!
</button>
```

> Essas novas funcionalidades avisam ao navegador para fazer uma requisição HTTP POST para o caminho "/clicked", e usar o conteúdo da resposta para substituir inteiramente o elemento com o id "parent-div".

### innerHTML e outerHTML

hx-swap="innerHTML"
- **Descrição**: Quando `hx-swap="innerHTML"` é usado, o conteúdo retornado pela requisição HTMX substitui apenas o conteúdo interno do elemento alvo, mantendo o elemento alvo em si no DOM.
- **Uso Comum**: É usado quando você deseja atualizar o conteúdo dentro de um contêiner, mas manter o próprio contêiner intacto.

hx-swap="outerHTML"
- **Descrição**: Quando `hx-swap="outerHTML"` é usado, o conteúdo retornado pela requisição HTMX substitui completamente o elemento alvo, incluindo ele próprio, pelo novo conteúdo.
- **Uso Comum**: É usado quando você deseja substituir o próprio elemento alvo no DOM por um novo conteúdo.