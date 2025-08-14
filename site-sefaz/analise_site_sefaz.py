import csv
from collections import Counter, defaultdict
import re

class AnaliseSiteSefaz:
    def __init__(self, csv_file="sefaz_site_servicos.csv"):
        self.csv_file = csv_file
        self.data = []
        self.load_data()
    
    def load_data(self):
        """Carrega dados do arquivo CSV"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.data = [row for row in reader]
            print(f"Dados carregados: {len(self.data)} registros")
        except FileNotFoundError:
            print(f"Arquivo {self.csv_file} não encontrado!")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def analyze_categories(self):
        """Analisa a distribuição de categorias"""
        categories = [row['Categorias'] for row in self.data]
        category_count = Counter(categories)
        
        print("\n=== ANÁLISE DE CATEGORIAS ===")
        print(f"Total de categorias únicas: {len(category_count)}")
        print("\nTop 10 categorias mais frequentes:")
        for category, count in category_count.most_common(10):
            percentage = (count / len(self.data)) * 100
            print(f"  {category}: {count} serviços ({percentage:.1f}%)")
        
        return category_count
    
    def analyze_by_profile(self):
        """Analisa serviços por perfil"""
        profile_data = defaultdict(list)
        
        for row in self.data:
            profile_data[row['Perfis']].append(row)
        
        print("\n=== ANÁLISE POR PERFIL ===")
        for profile, services in profile_data.items():
            categories = set(service['Categorias'] for service in services)
            print(f"\n{profile}:")
            print(f"  Serviços: {len(services)}")
            print(f"  Categorias únicas: {len(categories)}")
            print(f"  Média de categorias por serviço: {len(categories)/len(services):.1f}")
            
            # Top 3 categorias por perfil
            profile_categories = Counter(service['Categorias'] for service in services)
            print("  Top 3 categorias:")
            for cat, count in profile_categories.most_common(3):
                print(f"    - {cat}: {count} serviços")
        
        return profile_data
    
    def analyze_urls(self):
        """Analisa padrões de URLs"""
        urls = [row['URL'] for row in self.data]
        
        # Domínios
        domains = []
        for url in urls:
            if 'catalogo.sefaz.ms.gov.br' in url:
                domains.append('catalogo.sefaz.ms.gov.br')
            elif 'servicos.efazenda.ms.gov.br' in url:
                domains.append('servicos.efazenda.ms.gov.br')
            elif 'sefaz.ms.gov.br' in url:
                domains.append('sefaz.ms.gov.br')
            else:
                domains.append('outros')
        
        domain_count = Counter(domains)
        
        print("\n=== ANÁLISE DE URLs ===")
        print("Distribuição por domínio:")
        for domain, count in domain_count.most_common():
            percentage = (count / len(urls)) * 100
            print(f"  {domain}: {count} URLs ({percentage:.1f}%)")
        
        # Tipos de arquivo
        file_types = []
        for url in urls:
            if url.endswith('.pdf'):
                file_types.append('PDF')
            elif url.endswith('.doc') or url.endswith('.docx'):
                file_types.append('DOC')
            else:
                file_types.append('WEB')
        
        file_count = Counter(file_types)
        print("\nTipos de recursos:")
        for file_type, count in file_count.most_common():
            percentage = (count / len(urls)) * 100
            print(f"  {file_type}: {count} recursos ({percentage:.1f}%)")
        
        return domain_count, file_count
    
    def analyze_service_names(self):
        """Analisa padrões nos nomes dos serviços"""
        services = [row['Serviços'] for row in self.data]
        
        # Palavras-chave mais comuns
        all_words = []
        for service in services:
            # Remove caracteres especiais e converte para minúsculas
            words = re.findall(r'\b\w+\b', service.lower())
            # Filtra palavras com mais de 3 caracteres
            words = [word for word in words if len(word) > 3]
            all_words.extend(words)
        
        word_count = Counter(all_words)
        
        print("\n=== ANÁLISE DE NOMES DE SERVIÇOS ===")
        print("Palavras-chave mais frequentes:")
        for word, count in word_count.most_common(15):
            print(f"  {word}: {count} ocorrências")
        
        # Serviços por tipo (baseado em palavras-chave)
        service_types = {
            'Cadastro': ['cadastro', 'inscrição', 'registro'],
            'Certidão': ['certidão', 'certidao', 'atestado'],
            'Consulta': ['consulta', 'pesquisa'],
            'Emissão': ['emissão', 'emissao', 'geração'],
            'Declaração': ['declaração', 'declaracao'],
            'Processo': ['processo', 'procedimento']
        }
        
        type_count = defaultdict(int)
        for service in services:
            service_lower = service.lower()
            for service_type, keywords in service_types.items():
                if any(keyword in service_lower for keyword in keywords):
                    type_count[service_type] += 1
                    break
            else:
                type_count['Outros'] += 1
        
        print("\nClassificação por tipo de serviço:")
        for service_type, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(services)) * 100
            print(f"  {service_type}: {count} serviços ({percentage:.1f}%)")
        
        return word_count, type_count
    
    def generate_insights(self):
        """Gera insights estratégicos"""
        print("\n=== INSIGHTS ESTRATÉGICOS ===")
        
        # Perfil com mais serviços
        profile_counts = Counter(row['Perfis'] for row in self.data)
        top_profile = profile_counts.most_common(1)[0]
        print(f"1. Perfil prioritário: {top_profile[0]} ({top_profile[1]} serviços)")
        
        # Categoria mais comum
        category_counts = Counter(row['Categorias'] for row in self.data)
        top_category = category_counts.most_common(1)[0]
        print(f"2. Categoria principal: {top_category[0]} ({top_category[1]} serviços)")
        
        # Análise de digitalização
        pdf_count = sum(1 for row in self.data if row['URL'].endswith('.pdf'))
        digital_percentage = ((len(self.data) - pdf_count) / len(self.data)) * 100
        print(f"3. Nível de digitalização: {digital_percentage:.1f}% dos serviços são digitais")
        
        # Distribuição de complexidade (baseada no tamanho do nome)
        avg_name_length = sum(len(row['Serviços']) for row in self.data) / len(self.data)
        print(f"4. Complexidade média dos nomes: {avg_name_length:.0f} caracteres")
        
        # Perfis com menor cobertura
        min_profile = profile_counts.most_common()[-1]
        print(f"5. Perfil com menor cobertura: {min_profile[0]} ({min_profile[1]} serviços)")
    
    def save_detailed_report(self, filename="relatorio_detalhado_site_sefaz.txt"):
        """Salva relatório detalhado em arquivo"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DETALHADO - ANÁLISE SITE SEFAZ-MS\n")
            f.write("=" * 50 + "\n\n")
            
            # Estatísticas gerais
            f.write(f"Total de serviços: {len(self.data)}\n")
            f.write(f"Total de perfis: {len(set(row['Perfis'] for row in self.data))}\n")
            f.write(f"Total de categorias: {len(set(row['Categorias'] for row in self.data))}\n\n")
            
            # Distribuição por perfil
            profile_counts = Counter(row['Perfis'] for row in self.data)
            f.write("DISTRIBUIÇÃO POR PERFIL:\n")
            for profile, count in profile_counts.most_common():
                percentage = (count / len(self.data)) * 100
                f.write(f"  {profile}: {count} ({percentage:.1f}%)\n")
            
            f.write("\nCATEGORIAS MAIS FREQUENTES:\n")
            category_counts = Counter(row['Categorias'] for row in self.data)
            for category, count in category_counts.most_common(10):
                f.write(f"  {category}: {count}\n")
        
        print(f"\nRelatório detalhado salvo em: {filename}")
    
    def run_complete_analysis(self):
        """Executa análise completa"""
        print("INICIANDO ANÁLISE COMPLETA DOS DADOS DO SITE SEFAZ-MS")
        print("=" * 60)
        
        self.analyze_categories()
        self.analyze_by_profile()
        self.analyze_urls()
        self.analyze_service_names()
        self.generate_insights()
        self.save_detailed_report()
        
        print("\n" + "=" * 60)
        print("ANÁLISE COMPLETA FINALIZADA!")
        print("=" * 60)

def main():
    analyzer = AnaliseSiteSefaz()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()