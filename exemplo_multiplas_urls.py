#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do SefazScraper para múltiplas URLs
Este script demonstra como usar o scraper para coletar dados de diferentes perfis do catálogo SEFAZ-MS
"""

import logging
from sefaz_scraper import SefazScraper

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping_multiplas_urls.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Função principal para scraping de múltiplas URLs por perfil"""
    
    # URLs organizadas por perfil do site SEFAZ-MS
    urls_por_perfil = {
        "Agropecuária": [
            "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/autorizacoes-cap/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/regimes-especiais-cap/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/cadastro-cap/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/contencioso-cap/",
        ],
        "Comércio, Indústria e Serviços": [
            "https://www.catalogo.sefaz.ms.gov.br/Geral/comercio-industria-servicos/autorizacoes-ccis/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/comercio-industria-servicos/regimes-especiais-ccis/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/comercio-industria-servicos/cadastro-ccis/",
            "https://www.catalogo.sefaz.ms.gov.br/Geral/comercio-industria-servicos/contencioso-ccis/",
        ]
    }
    
    # Inicializa o scraper
    scraper = SefazScraper()
    
    total_urls = sum(len(urls) for urls in urls_por_perfil.values())
    logger.info("Iniciando scraping de múltiplas URLs por perfil")
    logger.info(f"Total de perfis: {len(urls_por_perfil)}")
    logger.info(f"Total de URLs para processar: {total_urls}")
    
    url_counter = 0
    
    # Processa cada perfil e suas URLs
    for perfil, urls in urls_por_perfil.items():
        logger.info(f"\n{'='*80}")
        logger.info(f"PROCESSANDO PERFIL: {perfil}")
        logger.info(f"URLs do perfil: {len(urls)}")
        logger.info(f"{'='*80}")
        
        for url in urls:
            url_counter += 1
            logger.info(f"\n[{url_counter}/{total_urls}] Processando: {url}")
            
            try:
                scraper.scrape_page(url)
                logger.info(f"✅ URL processada com sucesso")
            except Exception as e:
                logger.error(f"❌ Erro ao processar URL: {e}")
                continue
    
    # Salva os dados coletados
    output_file = "sefaz_multiplos_perfis.csv"
    scraper.save_to_csv(output_file)
    
    # Estatísticas finais
    total_records = len(scraper.data)
    logger.info(f"\n{'='*80}")
    logger.info("ESTATÍSTICAS FINAIS")
    logger.info(f"{'='*80}")
    logger.info(f"Total de registros coletados: {total_records}")
    logger.info(f"Arquivo salvo: {output_file}")
    
    # Estatísticas detalhadas
    if scraper.data:
        perfis_count = {}
        categorias_count = {}
        
        for record in scraper.data:
            perfil = record.get('Perfis', 'Não informado')
            categorias = record.get('Categorias', 'Não informado')
            
            perfis_count[perfil] = perfis_count.get(perfil, 0) + 1
            
            # Conta cada categoria individualmente
            if categorias and categorias != 'Não informado':
                for categoria in categorias.split(';'):
                    categoria = categoria.strip()
                    categorias_count[categoria] = categorias_count.get(categoria, 0) + 1
        
        logger.info("\n📊 DISTRIBUIÇÃO POR PERFIS:")
        for perfil, count in sorted(perfis_count.items()):
            logger.info(f"  📁 {perfil}: {count} serviços")
        
        logger.info("\n🏷️  TOP 10 CATEGORIAS MAIS FREQUENTES:")
        top_categorias = sorted(categorias_count.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (categoria, count) in enumerate(top_categorias, 1):
            logger.info(f"  {i:2d}. {categoria}: {count} ocorrências")
        
        # Estatísticas por perfil processado
        logger.info("\n📈 RESUMO POR PERFIL PROCESSADO:")
        for perfil_processado in urls_por_perfil.keys():
            count = perfis_count.get(perfil_processado, 0)
            urls_count = len(urls_por_perfil[perfil_processado])
            logger.info(f"  🎯 {perfil_processado}: {count} serviços de {urls_count} URLs")
    
    logger.info(f"\n🎉 Scraping concluído! Dados salvos em: {output_file}")
    logger.info(f"💾 Log detalhado salvo em: scraping_multiplas_urls.log")

if __name__ == "__main__":
    main()