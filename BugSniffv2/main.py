# main.py
import argparse
from recon_flow import ReconFlow

if __name__ == "__main__":
    # Configura o parser de argumentos para a linha de comando
    parser = argparse.ArgumentParser(description="Ferramenta de automação de reconhecimento - ReconFlow")
    
    # Argumento obrigatório: -l ou --list para o arquivo de domínios
    parser.add_argument("-l", "--list", dest="domain_file", help="Caminho para o arquivo contendo a lista de domínios.", required=True)
    
    # Argumento opcional: -o ou --output para o diretório de saída
    parser.add_argument("-o", "--output", dest="output_dir", help="Pasta onde os resultados serão salvos. Padrão: 'resultados'", default="resultados")

    # Analisa os argumentos passados pelo usuário
    args = parser.parse_args()

    # Cria uma instância da nossa classe principal com os argumentos fornecidos
    flow = ReconFlow(domain_file=args.domain_file, output_dir=args.output_dir)
    
    # Inicia o fluxo de execução
    flow.run()