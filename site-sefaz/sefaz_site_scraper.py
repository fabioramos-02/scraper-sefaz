import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin, urlparse
import re

class SefazSiteScraper:
    def __init__(self, base_url="https://www.sefaz.ms.gov.br/"):
        self.base_url = base_url
        self.profiles = [
            'cidadao-post',
            'produtor-rural-post', 
            'empresa-post',
            'poder-publico-post',
            'contabilista-post'
        ]
        self.profile_mapping = {
            'cidadao-post': 'Cidadão',
            'produtor-rural-post': 'Produtor Rural',
            'empresa-post': 'Empresa', 
            'poder-publico-post': 'Poder Público',
            'contabilista-post': 'Contabilista'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        self.statistics = {
            'total_services': 0,
            'services_by_profile': {},
            'categories_found': set(),
            'errors': []
        }

    def get_page_content(self, url):
        """Obtém o conteúdo HTML de uma página"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            error_msg = f"Erro ao acessar {url}: {str(e)}"
            print(error_msg)
            self.statistics['errors'].append(error_msg)
            return None

    def extract_services_from_page(self, url, profile_name):
        """Extrai serviços de uma página específica do perfil"""
        print(f"Extraindo serviços de: {url}")
        
        html_content = self.get_page_content(url)
        if not html_content:
            return
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Encontrar todas as colunas de listas
        list_columns = soup.find_all('div', class_='daems-list-column')
        
        for column in list_columns:
            # Encontrar todas as listas dentro da coluna
            service_lists = column.find_all('ul', class_='daems-list')
            
            for service_list in service_lists:
                # Extrair o título da categoria
                category_element = service_list.find('li', class_='daems-titulos')
                if not category_element:
                    continue
                    
                category_name = category_element.get_text(strip=True)
                self.statistics['categories_found'].add(category_name)
                
                # Extrair todos os serviços desta categoria
                service_items = service_list.find_all('li', class_='daems-list-itens')
                
                for item in service_items:
                    link_element = item.find('a')
                    if link_element and link_element.get('href'):
                        service_name = link_element.get_text(strip=True)
                        service_url = link_element.get('href').strip()
                        
                        # Limpar URL se necessário
                        if service_url.startswith(' '):
                            service_url = service_url.strip()
                        
                        # Validar se é uma URL válida
                        if service_name and service_url and self.is_valid_url(service_url):
                            service_data = {
                                'categoria': category_name,
                                'perfil': profile_name,
                                'servico': service_name,
                                'url': service_url
                            }
                            
                            self.scraped_data.append(service_data)
                            self.statistics['total_services'] += 1
                            
                            # Atualizar estatísticas por perfil
                            if profile_name not in self.statistics['services_by_profile']:
                                self.statistics['services_by_profile'][profile_name] = 0
                            self.statistics['services_by_profile'][profile_name] += 1
                            
                            print(f"  Categoria: {category_name} | Serviço: {service_name[:50]}...")

    def is_valid_url(self, url):
        """Valida se uma string é uma URL válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def generate_profile_urls(self, profiles=None):
        """Gera URLs para os perfis especificados"""
        if profiles is None:
            profiles = self.profiles
        
        urls = []
        for profile in profiles:
            url = urljoin(self.base_url, f"{profile}/")
            urls.append((url, self.profile_mapping.get(profile, profile)))
        
        return urls

    def save_to_csv(self, filename="sefaz_site_servicos.csv"):
        """Salva os dados extraídos em um arquivo CSV"""
        if not self.scraped_data:
            print("Nenhum dado para salvar.")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Categorias', 'Perfis', 'Serviços', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in self.scraped_data:
                writer.writerow({
                    'Categorias': data['categoria'],
                    'Perfis': data['perfil'],
                    'Serviços': data['servico'],
                    'URL': data['url']
                })
        
        print(f"Dados salvos em: {filename}")
        print(f"Total de registros: {len(self.scraped_data)}")

    def print_statistics(self):
        """Exibe estatísticas do scraping"""
        print("\n" + "="*60)
        print("ESTATÍSTICAS DO SCRAPING - SEFAZ SITE")
        print("="*60)
        print(f"Total de serviços coletados: {self.statistics['total_services']}")
        print(f"Total de categorias encontradas: {len(self.statistics['categories_found'])}")
        
        print("\nDistribuição por perfil:")
        for profile, count in self.statistics['services_by_profile'].items():
            percentage = (count / self.statistics['total_services']) * 100 if self.statistics['total_services'] > 0 else 0
            print(f"  {profile}: {count} serviços ({percentage:.1f}%)")
        
        print("\nCategorias encontradas:")
        for category in sorted(self.statistics['categories_found']):
            print(f"  - {category}")
        
        if self.statistics['errors']:
            print("\nErros encontrados:")
            for error in self.statistics['errors']:
                print(f"  - {error}")
        
        print("\nAmostra dos dados coletados:")
        for i, data in enumerate(self.scraped_data[:5]):
            print(f"  {i+1}. {data['categoria']} | {data['perfil']} | {data['servico'][:50]}...")
        
        print("="*60)

    def run_scraper(self, profiles=None, delay=1):
        """Executa o scraper para os perfis especificados"""
        print("Iniciando scraping do site SEFAZ-MS...")
        
        profile_urls = self.generate_profile_urls(profiles)
        
        for url, profile_name in profile_urls:
            print(f"\nProcessando perfil: {profile_name}")
            self.extract_services_from_page(url, profile_name)
            
            # Delay entre requisições
            if delay > 0:
                time.sleep(delay)
        
        print("\nScraping concluído!")
        self.print_statistics()

def main():
    """Função principal"""
    scraper = SefazSiteScraper()
    
    # Processar todos os perfis
    print("Executando scraper para todos os perfis do site SEFAZ-MS")
    scraper.run_scraper()
    
    # Salvar dados
    scraper.save_to_csv()
    
    print("\nScraping completo! Dados salvos em 'sefaz_site_servicos.csv'")
    print("Para processar apenas um perfil específico, use:")
    print("scraper.run_scraper(profiles=['cidadao-post'])  # exemplo")

if __name__ == "__main__":
    main()