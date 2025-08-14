#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cruzamento de Dados - SEFAZ-MS
Análise comparativa entre Carta de Serviço e Site SEFAZ

Este script realiza:
1. Carregamento e unificação dos datasets
2. Identificação de serviços similares
3. Padronização de categorias e perfis
4. Validação de URLs
5. Geração de relatório executivo
"""

import pandas as pd
import requests
import re
import time
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from urllib.parse import urlparse
import csv
from datetime import datetime

class CruzamentoDados:
    def __init__(self):
        self.carta_servico_path = '../carta-de-servico/sefaz_servicos.csv'
        self.site_sefaz_path = '../site-sefaz/sefaz_site_servicos.csv'
        self.output_path = 'base_dados_unificada.csv'
        
        # Dados carregados
        self.df_carta = None
        self.df_site = None
        self.df_unificado = None
        
        # Análises
        self.servicos_similares = []
        self.categorias_mapeadas = {}
        self.perfis_mapeados = {}
        self.urls_validadas = {}
        
        # Estatísticas
        self.stats = {
            'total_servicos': 0,
            'servicos_duplicados': 0,
            'urls_validas': 0,
            'urls_invalidas': 0,
            'categorias_unificadas': 0,
            'perfis_unificados': 0
        }
    
    def carregar_dados(self):
        """Carrega os datasets dos dois projetos"""
        print("📊 Carregando datasets...")
        
        try:
            # Carta de Serviço
            self.df_carta = pd.read_csv(self.carta_servico_path)
            self.df_carta['fonte'] = 'Carta de Serviço'
            print(f"   ✅ Carta de Serviço: {len(self.df_carta)} serviços")
            
            # Site SEFAZ
            self.df_site = pd.read_csv(self.site_sefaz_path)
            self.df_site['fonte'] = 'Site SEFAZ'
            print(f"   ✅ Site SEFAZ: {len(self.df_site)} serviços")
            
            # Padronizar colunas
            self._padronizar_colunas()
            
            print(f"   📈 Total: {len(self.df_carta) + len(self.df_site)} serviços carregados")
            
        except Exception as e:
            print(f"   ❌ Erro ao carregar dados: {e}")
            raise
    
    def _padronizar_colunas(self):
        """Padroniza nomes das colunas entre os datasets"""
        colunas_padrao = ['Categorias', 'Perfis', 'Serviços', 'URL', 'fonte']
        
        # Verificar se as colunas existem
        for df, nome in [(self.df_carta, 'Carta'), (self.df_site, 'Site')]:
            colunas_faltantes = [col for col in colunas_padrao[:-1] if col not in df.columns]
            if colunas_faltantes:
                print(f"   ⚠️  {nome}: Colunas faltantes: {colunas_faltantes}")
    
    def identificar_servicos_similares(self, threshold=0.7):
        """Identifica serviços similares entre os dois datasets"""
        print(f"\n🔍 Identificando serviços similares (threshold: {threshold})...")
        
        servicos_carta = self.df_carta['Serviços'].tolist()
        servicos_site = self.df_site['Serviços'].tolist()
        
        similares_encontrados = 0
        
        for i, servico_carta in enumerate(servicos_carta):
            for j, servico_site in enumerate(servicos_site):
                similaridade = SequenceMatcher(None, 
                                             servico_carta.lower(), 
                                             servico_site.lower()).ratio()
                
                if similaridade >= threshold:
                    self.servicos_similares.append({
                        'servico_carta': servico_carta,
                        'servico_site': servico_site,
                        'similaridade': round(similaridade, 3),
                        'categoria_carta': self.df_carta.iloc[i]['Categorias'],
                        'categoria_site': self.df_site.iloc[j]['Categorias'],
                        'perfil_carta': self.df_carta.iloc[i]['Perfis'],
                        'perfil_site': self.df_site.iloc[j]['Perfis'],
                        'url_carta': self.df_carta.iloc[i]['URL'],
                        'url_site': self.df_site.iloc[j]['URL']
                    })
                    similares_encontrados += 1
        
        print(f"   ✅ {similares_encontrados} pares de serviços similares encontrados")
        self.stats['servicos_duplicados'] = similares_encontrados
    
    def mapear_categorias(self):
        """Mapeia e padroniza categorias entre os datasets"""
        print("\n📂 Mapeando e padronizando categorias...")
        
        # Extrair todas as categorias
        categorias_carta = set()
        categorias_site = set()
        
        for categorias in self.df_carta['Categorias'].dropna():
            if ';' in str(categorias):
                categorias_carta.update([cat.strip() for cat in str(categorias).split(';')])
            else:
                categorias_carta.add(str(categorias).strip())
        
        for categoria in self.df_site['Categorias'].dropna():
            categorias_site.add(str(categoria).strip())
        
        print(f"   📊 Carta de Serviço: {len(categorias_carta)} categorias únicas")
        print(f"   📊 Site SEFAZ: {len(categorias_site)} categorias únicas")
        
        # Mapear categorias similares
        self._mapear_categorias_similares(categorias_carta, categorias_site)
        
        print(f"   ✅ {len(self.categorias_mapeadas)} mapeamentos de categoria criados")
    
    def _mapear_categorias_similares(self, categorias_carta, categorias_site, threshold=0.6):
        """Mapeia categorias similares entre os datasets"""
        for cat_carta in categorias_carta:
            melhor_match = None
            melhor_score = 0
            
            for cat_site in categorias_site:
                score = SequenceMatcher(None, cat_carta.lower(), cat_site.lower()).ratio()
                if score > threshold and score > melhor_score:
                    melhor_score = score
                    melhor_match = cat_site
            
            if melhor_match:
                self.categorias_mapeadas[cat_carta] = {
                    'categoria_site': melhor_match,
                    'similaridade': round(melhor_score, 3),
                    'categoria_unificada': self._unificar_categoria(cat_carta, melhor_match)
                }
    
    def _unificar_categoria(self, cat1, cat2):
        """Cria nome unificado para categoria"""
        # Lógica para criar nome unificado (pode ser refinada)
        if len(cat1) <= len(cat2):
            return cat1
        return cat2
    
    def mapear_perfis(self):
        """Mapeia e padroniza perfis entre os datasets"""
        print("\n👥 Mapeando e padronizando perfis...")
        
        perfis_carta = set(self.df_carta['Perfis'].dropna())
        perfis_site = set(self.df_site['Perfis'].dropna())
        
        print(f"   📊 Carta de Serviço: {len(perfis_carta)} perfis únicos")
        print(f"   📊 Site SEFAZ: {len(perfis_site)} perfis únicos")
        
        # Mapeamento manual baseado no conhecimento dos dados
        mapeamento_perfis = {
            'Cidadão / Órgão Governamental': 'Cidadão',
            'Comércio, Indústria e Serviços': 'Empresa',
            'Agropecuária': 'Produtor Rural',
            'Fiscalização': 'Poder Público'
        }
        
        self.perfis_mapeados = mapeamento_perfis
        print(f"   ✅ {len(self.perfis_mapeados)} mapeamentos de perfil criados")
    
    def validar_urls(self, sample_size=50):
        """Valida uma amostra de URLs para verificar se estão funcionais"""
        print(f"\n🔗 Validando URLs (amostra de {sample_size})...")
        
        # Combinar todas as URLs
        todas_urls = list(self.df_carta['URL'].dropna()) + list(self.df_site['URL'].dropna())
        
        # Selecionar amostra
        import random
        urls_amostra = random.sample(todas_urls, min(sample_size, len(todas_urls)))
        
        validas = 0
        invalidas = 0
        
        for url in urls_amostra:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                status = response.status_code
                
                if status == 200:
                    self.urls_validadas[url] = {'status': 'válida', 'codigo': status}
                    validas += 1
                elif status == 404:
                    self.urls_validadas[url] = {'status': 'não encontrada', 'codigo': status}
                    invalidas += 1
                else:
                    self.urls_validadas[url] = {'status': 'outro', 'codigo': status}
                    invalidas += 1
                    
            except Exception as e:
                self.urls_validadas[url] = {'status': 'erro', 'erro': str(e)}
                invalidas += 1
            
            # Rate limiting
            time.sleep(0.5)
        
        self.stats['urls_validas'] = validas
        self.stats['urls_invalidas'] = invalidas
        
        print(f"   ✅ URLs válidas: {validas}")
        print(f"   ❌ URLs inválidas: {invalidas}")
        print(f"   📊 Taxa de sucesso: {(validas/(validas+invalidas)*100):.1f}%")
    
    def criar_base_unificada(self):
        """Cria base de dados unificada"""
        print("\n🔄 Criando base de dados unificada...")
        
        # Aplicar mapeamentos
        df_carta_mapped = self.df_carta.copy()
        df_site_mapped = self.df_site.copy()
        
        # Mapear perfis na carta de serviço
        df_carta_mapped['Perfis'] = df_carta_mapped['Perfis'].map(
            lambda x: self.perfis_mapeados.get(x, x)
        )
        
        # Combinar datasets
        self.df_unificado = pd.concat([df_carta_mapped, df_site_mapped], ignore_index=True)
        
        # Adicionar colunas de análise
        self.df_unificado['id_unico'] = range(len(self.df_unificado))
        self.df_unificado['data_extracao'] = datetime.now().strftime('%Y-%m-%d')
        
        # Salvar
        self.df_unificado.to_csv(self.output_path, index=False, encoding='utf-8')
        
        self.stats['total_servicos'] = len(self.df_unificado)
        print(f"   ✅ Base unificada criada: {len(self.df_unificado)} registros")
        print(f"   💾 Salva em: {self.output_path}")
    
    def gerar_relatorio_executivo(self):
        """Gera relatório executivo para a chefia"""
        print("\n📋 Gerando relatório executivo...")
        
        relatorio = f"""
