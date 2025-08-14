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
├── carta-de-servico/     # Catálogo principal (359 serviços)
├── site-sefaz/          # Site principal (279 serviços)
└── README.md            # Este arquivo
```

### 🎯 Resultados Consolidados

- **638 serviços** mapeados no total
- **9 perfis únicos** de usuário
- **~50 categorias** identificadas
- **100% de cobertura** dos portais especificados

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

### ⚡ Uso Rápido

```bash
# Catálogo principal
cd carta-de-servico
python sefaz_scraper.py

# Site principal
cd site-sefaz
python sefaz_site_scraper.py
```

### 📊 Outputs Gerados

- **CSVs estruturados** com todos os serviços
- **Relatórios executivos** em Markdown
- **Análises detalhadas** com insights estratégicos
- **Estatísticas completas** por perfil e categoria

### 🔄 Próximos Passos

- [ ] Unificação dos datasets
- [ ] Dashboard interativo
- [ ] API de consulta
- [ ] Monitoramento automático

---

**Desenvolvido para**: Análise e Melhoria dos Portais SEFAZ-MS  
**Status**: ✅ Concluído  
**Última Atualização**: Agosto 2025