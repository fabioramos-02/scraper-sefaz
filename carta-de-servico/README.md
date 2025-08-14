# Scraper SEFAZ-MS

Este projeto contém um scraper para extrair informações de serviços do catálogo da Secretaria de Estado de Fazenda de Mato Grosso do Sul (SEFAZ-MS).

## 🎯 Funcionalidades

- **Extração de dados estruturados**: Coleta categorias, perfis, serviços e URLs
- **Detecção automática de perfil**: Extrai o perfil da URL (ex: Agropecuária, Comércio)
- **Suporte à paginação**: Processa automaticamente todas as páginas disponíveis
- **Construção completa de URLs**: Converte links relativos em URLs absolutas
- **Formatação CSV otimizada**: Remove vírgulas das categorias para evitar quebras no CSV
- **Rate limiting**: Pausa de 1 segundo entre requisições para respeitar o servidor
- **Logging detalhado**: Acompanhamento completo do processo de scraping
- **Tratamento de erros**: Gerenciamento robusto de falhas de conexão e parsing

## Estrutura do Projeto

```
├── sefaz_scraper.py    # Script principal do scraper
├── requirements.txt    # Dependências do projeto
├── README.md          # Este arquivo
└── sefaz_servicos.csv # Arquivo de saída (gerado após execução)
```

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Execução Básica

Para executar o scraper com a URL padrão:

```bash
python sefaz_scraper.py
```

### Adicionando Novas URLs

Para fazer scraping de múltiplas páginas, edite a lista `urls_to_scrape` na função `main()` do arquivo `sefaz_scraper.py`:

```python
urls_to_scrape = [
    "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/autorizacoes-cap/",
    "https://www.catalogo.sefaz.ms.gov.br/Geral/ccis-industria-e-servicos/autorizacoes-ccis/",
    # Adicione mais URLs aqui
]
```

## 📊 Estrutura do CSV

O arquivo CSV gerado contém as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|----------|
| **Categorias** | Categorias extraídas da div categorias, separadas por `;` | "Agropecuária;Autorizações - CAP;Comércio Indústria e Serviços" |
| **Perfis** | Perfil extraído da URL ou h1 | "Agropecuária" |
| **Serviços** | Nome do serviço | "Autorização específica – ICMS" |
| **URL** | URL completa do serviço | "https://www.catalogo.sefaz.ms.gov.br/..." |

### Exemplo de dados:
```csv
Categorias,Perfis,Serviços,URL
"Agropecuária;Autorizações - CAP",Agropecuária,"Autorização específica – diferimento do ICMS",https://www.catalogo.sefaz.ms.gov.br/...
```

### Estrutura HTML Esperada

O scraper foi desenvolvido para trabalhar com a seguinte estrutura HTML:

```html
<!-- Categoria principal (usado como fallback para perfil) -->
<h1 class="green">Nome da Categoria</h1>

<!-- Serviços -->
<div class="card-body">
    <a href="/link-do-servico">
        <h5 class="card-title">Nome do Serviço</h5>
    </a>
    
    <!-- Categorias (extraídas para coluna Categorias) -->
    <div class="categorias mt-2">
        <a rel="category tag" href="#">Categoria 1</a>
        <a rel="category tag" href="#">Categoria 2</a>
    </div>
</div>

<!-- Paginação (processada automaticamente) -->
<div class="paginacao">
    <ul class="list-unstyled list-inline">
        <li><a href="/pagina-2">2</a></li>
        <li><a href="/pagina-3">3</a></li>
    </ul>
</div>
```

## 🔧 Características Técnicas

- **Detecção de perfil inteligente**: Extrai perfil da URL automaticamente
- **Paginação automática**: Detecta e processa todas as páginas disponíveis
- **Prevenção de loops**: Sistema de controle de URLs visitadas
- **Formatação CSV segura**: Remove vírgulas das categorias para evitar quebras
- **Rate Limiting**: 1 segundo de pausa entre requisições
- **User-Agent**: Simula navegador real para evitar bloqueios
- **Encoding**: Suporte completo a UTF-8 para caracteres especiais
- **Error Handling**: Continua o scraping mesmo com falhas pontuais
- **Logging**: Registra todas as operações para debugging

## Logs

O scraper gera logs informativos durante a execução:
- Início do scraping de cada página
- Categoria principal encontrada
- Número de serviços encontrados
- Total de registros salvos

## Manutenção

### Adicionando Novos Seletores

Se a estrutura HTML mudar, você pode modificar os seletores nos seguintes métodos:

- `extract_category_from_h1()`: Para mudanças no h1 da categoria
- `extract_service_data()`: Para mudanças na estrutura dos cards
- `extract_profiles_from_categories()`: Para mudanças na div de categorias

### Tratamento de Erros

O scraper inclui tratamento para:
- Falhas de conexão HTTP
- Elementos HTML não encontrados
- Timeouts de requisição

## Dependências

- `requests`: Para fazer requisições HTTP
- `beautifulsoup4`: Para parsing HTML
- `csv`: Para geração do arquivo CSV (biblioteca padrão)
- `logging`: Para sistema de logs (biblioteca padrão)

## Limitações

- O scraper funciona apenas com a estrutura HTML atual do site da SEFAZ-MS
- Não há suporte para JavaScript/conteúdo dinâmico
- Limitado a páginas que seguem o padrão de cards identificado

## Contribuição

Para contribuir com melhorias:
1. Identifique a mudança necessária
2. Teste com diferentes URLs do catálogo SEFAZ-MS
3. Verifique se os logs estão informativos
4. Confirme que o CSV de saída mantém a estrutura esperada