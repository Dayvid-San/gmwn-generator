Uma tag link de exemplo, usada para carregar um arquivo css do pacote **Prism.js** marcação de sintaxe de blocos de código.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/themes/prism-twilight.min.css" integrity="sha512-6rkEt5SymQMcnlRz1dHwAMSfMnDaFX28qdr3wyaa+XRCR8dTSWE4U6vjiTVuB6Mq9FgYOLVOTk0lrOeCnodcgA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
```

### 1. `integrity`

O atributo `integrity` é usado para fornecer um hash criptográfico que o navegador usa para verificar se o arquivo solicitado foi alterado. Este atributo é parte da [Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) e ajuda a garantir que o arquivo não foi modificado por terceiros.

- **Valor do atributo**: `sha512-6rkEt5SymQMcnlRz1dHwAMSfMnDaFX28qdr3wyaa+XRCR8dTSWE4U6vjiTVuB6Mq9FgYOLVOTk0lrOeCnodcgA==`
- **Significado**: O navegador calcula o hash do arquivo baixado e compara com o valor fornecido. Se os hashes não coincidirem, o arquivo não será carregado.

### 2. `crossorigin`

O atributo `crossorigin` é utilizado para controlar como o navegador deve lidar com as solicitações de recursos de diferentes origens (cross-origin). Este atributo pode ter valores diferentes:

- **`anonymous`**: Envia a solicitação sem credenciais (cookies, certificados HTTP, etc.).
- **`use-credentials`**: Envia a solicitação com credenciais (cookies, certificados HTTP, etc.).

No exemplo:

- **Valor do atributo**: `anonymous`
- **Significado**: A solicitação do recurso será feita sem enviar credenciais, garantindo a privacidade e segurança da solicitação.

### 3. `referrerpolicy`

O atributo `referrerpolicy` controla como a informação de referenciador (referrer) deve ser enviada ao fazer a solicitação do recurso. Este atributo pode ter vários valores que determinam como o cabeçalho `Referer` será gerado.

- **`no-referrer`**: O navegador não envia a informação do referenciador.
- **`no-referrer-when-downgrade`**: O navegador não envia a informação do referenciador para solicitações HTTP, mas envia para HTTPS.
- **`origin`**: O navegador envia apenas a origem do documento (por exemplo, `https://example.com`).
- **`origin-when-cross-origin`**: O navegador envia a origem do documento para solicitações cross-origin, mas envia o referenciador completo para solicitações same-origin.
- **`same-origin`**: O navegador envia o referenciador completo apenas para solicitações same-origin.
- **`strict-origin`**: O navegador envia a origem do documento para todas as solicitações, mas envia o referenciador completo apenas para solicitações same-origin.
- **`strict-origin-when-cross-origin`**: O navegador envia a origem do documento para todas as solicitações cross-origin, mas envia o referenciador completo para solicitações same-origin.
- **`unsafe-url`**: O navegador envia o referenciador completo, incluindo a URL completa do documento de referência.

No exemplo:

- **Valor do atributo**: `no-referrer`
- **Significado**: O navegador não envia informações de referenciador ao fazer a solicitação para o recurso, melhorando a privacidade do usuário.

### Resumo

- **`integrity`**: Garante que o arquivo solicitado não foi alterado (verifica a integridade do arquivo).
- **`crossorigin`**: Controla se as credenciais (cookies, certificados) são enviadas com a solicitação.
- **`referrerpolicy`**: Controla quais informações de referenciador são enviadas com a solicitação, ajudando a proteger a privacidade do usuário.

Esses atributos são usados principalmente para melhorar a segurança e a privacidade ao carregar recursos externos, especialmente em sites que dependem de bibliotecas e arquivos de terceiros.