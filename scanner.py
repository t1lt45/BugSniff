# scanner.py
import subprocess
import os
import json
import shutil

from ui import print_step, print_ok, print_error, print_warn


class Scanner:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _check_tool(self, tool_name):
        if shutil.which(tool_name) is None:
            print_error(
                f"'{tool_name}' não foi encontrado no PATH. "
                f"Instale-o antes de continuar (veja o README)."
            )
            return False
        return True

    def _run_command(self, command, tool_name, env=None):
        if not self._check_tool(command[0]):
            return False
        try:
            print_step(f"Executando {tool_name}...")
            result = subprocess.run(
                command, check=True, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
            )
            print_ok(f"{tool_name} concluído.")
            return result
        except subprocess.CalledProcessError as e:
            print_error(f"{tool_name} retornou um erro.")
            if e.stderr:
                print_warn(e.stderr.strip()[:500])
            return False

    # ------------------------------------------------------------------ #
    # Subfinder
    # ------------------------------------------------------------------ #
    def run_subfinder(self, domain, shodan_key=None):
        """Executa o Subfinder. Usa a chave do Shodan se fornecida."""
        output_file = os.path.join(self.output_dir, f"{domain}_subdominios.txt")
        command = ["subfinder", "-d", domain, "-o", output_file, "-silent"]

        env = None
        if shodan_key:
            print_step("Usando chave da API do Shodan.")
            env = os.environ.copy()
            env["SHODAN_API_KEY"] = shodan_key

        return output_file if self._run_command(command, "Subfinder", env=env) else None

    # ------------------------------------------------------------------ #
    # Httpx (agora em JSON, para trazer status/title/tech)
    # ------------------------------------------------------------------ #
    def run_httpx(self, subdomains_file):
        """
        Executa o Httpx em modo JSON para validar subdomínios ativos e
        coletar metadados úteis (status code, título, tecnologia/servidor).
        Retorna uma lista de dicts.
        """
        if not self._check_tool("httpx"):
            return []

        domain_base = os.path.basename(subdomains_file).replace("_subdominios.txt", "")
        json_output_file = os.path.join(self.output_dir, f"{domain_base}_httpx.jsonl")

        command = [
            "httpx",
            "-l", subdomains_file,
            "-silent",
            "-json",
            "-status-code",
            "-title",
            "-tech-detect",
            "-o", json_output_file,
        ]

        result = self._run_command(command, "Httpx")
        if not result:
            return []

        parsed = []
        if os.path.exists(json_output_file):
            with open(json_output_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    tech = data.get("tech")
                    parsed.append({
                        "url": data.get("url", ""),
                        "status_code": data.get("status_code"),
                        "title": data.get("title", ""),
                        "webserver": data.get("webserver", ""),
                        "tech": ", ".join(tech) if isinstance(tech, list) else tech,
                    })

        # Mantém também um .txt simples (compatibilidade com fases futuras
        # e outras ferramentas que esperam uma lista de URLs por linha).
        txt_output_file = os.path.join(self.output_dir, f"{domain_base}_validos.txt")
        with open(txt_output_file, "w") as f:
            for item in parsed:
                f.write(f"{item['url']}\n")

        return parsed

    # ------------------------------------------------------------------ #
    # Katana (crawler) — roda DEPOIS do httpx, sobre hosts já validados.
    # Não checa se está online (isso é papel do httpx); descobre URLs/
    # endpoints internos de cada host ativo.
    # ------------------------------------------------------------------ #
    def run_katana(self, active_urls_file, depth=2):
        """
        Executa o Katana sobre a lista de URLs já validadas como ativas
        (gerada pelo httpx) para descobrir endpoints internos de cada uma.
        Retorna uma lista de URLs descobertas (sem filtro ainda).
        """
        if not self._check_tool("katana"):
            return []

        if not os.path.exists(active_urls_file) or os.path.getsize(active_urls_file) == 0:
            print_warn("Nenhuma URL ativa para crawlear com o Katana.")
            return []

        output_file = os.path.join(self.output_dir, "katana_urls.txt")
        command = [
            "katana",
            "-list", active_urls_file,
            "-silent",
            "-depth", str(depth),
            "-o", output_file,
        ]

        result = self._run_command(command, "Katana")
        if not result:
            return []

        urls = []
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                urls = [line.strip() for line in f if line.strip()]

        return urls
