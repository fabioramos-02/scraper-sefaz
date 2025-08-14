# Site SEFAZ - Portal Principal

## Visão Geral

Este módulo extrai e analisa o catálogo de serviços do site principal da SEFAZ-MS, disponível em https://www.sefaz.ms.gov.br/.

## Resultados

- **279 serviços** mapeados
- **5 perfis** de usuário
- **21 categorias** identificadas
- **Taxa de sucesso**: 100%

## Perfis Processados

| Perfil | Serviços | Percentual |
|--------|----------|------------|
| **Empresa** | 134 | 48.0% |
| **Cidadão** | 84 | 30.1% |
| **Produtor Rural** | 32 | 11.5% |
| **Poder Público** | 20 | 7.2% |
| **Contabilista** | 9 | 3.2% |

## Arquivos

### Scripts
- **`sefaz_site_scraper.py`** - Scraper principal do site SEFAZ
- **`analise_site_sefaz.py`** - Análise estatística e insights

### Dados
- **`sefaz_site_servicos.csv`** - Dataset completo (279 registros)
- **`cidadao_page.html`** - Página de exemplo para análise

### Relatórios
- **`relatorio_site_sefaz.md`** - Relatório executivo
- **`relatorio_detalhado_site_sefaz.txt`** - Análise técnica detalhada

## Uso

### Execução Completa
```bash
python sefaz_site_scraper.py
```

### Análise Detalhada
```bash
python analise_site_sefaz.py
```

## Estrutura dos Dados

| Campo | Descrição |
|-------|----------|
| **Categorias** | Categoria do serviço |
| **Perfis** | Perfil de usuário |
| **Serviços** | Nome do serviço |
| **URL** | Link completo para o serviço |

## Principais Insights

### Estratégicos
- **Foco empresarial**: 48% dos serviços para empresas
- **Digitalização alta**: 97.8% dos serviços são digitais
- **ICMS predominante**: Palavra mais frequente nos serviços
- **Catálogo centralizado**: 87.8% direcionam para catalogo.sefaz.ms.gov.br

### Técnicos
- **Estrutura HTML**: Baseada em classes `daems-*`
- **Validação de URLs**: Sistema robusto de verificação
- **Extração inteligente**: Categorias e serviços automáticos
- **Rate limiting**: Controle de requisições

## Funcionalidades

- ✅ Extração multi-perfil automática
- ✅ Validação de URLs completa
- ✅ Formatação CSV otimizada
- ✅ Estatísticas em tempo real
- ✅ Relatórios executivos
- ✅ Análise de palavras-chave
- ✅ Classificação de tipos de serviço
- ✅ Insights estratégicos

## Configuração

### URLs Base
```python
base_url = "https://www.sefaz.ms.gov.br"
profiles = {
    'cidadao-post': 'Cidadão',
    'produtor-rural-post': 'Produtor Rural', 
    'empresa-post': 'Empresa',
    'poder-publico-post': 'Poder Público',
    'contabilista-post': 'Contabilista'
}
```

### Estrutura HTML Alvo
```html
<div class="daems-list-column">
    <h3 class="daems-titulos">Categoria</h3>
    <ul class="daems-list mb-4">
        <li class="daems-list-itens">
            <a href="/servico-url">Nome do Serviço</a>
        </li>
    </ul>
</div>
```

## Categorias Principais

1. **Serviços** (52 serviços)
2. **Cadastro** (37 serviços)
3. **Certidões e Declarações Tributárias** (25 serviços)
4. **Emissão de DAEMS** (22 serviços)
5. **Comunicação** (18 serviços)

## Distribuição por Domínio

- **catalogo.sefaz.ms.gov.br**: 87.8%
- **www.sefaz.ms.gov.br**: 10.8%
- **Outros**: 1.4%

## Próximos Passos

- [ ] Monitoramento de atualizações
- [ ] Integração com catálogo principal
- [ ] Dashboard unificado
- [ ] API de consulta

---

**Fonte**: https://www.sefaz.ms.gov.br/  
**Última Atualização**: Agosto 2025  
**Status**: ✅ Produção