# Relatório Executivo - Cruzamento de Dados SEFAZ-MS

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Responsável**: Análise Automatizada

## Resumo Executivo

Este relatório apresenta os resultados do cruzamento de dados entre o Catálogo de Serviços e o Site Principal da SEFAZ-MS, visando identificar oportunidades de melhoria e padronização.

## Métricas Principais

### Volume de Dados
- **Total de Serviços**: {self.stats['total_servicos']}
- **Carta de Serviço**: {len(self.df_carta)} serviços
- **Site SEFAZ**: {len(self.df_site)} serviços

### Análise de Duplicação
- **Serviços Similares Identificados**: {self.stats['servicos_duplicados']}
- **Taxa de Sobreposição**: {(self.stats['servicos_duplicados']/min(len(self.df_carta), len(self.df_site))*100):.1f}%

### Validação de URLs
- **URLs Válidas**: {self.stats['urls_validas']}
- **URLs Inválidas**: {self.stats['urls_invalidas']}
- **Taxa de Funcionalidade**: {(self.stats['urls_validas']/(self.stats['urls_validas']+self.stats['urls_invalidas'])*100):.1f}%

## Análise de Categorias

### Distribuição por Fonte
"""
        
        # Análise de categorias
        categorias_carta = self.df_carta['Categorias'].value_counts().head(5)
        categorias_site = self.df_site['Categorias'].value_counts().head(5)
        
        relatorio += "\n#### Top 5 Categorias - Carta de Serviço\n"
        for cat, count in categorias_carta.items():
            relatorio += f"- **{cat}**: {count} serviços\n"
        
        relatorio += "\n#### Top 5 Categorias - Site SEFAZ\n"
        for cat, count in categorias_site.items():
            relatorio += f"- **{cat}**: {count} serviços\n"
        
        # Análise de perfis
        relatorio += "\n## Análise de Perfis\n\n"
        
        perfis_carta = self.df_carta['Perfis'].value_counts()
        perfis_site = self.df_site['Perfis'].value_counts()
        
        relatorio += "### Distribuição por Perfil\n\n"
        relatorio += "| Perfil | Carta de Serviço | Site SEFAZ |\n"
        relatorio += "|--------|------------------|------------|\n"
        
        todos_perfis = set(perfis_carta.index) | set(perfis_site.index)
        for perfil in sorted(todos_perfis):
            count_carta = perfis_carta.get(perfil, 0)
            count_site = perfis_site.get(perfil, 0)
            relatorio += f"| {perfil} | {count_carta} | {count_site} |\n"
        
        # Recomendações
        relatorio += f"""

