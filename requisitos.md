Crie um aplicativo desktop instalável para Windows chamado Gerador de Lista de Produção.

Objetivo do app

O aplicativo deve importar um arquivo .xlsx exportado do Upseller, interpretar os produtos e suas variações, e gerar automaticamente uma lista de produção organizada por tipo e litragem, além de salvar tudo em banco de dados local para consulta posterior.

O app deve ser pensado para uso real em operação diária, com interface bonita, moderna, profissional e intuitiva.

Stack e arquitetura

Quero que o projeto seja construído em Python, com arquitetura profissional e organizada.

Requisitos técnicos principais
Linguagem principal: Python
Aplicativo desktop instalável no PC
Interface moderna com aparência inspirada em shadcn/ui + TailwindCSS
Tema claro e escuro
Banco de dados local incluso
Integração com Supabase
Persistência local obrigatória mesmo sem internet
Estrutura pronta para crescimento e manutenção
Sugestão de stack

Use uma stack desktop moderna em Python, priorizando boa aparência e experiência de uso:

PySide6 para interface desktop
QSS / tema customizado para reproduzir visual moderno estilo shadcn
SQLite como banco local principal
SQLAlchemy para ORM
Supabase para sincronização remota opcional
Pandas + openpyxl para leitura de arquivos .xlsx
Pydantic para validação de dados
PyInstaller para gerar executável instalável

Se houver opção melhor mantendo tudo em Python, pode usar, mas o resultado precisa ser moderno, rápido e pronto para produção.

Identidade visual e UX

A interface deve ser extremamente bem feita.

Visual
Layout moderno, limpo e profissional
Inspirado em shadcn/ui
Cartões com cantos arredondados
Sombras suaves
Tipografia elegante
Espaçamentos bem definidos
Ícones modernos
Cores neutras com destaque elegante
Modo claro e modo escuro com alternância no app
Estrutura visual

Criar navegação lateral ou superior com as seguintes áreas:

Dashboard
Importar XLSX
Produtos cadastrados
Listas geradas
Configurações
Sincronização Supabase
Funcionalidade principal

O app deve gerar uma lista de produção a partir de um .xlsx do Upseller.

Exemplo do formato final da lista

A lista gerada deve seguir algo como:

🎨 LISTA DE PRODUÇÃO - E.F.S.T COMERCIAL LTDA
📅 Data: 20/03/2026
============================================================

INTERNA:
Tinta interna 3,6L:
branco - 2
palha - 1
Tinta interna 10L:
branco - 2
palha - 1
Tinta interna 18L:
areia - 2
branco neve - 3

PISO:
Tinta piso 3,6L:
branco - 2
palha - 1
Tinta piso 10L:
branco - 2
palha - 1
Tinta piso 18L:
areia - 2
branco neve - 3

EXTERNA:
etc.

EMBORRACHADA:
etc.

📊 RESUMO GERAL:
Total de baldes produzidos: 18
Regras de negócio

O sistema deve entender que os dados virão do arquivo .xlsx do Upseller.

Origem das informações

Os dados normalmente vêm do:

título do produto
variações do produto
nome do arquivo .xlsx
Exemplo de nomes de produtos

Os títulos podem vir assim:

Tinta acrílica interna 10 litros ColorsPro - Sem cheiro e com Antimofo Varias cores - Alta cobertura
Tinta acrílica parede 10 litros ColorsPro - Sem cheiro e com Antimofo Varias cores - Alta cobertura
Tinta acrílica piso 10 litros ColorsPro - Sem cheiro e com Antimofo Varias cores - Alta cobertura
títulos contendo emborrachada
produtos com nomes diferentes, mas que pertencem à mesma categoria de produção
Objetivo do cadastro de produtos

Preciso de uma tela onde eu possa cadastrar manualmente um mapeamento do produto.

Cada produto cadastrado deve ter:

campo 1: título ou padrão do título
campo 2: litragem
campo 3: tipo
Exemplos de tipo
Interna
Piso
Externa
Emborrachada
Econômica
Premium
Outros

O cadastro deve permitir que eu normalize nomes diferentes que representam o mesmo produto.

Exemplo:

