# Carta de Serviço - Catálogo SEFAZ-MS

## Visão Geral

Este módulo extrai e analisa o catálogo de serviços do portal principal da SEFAZ-MS, disponível em https://www.catalogo.sefaz.ms.gov.br/Geral/.

## Resultados

- **359 serviços** mapeados
- **4 perfis** de usuário
- **100% de cobertura** dos perfis especificados
- **Taxa de sucesso**: 100%

## Perfis Processados

| Perfil | Serviços | Percentual |
|--------|----------|------------|
| **Comércio, Indústria e Serviços** | 161 | 44.8% |
| **Agropecuária** | 99 | 27.6% |
| **Cidadão / Órgão Governamental** | 78 | 21.7% |
| **Fiscalização** | 21 | 5.8% |

## Arquivos

### Scripts
- **`sefaz_scraper.py`** - Scraper principal com suporte a múltiplos perfis
- **`analise_detalhada.py`** - Análise estatística avançada

### Dados
- **`sefaz_servicos.csv`** - Dataset completo (359 registros)

### Relatórios
- **`relatorio/relatorio_final_gestora.md`** - Relatório executivo
- **`relatorio/estatisticas_detalhadas.txt`** - Métricas detalhadas
- **`relatorio/relatorio_executivo_sefaz.md`** - Análise técnica

## Uso

### Execução Completa
```bash
python sefaz_scraper.py
```

### Análise Detalhada
```bash
python analise_detalhada.py
```

## Estrutura dos Dados

| Campo | Descrição |
|-------|----------|
| **Categorias** | Categorias do serviço (separadas por `;`) |
| **Perfis** | Perfil de usuário |
| **Serviços** | Nome do serviço |
| **URL** | Link completo para o serviço |

## Principais Insights

### Estratégicos
- **Foco empresarial**: 44.8% dos serviços para Comércio/Indústria
- **ICMS predominante**: Serviço mais demandado
- **Cobertura rural**: 27.6% para Agropecuária (alinhado com MS)

### Técnicos
- **Paginação automática**: Processa todas as páginas
- **Detecção de perfil**: Extração inteligente da URL
- **Prevenção de loops**: Sistema anti-duplicação
- **Rate limiting**: 1s entre requisições

## Funcionalidades

- ✅ Extração multi-perfil automática
- ✅ Suporte completo à paginação
- ✅ Validação de URLs
- ✅ Formatação CSV otimizada
- ✅ Estatísticas em tempo real
- ✅ Relatórios executivos
- ✅ Análise de palavras-chave
- ✅ Categorização automática

## Configuração

### URLs Base
```python
base_url = "https://www.catalogo.sefaz.ms.gov.br/Geral/"
profiles = [
    'agropecuaria',
    'ccis-industria-e-servicos', 
    'cidadao-orgao-governamental',
    'autuacoesnotificacoes-fiscalizacao-fiscalizacao'
]
```

### Estrutura HTML Alvo
```html
<div class="card-body">
    <a href="/servico-url">
        <h5 class="card-title">Nome do Serviço</h5>
    </a>
    <div class="categorias mt-2">
        <a rel="category tag">Categoria</a>
    </div>
</div>
```

## Próximos Passos

- [ ] Monitoramento de mudanças
- [ ] Integração com API
- [ ] Dashboard interativo
- [ ] Alertas automáticos

---

**Fonte**: https://www.catalogo.sefaz.ms.gov.br/Geral/  
**Última Atualização**: Agosto 2025  
**Status**: ✅ Produção