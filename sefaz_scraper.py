import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SefazScraper:
    def __init__(self, base_url="https://www.catalogo.sefaz.ms.gov.br"):
        self.base_url = base_url
        self.data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Perfis disponíveis no catálogo SEFAZ-MS
        self.profiles = [
            'agropecuaria',
            'ccis-industria-e-servicos', 
            'cidadao-orgao-governamental',
            'fiscalizacao'
        ]
    
    def get_page_content(self, url):
        """Faz requisição HTTP e retorna o conteúdo da página"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None
    
    def extract_categories_from_div(self, categories_div):
        """Extrai as categorias da div de categorias e retorna como string separada por ;"""
        categories = []
        if categories_div:
            category_links = categories_div.find_all('a', rel='category tag')
            for link in category_links:
                category_text = link.get_text(strip=True)
                # Remove vírgulas para evitar problemas no CSV
                category_text = category_text.replace(',', '')
                categories.append(category_text)
        return ';'.join(categories) if categories else ""
    
    def extract_profile_from_url(self, url):
        """Extrai o perfil da URL (ex: agropecuaria, comercio-industria-servicos)"""
        try:
            # Remove o domínio e divide a URL
            path = url.replace(self.base_url, '').strip('/')
            parts = path.split('/')
            
            # Mapeamento de perfis da URL para nomes legíveis
            profile_mapping = {
                'agropecuaria': 'Agropecuária',
                'ccis-industria-e-servicos': 'Comércio, Indústria e Serviços',
                'cidadao-orgao-governamental': 'Cidadão / Órgão Governamental',
                'autuacoesnotificacoes-fiscalizacao-fiscalizacao': 'Autuações/Notificações - Fiscalização'
            }
            
            # Procura por perfis conhecidos na URL
            for profile_key, profile_name in profile_mapping.items():
                if profile_key in parts:
                    return profile_name
            
            # Se tem 'geral', pega o próximo item
            if 'geral' in parts and len(parts) > 1:
                for i, part in enumerate(parts):
                    if part == 'geral' and i + 1 < len(parts):
                        profile_part = parts[i + 1]
                        if profile_part in profile_mapping:
                            return profile_mapping[profile_part]
            
            # Fallback: tenta extrair do h1
            return ""
        except Exception as e:
            logger.warning(f"Erro ao extrair perfil da URL {url}: {e}")
            return ""
    
    def extract_service_data(self, card_body):
        """Extrai dados de um card-body específico"""
        service_data = {
            'title': '',
            'url': '',
            'categories': ''
        }
        
        # Extrai o link e título do serviço
        main_link = card_body.find('a', href=True)
        if main_link:
            service_data['url'] = urljoin(self.base_url, main_link['href'])
            
            # Extrai o título do h5
            title_element = main_link.find('h5', class_='card-title')
            if title_element:
                service_data['title'] = title_element.get_text(strip=True)
        
        # Extrai as categorias da div categorias mt-2
        categories_div = card_body.find('div', class_='categorias')
        service_data['categories'] = self.extract_categories_from_div(categories_div)
        
        return service_data
    
    def get_pagination_urls(self, soup, current_url):
        """Extrai URLs de paginação da div paginacao"""
        pagination_urls = []
        pagination_div = soup.find('div', class_='paginacao')
        
        if pagination_div:
            pagination_links = pagination_div.find_all('a', href=True)
            for link in pagination_links:
                href = link.get('href')
                if href and href != '#':
                    full_url = urljoin(self.base_url, href)
                    if full_url != current_url and full_url not in pagination_urls:
                        pagination_urls.append(full_url)
        
        return pagination_urls
    
    def scrape_page(self, url, visited_urls=None):
        """Scraping de uma página específica com suporte à paginação"""
        if visited_urls is None:
            visited_urls = set()
        
        if url in visited_urls:
            return
        
        visited_urls.add(url)
        logger.info(f"Fazendo scraping da página: {url}")
        
        content = self.get_page_content(url)
        if not content:
            return
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extrai o perfil da URL
        main_profile = self.extract_profile_from_url(url)
        
        # Se não conseguiu extrair da URL, tenta do h1
        if not main_profile:
            h1_element = soup.find('h1', class_='green')
            if h1_element:
                main_profile = h1_element.get_text(strip=True)
        
        logger.info(f"Perfil encontrado: {main_profile}")
        
        # Encontra todos os card-body
        card_bodies = soup.find_all('div', class_='card-body')
        logger.info(f"Encontrados {len(card_bodies)} serviços")
        
        for card_body in card_bodies:
            service_data = self.extract_service_data(card_body)
            
            if service_data['title'] and service_data['url']:
                self.data.append({
                    'Categorias': service_data['categories'],
                    'Perfis': main_profile,
                    'Serviços': service_data['title'],
                    'URL': service_data['url']
                })
        
        # Verifica se há paginação e processa as páginas adicionais
        pagination_urls = self.get_pagination_urls(soup, url)
        if pagination_urls:
            logger.info(f"Encontradas {len(pagination_urls)} páginas adicionais")
            for page_url in pagination_urls:
                self.scrape_page(page_url, visited_urls)
        
        # Pausa entre requisições para ser respeitoso com o servidor
        time.sleep(1)
    
    def save_to_csv(self, filename='sefaz_servicos.csv'):
        """Salva os dados coletados em um arquivo CSV"""
        if not self.data:
            logger.warning("Nenhum dado foi coletado")
            return
        
        fieldnames = ['Categorias', 'Perfis', 'Serviços', 'URL']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info(f"Dados salvos em {filename}. Total de registros: {len(self.data)}")
    
    def generate_profile_urls(self):
        """Gera URLs para todos os perfis disponíveis"""
        urls = []
        for profile in self.profiles:
            url = f"{self.base_url}/Geral/{profile}/"
            urls.append(url)
        return urls
    
    def run_scraper(self, urls=None):
        """Executa o scraper para uma lista de URLs ou todos os perfis"""
        if urls is None:
            urls = self.generate_profile_urls()
            logger.info(f"Fazendo scraping de todos os perfis: {', '.join(self.profiles)}")
        
        logger.info(f"Iniciando scraper para {len(urls)} URLs")
        
        for url in urls:
            logger.info(f"Processando perfil: {url}")
            self.scrape_page(url)
        
        self.save_to_csv()
        logger.info("Scraping concluído!")
        
        # Estatísticas por perfil
        self.print_statistics()

    def print_statistics(self):
        """Exibe estatísticas dos dados coletados"""
        if not self.data:
            return
        
        # Estatísticas por perfil
        profile_stats = {}
        for item in self.data:
            profile = item['Perfis']
            if profile not in profile_stats:
                profile_stats[profile] = 0
            profile_stats[profile] += 1
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS DO SCRAPING")
        print("="*60)
        print(f"Total de serviços coletados: {len(self.data)}")
        print("\nDistribuição por perfil:")
        for profile, count in sorted(profile_stats.items()):
            print(f"  • {profile}: {count} serviços")
        
        # Amostra dos dados
        print("\nAmostra dos dados coletados:")
        for i, item in enumerate(self.data[:3]):
            print(f"\n{i+1}. Categorias: {item['Categorias'][:80]}{'...' if len(item['Categorias']) > 80 else ''}")
            print(f"   Perfil: {item['Perfis']}")
            print(f"   Serviço: {item['Serviços'][:80]}{'...' if len(item['Serviços']) > 80 else ''}")
            print(f"   URL: {item['URL']}")

def main():
    """Função principal - executa scraping de todos os perfis"""
    scraper = SefazScraper()
    
    # Opção 1: Scraping de todos os perfis automaticamente
    print("Iniciando scraping de todos os perfis do catálogo SEFAZ-MS...")
    scraper.run_scraper()
    
    # Opção 2: Scraping de perfis específicos (descomente se necessário)
    # urls_especificas = [
    #     "https://www.catalogo.sefaz.ms.gov.br/Geral/agropecuaria/",
    #     "https://www.catalogo.sefaz.ms.gov.br/Geral/ccis-industria-e-servicos/"
    # ]
    # scraper.run_scraper(urls_especificas)

if __name__ == "__main__":
    main()