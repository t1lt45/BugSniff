# main.py
import argparse
import sys

from ui import print_banner, print_error
from recon_flow import ReconFlow

VERSION = "2.0"


def build_parser():
    parser = argparse.ArgumentParser(
        description="BugSniff — Descoberta e validação de subdomínios para Bug Bounty e Pentest.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplo: python3 main.py -l dominios.txt -o resultados -c 5",
    )

    parser.add_argument(
        "-l", "--list", dest="domain_file", required=True,
        help="Caminho para o arquivo contendo a lista de domínios (um por linha).",
    )
    parser.add_argument(
        "-sk", "--shodan-key", dest="shodan_key", default=None,
        help="Chave da API do Shodan para enriquecer os resultados do Subfinder.",
    )
    parser.add_argument(
        "-o", "--output", dest="output_dir", default="resultados",
        help="Pasta onde os resultados serão salvos. Padrão: 'resultados'.",
    )
    parser.add_argument(
        "-c", "--concurrency", dest="concurrency", type=int, default=1,
        help="Quantidade de domínios processados em paralelo. Padrão: 1 (sequencial).",
    )
    parser.add_argument(
        "--skip-crawl", dest="skip_crawl", action="store_true",
        help="Pula a etapa de crawling com Katana (só descoberta + validação, mais rápido).",
    )
    parser.add_argument(
        "--crawl-depth", dest="crawl_depth", type=int, default=2,
        help="Profundidade do crawling do Katana. Padrão: 2.",
    )
    parser.add_argument(
        "--version", action="version", version=f"BugSniff v{VERSION} — by 0xtiltas",
    )

    return parser


if __name__ == "__main__":
    print_banner(version=VERSION)

    parser = build_parser()
    args = parser.parse_args()

    if args.concurrency < 1:
        print_error("Concorrência deve ser >= 1.")
        sys.exit(1)

    flow = ReconFlow(
        domain_file=args.domain_file,
        output_dir=args.output_dir,
        shodan_key=args.shodan_key,
        concurrency=args.concurrency,
        crawl=not args.skip_crawl,
        crawl_depth=args.crawl_depth,
    )

    flow.run()
