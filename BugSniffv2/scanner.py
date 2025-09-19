# scanner.py
import subprocess
import os

class Scanner:
    def __init__(self, output_dir):
        """
        Inicializa o Scanner.
        :param output_dir: Diretório onde os arquivos de resultado temporários serão salvos.
        """
        self.output_dir = output_dir
        # Garante que o diretório de saída para os scans de cada domínio exista
        os.makedirs(self.output_dir, exist_ok=True)

    def _run_command(self, command, tool_name):
        """
        Função auxiliar para executar comandos de forma segura.
        :param command: O comando a ser executado, como uma lista de strings.
        :param tool_name: O nome da ferramenta, para mensagens de erro claras.
        """
        try:
            print(f"    -> Executando {tool_name}...")
            # Executa o comando, não mostra a saída no console (stdout=PIPE),
            # mas captura erros (stderr=PIPE). check=True garante que um erro no comando pare a execução.
            subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"    ✅ {tool_name} concluído.")
        except FileNotFoundError:
            print(f"    ❌ ERRO: '{tool_name}' não foi encontrado. Verifique se ele está instalado e no PATH do sistema.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"    ❌ ERRO: {tool_name} retornou um erro.")
            print(f"    {e.stderr}")
            return False
        return True

    def run_subfinder(self, domain):
        """
        Executa o Subfinder para encontrar subdomínios.
        :param domain: O domínio alvo.
        :return: O caminho para o arquivo de saída ou None em caso de falha.
        """
        output_file = os.path.join(self.output_dir, f"{domain}_subdominios.txt")
        command = ["subfinder", "-d", domain, "-o", output_file]
        
        if self._run_command(command, "Subfinder"):
            # O sort -u é automaticamente tratado pelo subfinder, então não é mais necessário.
            return output_file
        return None

    def run_httpx(self, subdomains_file):
        """
        Executa o Httpx para validar quais subdomínios estão ativos.
        :param subdomains_file: O arquivo de entrada com a lista de subdomínios.
        :return: O caminho para o arquivo de saída ou None em caso de falha.
        """
        domain_base = os.path.basename(subdomains_file).replace('_subdominios.txt', '')
        output_file = os.path.join(self.output_dir, f"{domain_base}_validos.txt")
        command = ["httpx", "-l", subdomains_file, "-silent", "-o", output_file]

        if self._run_command(command, "Httpx"):
            return output_file
        return None

    def run_katana(self, valid_hosts_file):
        """
        Executa o Katana para encontrar URLs nos hosts ativos.
        :param valid_hosts_file: O arquivo de entrada com os hosts válidos.
        :return: O caminho para o arquivo de saída ou None em caso de falha.
        """
        domain_base = os.path.basename(valid_hosts_file).replace('_validos.txt', '')
        output_file = os.path.join(self.output_dir, f"{domain_base}_online.txt")
        command = ["katana", "-l", valid_hosts_file, "-silent", "-o", output_file]

        if self._run_command(command, "Katana"):
            return output_file
        return None