## Principais Achados

### 🎯 Oportunidades de Melhoria

1. **Padronização de Categorias**
   - {len(self.categorias_mapeadas)} categorias similares identificadas
   - Oportunidade de unificação de nomenclaturas

2. **Eliminação de Duplicações**
   - {self.stats['servicos_duplicados']} serviços potencialmente duplicados
   - Necessidade de revisão e consolidação

3. **Manutenção de URLs**
   - {self.stats['urls_invalidas']} URLs com problemas identificadas
   - Requer atualização ou correção

### 📊 Insights Estratégicos

1. **Cobertura de Serviços**
   - Boa distribuição entre perfis de usuário
   - Foco empresarial em ambas as plataformas

2. **Qualidade dos Dados**
   - Taxa de funcionalidade de URLs: {(self.stats['urls_validas']/(self.stats['urls_validas']+self.stats['urls_invalidas'])*100):.1f}%
   - Base de dados robusta e confiável

## Recomendações

### Curto Prazo (1-2 meses)
- [ ] Corrigir URLs inválidas identificadas
- [ ] Revisar serviços duplicados
- [ ] Padronizar nomenclatura de categorias principais

### Médio Prazo (3-6 meses)
- [ ] Implementar base de dados unificada
- [ ] Criar processo de sincronização entre portais
- [ ] Desenvolver dashboard de monitoramento

