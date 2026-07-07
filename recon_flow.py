# recon_flow.py
import os
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

from scanner import Scanner
from url_processor import URLProcessor
from ui import (
    console, print_step, print_ok, print_error, print_warn,
    make_progress, print_results_table, print_summary, print_url_list,
)


class ReconFlow:
    def __init__(self, domain_file, output_dir, shodan_key=None, concurrency=1,
                 crawl=True, crawl_depth=2):
        self.domain_file = domain_file
        self.output_dir = output_dir
        self.shodan_key = shodan_key
        self.concurrency = max(1, concurrency)
        self.crawl = crawl
        self.crawl_depth = crawl_depth
        self.targets = []
        self.scanner = Scanner(self.output_dir)
        self.url_processor = URLProcessor()
        self.all_results = []      # lista de dicts (url, status_code, title, webserver, tech)
        self.crawled_urls = []     # URLs descobertas pelo Katana, já filtradas

        print_step("ReconFlow iniciado.")
        print_step(f"Arquivo de alvos: {self.domain_file}")
        if self.shodan_key:
            print_step("Chave do Shodan fornecida.")
        print_step(f"Diretório de saída: {self.output_dir}")
        if self.concurrency > 1:
            print_step(f"Concorrência: {self.concurrency} alvo(s) em paralelo.")
        print_step(f"Crawling com Katana: {'ativado' if self.crawl else 'desativado'}.")

    # ------------------------------------------------------------------ #
    def _load_targets(self):
        try:
            with open(self.domain_file, "r") as f:
                self.targets = [line.strip() for line in f if line.strip()]
            if not self.targets:
                print_error("O arquivo de domínios está vazio.")
                return False
            print_ok(f"{len(self.targets)} alvo(s) carregado(s).")
            return True
        except FileNotFoundError:
            print_error(f"Arquivo de domínios '{self.domain_file}' não encontrado.")
            return False

    # ------------------------------------------------------------------ #
    def _process_target(self, target):
        """Executa subfinder + httpx para um único domínio. Retorna lista de resultados."""
        subdomains_file = self.scanner.run_subfinder(target, shodan_key=self.shodan_key)
        if not subdomains_file or not os.path.exists(subdomains_file):
            print_warn(f"Sem subdomínios para {target}, pulando.")
            return []

        if os.path.getsize(subdomains_file) == 0:
            print_warn(f"Subfinder não encontrou subdomínios para {target}.")
            return []

        results = self.scanner.run_httpx(subdomains_file)
        return results

    # ------------------------------------------------------------------ #
    def _save_outputs(self, results):
        """Salva os resultados finais em .txt (compatibilidade) e .csv (dados completos)."""
        if not results:
            return

        txt_path = os.path.join(self.output_dir, "subdominios_ativos_final.txt")
        with open(txt_path, "w") as f:
            for r in results:
                f.write(f"{r['url']}\n")

        csv_path = os.path.join(self.output_dir, "subdominios_ativos_final.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "status_code", "title", "webserver", "tech"])
            writer.writeheader()
            for r in results:
                writer.writerow(r)

        print_ok(f"Lista final (.txt) salva em: {txt_path}")
        print_ok(f"Detalhes completos (.csv) salvos em: {csv_path}")

    # ------------------------------------------------------------------ #
    def run(self):
        start_time = time.time()
        os.makedirs(self.output_dir, exist_ok=True)

        if not self._load_targets():
            return

        with make_progress() as progress:
            task = progress.add_task("Processando alvos...", total=len(self.targets))

            if self.concurrency == 1:
                for target in self.targets:
                    console.print(f"\n[bold]--- Processando Alvo: {target} ---[/bold]")
                    self.all_results.extend(self._process_target(target))
                    progress.advance(task)
            else:
                with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
                    futures = {executor.submit(self._process_target, t): t for t in self.targets}
                    for future in as_completed(futures):
                        target = futures[future]
                        try:
                            res = future.result()
                            self.all_results.extend(res)
                        except Exception as e:
                            print_error(f"Falha ao processar {target}: {e}")
                        progress.advance(task)

        # Dedup por URL, mantendo o primeiro registro encontrado
        seen = set()
        deduped = []
        for r in sorted(self.all_results, key=lambda x: x["url"]):
            if r["url"] not in seen:
                seen.add(r["url"])
                deduped.append(r)
        self.all_results = deduped

        if not self.all_results:
            print_warn("Nenhum subdomínio ativo foi encontrado.")
        else:
            print_results_table(self.all_results)
            self._save_outputs(self.all_results)

            if self.crawl:
                self._run_crawl_step()

        elapsed = f"{time.time() - start_time:.1f}s"
        print_summary(
            len(self.targets), len(self.all_results), self.output_dir, elapsed,
            crawled=len(self.crawled_urls) if self.crawl else None,
        )
        console.print("\n[bold cyan][*] Fluxo de trabalho concluído![/bold cyan]")

    # ------------------------------------------------------------------ #
    def _run_crawl_step(self):
        """
        Etapa de crawling: roda o Katana sobre os hosts JÁ validados como
        ativos (subdominios_ativos_final.txt) para descobrir URLs internas,
        depois filtra o resultado com o URLProcessor (remove extensões e
        domínios indesejados).
        """
        console.print("\n[bold]--- Etapa de Crawling (Katana) ---[/bold]")
        active_urls_file = os.path.join(self.output_dir, "subdominios_ativos_final.txt")

        raw_urls = self.scanner.run_katana(active_urls_file, depth=self.crawl_depth)
        if not raw_urls:
            print_warn("Katana não retornou nenhuma URL (ou não está instalado).")
            return

        filtered_urls = self.url_processor.filter_urls(raw_urls)
        self.crawled_urls = sorted(set(filtered_urls))

        crawl_output_file = os.path.join(self.output_dir, "urls_crawled_final.txt")
        with open(crawl_output_file, "w") as f:
            for url in self.crawled_urls:
                f.write(f"{url}\n")

        print_ok(f"{len(self.crawled_urls)} URL(s) descobertas e filtradas.")
        print_ok(f"Lista salva em: {crawl_output_file}")
        print_url_list(self.crawled_urls, title="URLs Descobertas pelo Katana")