“Tinta acrílica parede 10 litros...” pode ser tratada como Interna 10L
“Tinta acrílica interna 10 litros...” também pode ser tratada como Interna 10L
Tratamento de variações

As variações podem vir separadas por vírgula.

Exemplos
branco,3,6l
palha,10l
cinza chumbo,18l

Mas também pode haver produtos com mais de uma variação além da cor.

Regra

O sistema deve:

identificar a cor
identificar a litragem
usar o cadastro de produtos para identificar o tipo
permitir tratamento flexível para variações diferentes
ignorar diferenças pequenas de caixa alta/baixa, espaços e acentos
Regras de leitura

Criar lógica robusta para:

interpretar 3,6l, 3.6l, 3,6 L, 3.6 litros
interpretar 10l, 10 L, 10 litros
interpretar 18l, 18 L, 18 litros
reconhecer palavras como:
interna
parede
piso
externa
emborrachada
econômica

Se a litragem vier na variação, usar a da variação.
Se não vier na variação, tentar pegar do título do produto.
Se não conseguir identificar automaticamente, marcar o item como pendente de classificação para o usuário corrigir.

Data da lista pelo nome do arquivo

O nome do arquivo .xlsx geralmente vem assim:

Export_Order20260409214937.xlsx

O sistema deve extrair automaticamente a data do nome do arquivo.

Regra

Do exemplo acima:

data extraída: 09/04/2026

Ignorar a parte da hora na exibição principal, mas armazenar no banco se possível.

Criar função específica para:

localizar o trecho numérico da data
interpretar formato YYYYMMDDHHMMSS
exibir no formato brasileiro DD/MM/YYYY
Fluxo do usuário
Fluxo principal ideal
Usuário abre o app
Importa um arquivo .xlsx
Sistema lê o arquivo
Sistema extrai a data pelo nome do arquivo
Sistema identifica os produtos e variações
Sistema usa o cadastro de mapeamento para classificar:
tipo
litragem
cor
Sistema gera a lista de produção
Sistema mostra pré-visualização
Usuário pode editar manualmente antes de salvar
Usuário salva a lista no banco
Usuário pode reabrir listas antigas depois
Telas obrigatórias

1. Dashboard

Deve exibir:

total de listas geradas
total de produtos cadastrados
última importação
total de itens pendentes de classificação
atalhos para importar novo arquivo e ver listas antigas 2. Importar XLSX

Deve permitir:

selecionar arquivo
mostrar nome do arquivo
extrair data automaticamente
visualizar linhas importadas
identificar erros
botão para processar 3. Produtos cadastrados

Tela para cadastro e edição do mapeamento de produtos.

Cada cadastro deve ter:

título/padrão do produto
palavras-chave opcionais
tipo
litragem padrão
observações
status ativo/inativo

Permitir:

criar
editar
excluir
pesquisar
filtrar por tipo 4. Prévia da lista gerada

Mostrar a lista final já organizada:

por tipo
depois por litragem
depois por cor
com total por seção
com total geral

Permitir edição manual antes de salvar.

5. Histórico de listas

Mostrar todas as listas já geradas e salvas.
Permitir:

abrir
duplicar
editar
exportar
excluir
buscar por data 6. Configurações

Permitir:

trocar entre modo claro e escuro
configurar nome da empresa exibida no topo da lista
definir preferências de exportação
configurar Supabase 7. Sincronização Supabase

Criar uma tela para:

informar URL do projeto
informar chave
testar conexão
ativar ou desativar sincronização
enviar listas e produtos cadastrados para nuvem
Banco de dados

Criar banco local em SQLite com estrutura bem feita.

Tabelas sugeridas
tabela: products_mapping

Campos:

id
title_pattern
keywords
product_type
default_volume
notes
is_active
created_at
updated_at
tabela: production_lists

Campos:

id
company_name
list_date
source_file_name
source_file_datetime
raw_text_output
total_buckets
created_at
updated_at
synced_at
sync_status
tabela: production_list_items

Campos:

id
production_list_id
product_type
volume
color
quantity
original_title
original_variation
classification_status
created_at
updated_at
tabela: app_settings

Campos:

id
company_name
theme
supabase_url
supabase_key
enable_sync
created_at
updated_at
Regras da geração da lista

