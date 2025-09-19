# recon_flow.py
import os
from scanner import Scanner

class ReconFlow:
    def __init__(self, domain_file, output_dir, shodan_key=None):
        self.domain_file = domain_file
        self.output_dir = output_dir
        self.shodan_key = shodan_key # Novo atributo
        self.targets = []
        self.scanner = Scanner(self.output_dir)
        
        print(f"[*] ReconFlow (Fase 1) iniciado.")
        print(f"[*] Arquivo de alvos: {self.domain_file}")
        if self.shodan_key:
            print("[*] Chave do Shodan fornecida.")
        print(f"[*] Diretório de saída: {self.output_dir}")

    def _load_targets(self):
        try:
            with open(self.domain_file, 'r') as f:
                self.targets = [line.strip() for line in f if line.strip()]
            if not self.targets:
                print("❌ ERRO: O arquivo de domínios está vazio.")
                return False
            print(f"[*] {len(self.targets)} alvo(s) carregado(s).")
            return True
        except FileNotFoundError:
            print(f"❌ ERRO: Arquivo de domínios '{self.domain_file}' não encontrado.")
            return False

    def _aggregate_httpx_results(self):
        """Junta os resultados de todos os arquivos _validos.txt."""
        final_results = []
        print("\n[*] Agregando subdomínios ativos...")
        for filename in os.listdir(self.output_dir):
            if filename.endswith("_validos.txt"):
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, 'r') as f:
                    final_results.extend([line.strip() for line in f if line.strip()])
        return sorted(set(final_results))

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)

        if not self._load_targets():
            return

        for target in self.targets:
            print(f"\n--- Processando Alvo: {target} ---")
            
            # Passa a chave do Shodan (pode ser None) para o scanner
            subdomains_file = self.scanner.run_subfinder(target, shodan_key=self.shodan_key)
            if not subdomains_file: continue

            self.scanner.run_httpx(subdomains_file)

        # Agrega todos os resultados válidos em um único arquivo
        aggregated_results = self._aggregate_httpx_results()
        
        if not aggregated_results:
             print("\n[*] Nenhum subdomínio ativo foi encontrado.")
        else:
            final_output_file = os.path.join(self.output_dir, "subdominios_ativos_final.txt")
            with open(final_output_file, 'w') as f:
                for result in aggregated_results:
                    f.write(f"{result}\n")
            print(f"\n[*] Lista final de subdomínios ativos salva em: {final_output_file}")

        print("\n[*] Fluxo de trabalho concluído!")