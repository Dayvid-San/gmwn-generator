## Descrição
Tailwind CSS é um framework CSS que possibilita usar classes já criadas, que combinadas podem criar qualquer design sem precisar escrever CSS.

### Funcionamento
Tailwind CSS funciona escaneando todos os arquivos html, componentes javascript e outros arquivos, procurando pelos nomes de classes que ele oferece, gerando assim os estilos em um arquivo CSS de saída os estilos correspondentes.

## Instalar

Instalar usando NODE Js `npm`
```shell
npm install -D tailwindcss
```

Configurar os caminhos com `tailwind.config.js`
Como:
- Pode ser criado manualmente e colado o código abaixo, editando o caminho em **content**
- Com o comando `npx tailwindcss init` (Recomendado)
- Ou gerando o arquivo completo, com `npx tailwindcss init --full`
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Adicionar as diretivas CSS para o arquivo de input
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Build process automático
```shell
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch
```

ou através do script de build único
```shell
tailwindcss build -i src/styles.css -o public/styles.css
```

Flags
- `-i`: Caminho do arquivo de input
- `-o`: Caminho do arquivo de saída(CSS usado importado no HTML)

Usando no HTML
```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="./output.css" rel="stylesheet">
</head>
<body>
  <h1 class="text-3xl font-bold underline">
    Hello world!
  </h1>
</body>
</html>
```

Com isso basta escolher qual o melhor método de build e ir incluindo as classes para as tags desejadas.

## Exemplos

Todo texto do `body` terá a cor indicada
```html
<body class="text-gray-600">
```

O header H1 estará em negrito e em Uppercase
```html
<div><h1 class="font-bold uppercase">
	<a href="#">Foot Ninja</a>
</h1></div>
```

O item da lista reescreverá a cor do `body` para ter a cor indicada e será negrito
```html
<li class="text-gray-700 font-bold"><a href="#">
	<span>Home</span>
</a></li>
```

Os headers H2 reescreve a cor inicial do `body`, terá tamanho **6xl** e semibold. H3 terá tamanho **2xl** e semibold
```html
<header> <!--Headers-->
	<h2 class="text-gray-700 text-6xl font-semibold">Recipes</h2>
	<h3 class="text-2xl font-semibold">For ninjas</h3>
</header> <!--Headers-->
```