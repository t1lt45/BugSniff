# scanner.py
import subprocess
import os

class Scanner:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _run_command(self, command, tool_name, env=None):
        """Função auxiliar para executar comandos, agora com suporte a variáveis de ambiente."""
        try:
            print(f"    -> Executando {tool_name}...")
            subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            print(f"    ✅ {tool_name} concluído.")
            return True
        except FileNotFoundError:
            print(f"    ❌ ERRO: '{tool_name}' não foi encontrado. Verifique se ele está instalado e no PATH do sistema.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"    ❌ ERRO: {tool_name} retornou um erro.")
            print(f"    {e.stderr.strip()}")
            return False

    def run_subfinder(self, domain, shodan_key=None):
        """
        Executa o Subfinder. Se uma chave do Shodan for fornecida, a utiliza.
        """
        output_file = os.path.join(self.output_dir, f"{domain}_subdominios.txt")
        command = ["subfinder", "-d", domain, "-o", output_file]
        
        env = None
        if shodan_key:
            print("    -> Usando chave da API do Shodan.")
            env = os.environ.copy()
            env['SHODAN_API_KEY'] = shodan_key
            # Você pode adicionar outras chaves aqui da mesma forma (ex: env['CENSYS_SECRET'] = ...)

        return output_file if self._run_command(command, "Subfinder", env=env) else None

    def run_httpx(self, subdomains_file):
        """
        Executa o Httpx para validar quais subdomínios estão ativos.
        """
        domain_base = os.path.basename(subdomains_file).replace('_subdominios.txt', '')
        output_file = os.path.join(self.output_dir, f"{domain_base}_validos.txt")
        command = ["httpx", "-l", subdomains_file, "-silent", "-o", output_file]
        return output_file if self._run_command(command, "Httpx") else None