A lista precisa ser agrupada nesta ordem:

Ordem dos tipos
Interna
Piso
Externa
Emborrachada
Econômica
Outros
Ordem das litragens
3,6L
10L
18L
outras
Dentro de cada grupo

Ordenar por cor em ordem alfabética.

Saída textual

Gerar o bloco final em texto formatado exatamente pronto para copiar.

Também gerar versão visual na interface com boa leitura.

Recursos extras importantes

Implementar também:

Edição manual

Se algum item não for reconhecido corretamente, permitir correção manual antes de salvar.

Itens pendentes

Criar área de “itens não classificados” para o usuário decidir:

tipo
litragem
cor
Exportação

Permitir exportar lista gerada em:

.txt
.pdf
.xlsx
Histórico

Poder abrir listas antigas já geradas.

Reprocessamento

Permitir pegar uma lista antiga e reprocessar com regras novas de mapeamento.

Busca inteligente

Permitir buscar produtos cadastrados por:

nome
palavra-chave
tipo
litragem
Lógica de classificação

Implementar um motor de classificação com estas prioridades:

Prioridade de identificação
tentar identificar pelo cadastro de produtos
tentar identificar pelo título do produto
tentar identificar pela variação
se falhar, marcar como pendente
Normalização

Antes de comparar:

remover acentos
converter para minúsculas
remover espaços duplicados
tolerar pequenas diferenças de escrita
Reconhecimento semântico

O sistema deve entender equivalências, por exemplo:

parede pode ser classificado como interna quando definido pelo cadastro
emborrachara, emborracghara, emborrachada devem ser tratados com tolerância básica a erro de digitação quando possível
3,6l, 3.6l, 3,6 litros, 3.6 litros devem virar 3,6L
Qualidade do código

Quero código com padrão profissional.

Exigências
arquitetura modular
separação entre interface, regras de negócio e persistência
código limpo
tipagem
validação de dados
tratamento de erros
logs
comentários apenas onde necessário
pronto para manutenção
estrutura de pastas organizada
Estrutura desejada do projeto

Organize o projeto em algo como:

app/
app/ui/
app/core/
app/services/
app/models/
app/repositories/
app/database/
app/utils/
app/themes/
app/config/
tests/
Entregáveis esperados

Quero que você gere:

Estrutura completa do projeto
Código do app funcional
Interface moderna
Banco local SQLite funcionando
Integração configurável com Supabase
Tela de importação de .xlsx
Tela de cadastro de produtos
Tela de histórico de listas
Geração automática da lista
Exportação da lista
Modo claro e escuro
Script de build para executável
README com instruções de instalação e uso
Comportamento esperado da IA

Não crie apenas um protótipo visual.
Crie um projeto real, funcional e bem estruturado, com foco em uso prático.

Quando houver ambiguidade no .xlsx, implemente lógica segura e permita correção manual.

Priorize:

usabilidade
performance
interface bonita
código escalável
facilidade de manutenção
Exemplo de parsing esperado
Entrada

Título:
Tinta acrílica interna 10 litros ColorsPro - Sem cheiro e com Antimofo Varias cores - Alta cobertura

Variação:
branco,10l

Quantidade:
2

Saída esperada

Tipo:
Interna

Litragem:
10L

Cor:
Branco

Quantidade:
2

Exemplo de outra entrada

Título:
Tinta acrílica piso 18 litros ColorsPro - Sem cheiro e com Antimofo Varias cores - Alta cobertura

Variação:
areia,18l

Quantidade:
3

Saída esperada

Tipo:
Piso

Litragem:
18L

Cor:
Areia

Quantidade:
3

Exemplo de extração da data do arquivo

Nome:
Export_Order20260409214937.xlsx

Resultado esperado
Data da lista: 09/04/2026
Data/hora armazenada internamente: 2026-04-09 21:49:37
Quero também

Além do código, explique no final:

como rodar localmente
como gerar o executável
como configurar o Supabase
onde trocar nome da empresa
como cadastrar novos padrões de produto
como importar novos .xlsx

Se achar necessário, você pode melhorar a arquitetura, mas sem fugir desses requisitos.
