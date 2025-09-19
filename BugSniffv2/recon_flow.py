# recon_flow.py
import os
from scanner import Scanner
from url_processor import URLProcessor

class ReconFlow:
    def __init__(self, domain_file, output_dir):
        """Construtor da classe ReconFlow."""
        self.domain_file = domain_file
        self.output_dir = output_dir
        self.targets = []
        self.scanner = Scanner(self.output_dir)
        self.url_processor = URLProcessor()
        
        print(f"[*] ReconFlow iniciado.")
        print(f"[*] Arquivo de alvos: {self.domain_file}")
        print(f"[*] Diretório de saída: {self.output_dir}")

    def _load_targets(self):
        """Carrega os domínios alvo do arquivo de entrada."""
        try:
            with open(self.domain_file, 'r') as f:
                # Remove espaços em branco e linhas vazias
                self.targets = [line.strip() for line in f if line.strip()]
            if not self.targets:
                print("❌ ERRO: O arquivo de domínios está vazio.")
                return False
            print(f"[*] {len(self.targets)} alvo(s) carregado(s).")
            return True
        except FileNotFoundError:
            print(f"❌ ERRO: Arquivo de domínios '{self.domain_file}' não encontrado.")
            return False

    def _aggregate_results(self):
        """Junta os resultados de URLs de todos os arquivos _online.txt."""
        all_urls = []
        print("[*] Juntando todos os resultados de URLs...")
        for target in self.targets:
            katana_output_file = os.path.join(self.output_dir, f"{target}_online.txt")
            if os.path.exists(katana_output_file):
                with open(katana_output_file, 'r') as f:
                    all_urls.extend([line.strip() for line in f if line.strip()])
        return all_urls

    def run(self):
        """Inicia a execução do fluxo de reconhecimento."""
        os.makedirs(self.output_dir, exist_ok=True)

        if not self._load_targets():
            return # Para a execução se não conseguir carregar os alvos

        for target in self.targets:
            print(f"\n--- Processando Alvo: {target} ---")
            
            subdomains_file = self.scanner.run_subfinder(target)
            if not subdomains_file: continue # Pula para o próximo alvo se o subfinder falhar

            valid_hosts_file = self.scanner.run_httpx(subdomains_file)
            if not valid_hosts_file: continue # Pula se o httpx falhar
            
            self.scanner.run_katana(valid_hosts_file)
            # Não precisamos verificar o resultado do katana aqui, pois o _aggregate_results cuidará disso

        # Agregação e Filtragem após processar todos os alvos
        total_urls = self._aggregate_results()
        if not total_urls:
            print("\n[*] Nenhuma URL foi encontrada para processar.")
            print("\n[*] Fluxo de trabalho concluído!")
            return

        filtered_urls = self.url_processor.filter_urls(total_urls)

        # Salva o resultado final
        final_output_file = os.path.join(self.output_dir, "URLs_filtradas.txt")
        with open(final_output_file, 'w') as f:
            for url in filtered_urls:
                f.write(f"{url}\n")
        
        print(f"\n[*] Resultado final salvo em: {final_output_file}")
        print("\n[*] Fluxo de trabalho concluído!")