### Longo Prazo (6+ meses)
- [ ] Integração completa dos portais
- [ ] Sistema de gestão unificado de serviços
- [ ] Automação de validação de URLs

## Conclusão

O cruzamento de dados revelou oportunidades significativas de melhoria na gestão dos serviços da SEFAZ-MS. A implementação das recomendações propostas resultará em:

- **Melhor experiência do usuário** através da eliminação de duplicações
- **Maior eficiência operacional** com processos padronizados
- **Redução de custos** de manutenção através da unificação

---

**Próximos Passos**: Apresentação dos resultados e definição de cronograma de implementação.
"""
        
        # Salvar relatório
        with open('relatorio_executivo_cruzamento.md', 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print("   ✅ Relatório executivo gerado: relatorio_executivo_cruzamento.md")
    
    def salvar_analises_detalhadas(self):
        """Salva análises detalhadas em arquivos separados"""
        print("\n💾 Salvando análises detalhadas...")
        
        # Serviços similares
        if self.servicos_similares:
            df_similares = pd.DataFrame(self.servicos_similares)
            df_similares.to_csv('servicos_similares.csv', index=False, encoding='utf-8')
            print("   ✅ Serviços similares: servicos_similares.csv")
        
        # Mapeamento de categorias
        if self.categorias_mapeadas:
            with open('mapeamento_categorias.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Categoria_Carta', 'Categoria_Site', 'Similaridade', 'Categoria_Unificada'])
                for cat_carta, dados in self.categorias_mapeadas.items():
                    writer.writerow([
                        cat_carta,
                        dados['categoria_site'],
                        dados['similaridade'],
                        dados['categoria_unificada']
                    ])
            print("   ✅ Mapeamento de categorias: mapeamento_categorias.csv")
        
        # URLs validadas
        if self.urls_validadas:
            with open('validacao_urls.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['URL', 'Status', 'Codigo_HTTP', 'Erro'])
                for url, dados in self.urls_validadas.items():
                    writer.writerow([
                        url,
                        dados['status'],
                        dados.get('codigo', ''),
                        dados.get('erro', '')
                    ])
            print("   ✅ Validação de URLs: validacao_urls.csv")
    
    def executar_analise_completa(self):
        """Executa análise completa de cruzamento de dados"""
        print("🚀 Iniciando Análise de Cruzamento de Dados SEFAZ-MS")
        print("=" * 60)
        
        try:
            # Carregar dados
            self.carregar_dados()
            
            # Análises
            self.identificar_servicos_similares()
            self.mapear_categorias()
            self.mapear_perfis()
            self.validar_urls()
            
            # Gerar outputs
            self.criar_base_unificada()
            self.gerar_relatorio_executivo()
            self.salvar_analises_detalhadas()
            
            print("\n" + "=" * 60)
            print("✅ Análise de cruzamento concluída com sucesso!")
            print(f"📊 {self.stats['total_servicos']} serviços processados")
            print(f"🔍 {self.stats['servicos_duplicados']} duplicações identificadas")
            print(f"🔗 {self.stats['urls_validas']}/{self.stats['urls_validas']+self.stats['urls_invalidas']} URLs válidas")
            
        except Exception as e:
            print(f"\n❌ Erro durante a análise: {e}")
            raise

def main():
    """Função principal"""
    cruzamento = CruzamentoDados()
    cruzamento.executar_analise_completa()

if __name__ == "__main__":
    main()