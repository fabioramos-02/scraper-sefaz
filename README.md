# Demanda ARI - Mapeamento de Serviços SEFAZ-MS

## Demanda

Mapeamento completo dos serviços oferecidos pela SEFAZ-MS através de seus portais digitais, visando:

- **Catalogação sistemática** de todos os serviços disponíveis
- **Análise por perfil de usuário** (Cidadão, Empresa, Produtor Rural, etc.)
- **Identificação de categorias** e padrões de serviços
- **Geração de insights estratégicos** para melhoria dos portais

## Sobre o Repositório

Este repositório contém a implementação de scrapers automatizados e análises detalhadas dos principais portais da SEFAZ-MS:

### 📁 Estrutura

```
demanda-ari/
├── carta-de-servico/          # Extração da Carta de Serviços
│   ├── sefaz_scraper.py       # Script principal de extração
│   ├── sefaz_servicos.csv     # Dados extraídos (359 serviços)
│   ├── analise_dados.py       # Análise dos dados
│   ├── relatorio_detalhado.txt # Relatório técnico
│   └── relatorio_executivo.md # Relatório executivo
│
├── site-sefaz/                # Extração do Portal Principal
│   ├── sefaz_site_scraper.py  # Script de extração do site
│   ├── sefaz_site_servicos.csv # Dados do portal (279 serviços)
│   ├── analise_site_sefaz.py  # Análise dos dados
│   ├── relatorio_site_sefaz.md # Relatório do portal
│   └── cidadao_page.html      # Página de exemplo
│
├── cruzamento-de-dados/       # Análise Comparativa e Unificação
│   ├── cruzamento_dados.py    # Script de cruzamento
│   ├── base_dados_unificada.csv # Base unificada (638 serviços)
│   ├── servicos_similares.csv # Serviços duplicados (588 pares)
│   ├── mapeamento_categorias.csv # Categorias padronizadas
│   ├── validacao_urls.csv     # Status das URLs
│   └── relatorio_executivo_cruzamento.md # Relatório final
│
└── README.md                  # Este arquivo
```

### 🎯 Resultados Consolidados

#### Extração Individual
- **638 serviços** mapeados no total
- **359 serviços** da Carta de Serviço
- **279 serviços** do Site SEFAZ
- **9 perfis únicos** de usuários identificados
- **~50 categorias** diferentes entre os portais

#### Análise de Cruzamento
- **588 serviços similares** identificados (duplicações potenciais)
- **8 categorias** mapeadas entre portais
- **4 perfis** padronizados
- **98% de URLs válidas** (49/50 testadas)
- **Base unificada** criada com 638 registros

### 🔧 Tecnologias

- **Python 3.x** - Linguagem principal
- **BeautifulSoup4** - Parsing HTML
- **Requests** - Requisições HTTP
- **CSV** - Formato de dados

### 🚀 Instalação

```bash
git clone <repositorio>
cd demanda-ari
pip install requests beautifulsoup4
```

### 🚀 Uso Rápido

### Carta de Serviço
```bash
cd carta-de-servico
python sefaz_scraper.py
python analise_dados.py
```

### Site SEFAZ
```bash
cd site-sefaz
python sefaz_site_scraper.py
python analise_site_sefaz.py
```

### Cruzamento de Dados
```bash
cd cruzamento-de-dados
pip install pandas requests
python cruzamento_dados.py
```

### 📊 Outputs Gerados

- **CSVs estruturados** com todos os serviços
- **Relatórios executivos** em Markdown
- **Análises detalhadas** com insights estratégicos
- **Estatísticas completas** por perfil e categoria

### 🔄 Próximos Passos

#### ✅ Concluído
- ✅ Extração completa dos dois portais
- ✅ Análise comparativa entre portais
- ✅ Identificação de 588 serviços similares
- ✅ Padronização de 8 categorias e 4 perfis
- ✅ Criação de base unificada (638 serviços)
- ✅ Validação de URLs (98% funcionais)

#### 🎯 Implementação Imediata
- [ ] Revisar 588 serviços similares identificados
- [ ] Corrigir 1 URL inválida detectada
- [ ] Padronizar nomenclatura das 8 categorias
- [ ] Eliminar duplicações entre portais

#### 🚀 Melhorias Futuras
- [ ] Dashboard de monitoramento
- [ ] API unificada de consulta
- [ ] Automação de sincronização
- [ ] Sistema de alertas para mudanças

---

**Desenvolvido para**: Análise e Melhoria dos Portais SEFAZ-MS  
**Status**: ✅ Concluído  
**Última Atualização**: Agosto 2025