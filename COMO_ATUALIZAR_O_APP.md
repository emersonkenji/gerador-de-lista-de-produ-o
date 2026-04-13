# Fluxo de Trabalho: Como Gerar o Instalador (.exe) e Publicar a Atualização no GitHub

Como o software foi convertido para rodar nativamente como um Executável de Windows Standalone, criamos uma nova arquitetura para publicar as atualizações garantindo que o programa se "Auto-Engula e Atualize" na máquina do cliente. Siga estes passos a cada nova modificação:

## ETAPA 1: Gerar o Executável (Instalador)

Sempre que você alterar seu código em Python na sua máquina (`.py`) e testar que está tudo pronto:

1. Dê um clique duplo no arquivo **`build_app.bat`** (Fica dentro dessa pasta raiz).
2. Ele vai abrir uma telinha preta e compilar as centenas de bibliotecas nativas, interfaces e bancos de dados em um `GeradorDeLista.exe` único. (Pode demorar uns 2-3 minutos na primeira vez por conta de download de C++ interno do sistema nativo).
3. Após ele dizer "Compilação Concluída", procure a pasta amarela nova chamada **`dist`**.
4. Dentro dela estará o seu aplicativo oficial! Teste dar 2 cliques nele.

---

## ETAPA 2: Mandar para a Internet (Publicar no Github)

Para que o aplicativo dos seus clientes (que já instalaram o exe velho) achem a atualização e recebam o download, faça isso na ordem:

### 1. Subir os Códigos (Via Terminal)
Abra seu terminal na pasta do app e envie os scripts (`.py` somente) como costumam fazer:
```bash
git add .
git commit -m "Correção de bugs ou nova feature XY"
git push
```

### 2. Criar a "Release" Oficial
1. Vá no navegador e abra seu link do Github: `https://github.com/emersonkenji/gerador-de-lista-de-produ-o`
2. No painel à direita da tela inicial do repositório, você verá uma aba chamada **"Releases"**. Clique lá (ou vá direto para a criação clicando em `Create a new release`).
3. Em **"Choose a tag"**, digite o número da versão nova. (Exemplo: se a anterior era `v1.0.0`, digite **`v1.0.1`**).
4. Clique em **"Create new tag: v1.0.1 on publish"**.
5. No bloco de texto (Descrição/Body), você dita o que mudou (Ex: "Correção de Bugs e Ajuste visual na Tabela X"). **É esse texto que aparecerá na tela do aplicativo pra pessoa dizendo que tem novidade!**

### 3. O SEGREDO ⚠️ (Anexar o `.exe`)
6. Logo embaixo da caixa de descrição de texto, você verá um campo drag-and-drop escrito: **"Attach binaries by dropping them here"**.
7. Vá na sua pasta `dist` (criada pela Etapa 1) e arraste o **`GeradorDeLista.exe`** para dentro dessa caixinha e solte! Espere a barrinha carregar 100%.
8. Clique no botão verde lá embaixo **[Publish Release]**!

## Pronto!
Em até 10 segundos, no momento que você confirmou, qualquer aplicativo `.exe` ativo no mundo inteiro que abrir a aplicação dele e bater automaticamente no limite interno criará uma aba pipocando na tela perguntando se desja baixar a versão `v1.0.1`.

Se eles clicarem em **Sim**, o app faz o download invisível de Anexo do Github, fecha, se deleta, coloca o `GeradorDeLista.exe` novo que você arremessou e abre pra pessoa na tela já na versão `v1.0.1`. 🚀
