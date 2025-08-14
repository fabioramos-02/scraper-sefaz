# Cruzamento de Dados - SEFAZ-MS

## Visão Geral

Este módulo realiza análise comparativa entre os datasets da **Carta de Serviço** e **Site SEFAZ**, identificando duplicações, padronizando categorias e validando URLs para otimização dos portais.

## Resultados da Análise

- **638 serviços** analisados (359 + 279)
- **588 serviços similares** identificados
- **8 categorias** mapeadas entre portais
- **98% de URLs válidas** (49/50 testadas)
- **4 perfis** padronizados

## Arquivos Gerados

### Script Principal
- **`cruzamento_dados.py`** - Análise completa de cruzamento

### Base de Dados
- **`base_dados_unificada.csv`** - Dataset consolidado (638 registros)

### Análises Detalhadas
- **`servicos_similares.csv`** - 588 pares de serviços similares
- **`mapeamento_categorias.csv`** - 8 mapeamentos de categorias
- **`validacao_urls.csv`** - Status de 50 URLs testadas

### Relatório Executivo
- **`relatorio_executivo_cruzamento.md`** - Relatório para chefia

## Principais Descobertas

### 🔍 Serviços Similares
- **588 duplicações** potenciais identificadas
- Threshold de similaridade: **70%**
- Exemplos de alta similaridade:
  - "Guia de Trânsito Suspensa" (100% match)
  - "Regime Especial PROEXPRP" (97.9% match)
  - "Nota Fiscal Eletrônica" (99.2% match)

### 📂 Padronização de Categorias

| Carta de Serviço | Site SEFAZ | Similaridade |
|------------------|------------|-------------|
| **IPVA** | IPVA | 100% |
| **Consulta Tributária - Geral** | Consulta Tributária | 82.6% |
| **Cadastro Fiscal** | Cadastros | 75% |
| **Documentos Fiscais - Geral** | Documentos Fiscais Eletrônicos | 75% |

### 👥 Mapeamento de Perfis

| Carta de Serviço | Site SEFAZ | Unificado |
|------------------|------------|----------|
| **Cidadão / Órgão Governamental** | Cidadão | Cidadão |
| **Comércio, Indústria e Serviços** | Empresa | Empresa |
| **Agropecuária** | Produtor Rural | Produtor Rural |
| **Fiscalização** | Poder Público | Poder Público |

### 🔗 Qualidade das URLs
- **98% de funcionalidade** (49/50 URLs válidas)
- **1 URL com problema** identificada
- Maioria direciona para `catalogo.sefaz.ms.gov.br`

## Uso

### Execução Completa
```bash
cd cruzamento-de-dados
python cruzamento_dados.py
```

### Dependências
```bash
pip install pandas requests
```

## Funcionalidades

### 🔄 Análise de Similaridade
- **Algoritmo**: SequenceMatcher (difflib)
- **Threshold configurável**: 70% (padrão)
- **Comparação textual** de nomes de serviços
- **Identificação automática** de duplicações

### 📊 Padronização
- **Mapeamento inteligente** de categorias similares
- **Unificação de perfis** entre portais
- **Criação de taxonomia** padronizada

### ✅ Validação de URLs
- **Teste HTTP** de funcionalidade
- **Detecção de 404** e outros erros
- **Rate limiting** para não sobrecarregar servidores
- **Amostragem configurável**

### 📋 Relatórios
- **Relatório executivo** para gestão
- **Análises detalhadas** para equipe técnica
- **Métricas consolidadas** e insights estratégicos

## Insights Estratégicos

### 🎯 Oportunidades Identificadas

1. **Eliminação de Duplicações**
   - 588 serviços similares para revisão
   - Potencial redução de ~50% do catálogo
   - Melhoria na experiência do usuário

2. **Padronização de Categorias**
   - 8 categorias com nomenclaturas diferentes
   - Oportunidade de taxonomia unificada
   - Facilita navegação e busca

3. **Manutenção Preventiva**
   - 98% de URLs funcionais
   - 1 URL para correção imediata
   - Sistema robusto e confiável

### 📈 Benefícios Esperados

- **Redução de custos** de manutenção
- **Melhoria na experiência** do usuário
- **Maior eficiência** operacional
- **Padronização** de processos
- **Facilidade de gestão** do catálogo

## Configuração

### Parâmetros Ajustáveis
```python
# Threshold de similaridade (0.0 a 1.0)
threshold_similaridade = 0.7

# Tamanho da amostra para validação de URLs
tamanho_amostra_urls = 50

# Delay entre requisições (segundos)
rate_limit = 0.5
```

### Caminhos dos Arquivos
```python
carta_servico_path = '../carta-de-servico/sefaz_servicos.csv'
site_sefaz_path = '../site-sefaz/sefaz_site_servicos.csv'
output_path = 'base_dados_unificada.csv'
```

## Próximos Passos

### Implementação Imediata
- [ ] Revisar 588 serviços similares identificados
- [ ] Corrigir 1 URL inválida
- [ ] Padronizar 8 categorias mapeadas

### Melhorias Futuras
- [ ] Dashboard interativo de monitoramento
- [ ] Automação de sincronização entre portais
- [ ] API unificada de consulta
- [ ] Sistema de alertas para mudanças

---

**Objetivo**: Unificação e otimização dos portais SEFAZ-MS  
**Status**: ✅ Análise Concluída  
**Última Execução**: 14/08/2025 11:28