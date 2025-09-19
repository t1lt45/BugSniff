# main.py
import argparse
from recon_flow import ReconFlow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fase 1: Ferramenta de descoberta e validação de subdomínios.")
    
    parser.add_argument("-l", "--list", dest="domain_file", help="Caminho para o arquivo contendo a lista de domínios.", required=True)
    
    # NOVO: Argumento opcional para a chave da API do Shodan
    parser.add_argument("-sk", "--shodan-key", dest="shodan_key", help="Chave da API do Shodan para enriquecer os resultados do Subfinder.", default=None)

    parser.add_argument("-o", "--output", dest="output_dir", help="Pasta onde os resultados serão salvos. Padrão: 'resultados'", default="resultados")

    args = parser.parse_args()

    # Passa a chave (ou None, se não for fornecida) para a classe principal
    flow = ReconFlow(domain_file=args.domain_file, output_dir=args.output_dir, shodan_key=args.shodan_key)
    
    flow.run()