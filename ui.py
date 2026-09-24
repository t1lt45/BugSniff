# ui.py
"""
Camada de apresentação do BugSniff.
Centraliza banner, cores e tabelas para manter recon_flow.py e scanner.py
focados só na lógica de negócio.
"""
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeElapsedColumn
)
from rich import box

try:
    import pyfiglet
    _HAS_FIGLET = True
except ImportError:
    _HAS_FIGLET = False

console = Console()

AUTHOR_TAG = "t1lt45"


def print_banner(version: str = "2.0"):
    if _HAS_FIGLET:
        art = pyfiglet.figlet_format("BugSniff", font="slant")
    else:
        art = "B U G S N I F F\n"

    console.print(Panel.fit(
        f"[bold cyan]{art}[/bold cyan]"
        f"[dim]Recon automatizado para Bug Bounty & Pentest — v{version}[/dim]\n"
        f"[bold magenta]by: {AUTHOR_TAG}[/bold magenta]",
        border_style="cyan",
        box=box.DOUBLE,
    ))


def print_step(msg: str):
    console.print(f"[bold blue][*][/bold blue] {msg}")


def print_ok(msg: str):
    console.print(f"[bold green]✅[/bold green] {msg}")


def print_warn(msg: str):
    console.print(f"[bold yellow]⚠[/bold yellow]  {msg}")


def print_error(msg: str):
    console.print(f"[bold red]❌[/bold red] {msg}")


def make_progress() -> Progress:
    """Barra de progresso padrão usada para acompanhar alvos sendo processados."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    )


def status_color(status_code):
    if status_code is None:
        return "dim"
    code = int(status_code)
    if 200 <= code < 300:
        return "bold green"
    if 300 <= code < 400:
        return "bold yellow"
    if 400 <= code < 500:
        return "bold red"
    return "bold magenta"


def print_results_table(results: list, title: str = "Subdomínios Ativos"):
    """
    results: lista de dicts com chaves: url, status_code, title, webserver, tech
    """
    width = shutil.get_terminal_size((100, 20)).columns
    table = Table(title=f"{title} ({len(results)})", box=box.ROUNDED, expand=width < 100)

    table.add_column("#", style="dim", width=4)
    table.add_column("URL", style="bold cyan", overflow="fold")
    table.add_column("Status", justify="center")
    table.add_column("Título da Página", overflow="fold")
    table.add_column("Servidor/Tech", overflow="fold")

    for i, r in enumerate(results, start=1):
        code = r.get("status_code")
        color = status_color(code)
        table.add_row(
            str(i),
            r.get("url", "-"),
            f"[{color}]{code}[/{color}]" if code is not None else "-",
            (r.get("title") or "-")[:60],
            (r.get("tech") or r.get("webserver") or "-")[:40],
        )

    console.print(table)


def print_url_list(urls: list, title: str = "URLs Descobertas", max_rows: int = 30):
    """
    Lista simples de URLs (usada para o resultado do Katana, que não tem
    status/título/tech como o httpx — é só descoberta de endpoints).
    """
    width = shutil.get_terminal_size((100, 20)).columns
    table = Table(title=f"{title} ({len(urls)})", box=box.SIMPLE, expand=width < 100)
    table.add_column("#", style="dim", width=4)
    table.add_column("URL", style="bold cyan", overflow="fold")

    shown = urls[:max_rows]
    for i, url in enumerate(shown, start=1):
        table.add_row(str(i), url)

    console.print(table)
    if len(urls) > max_rows:
        console.print(f"[dim]... e mais {len(urls) - max_rows} URL(s). Veja o arquivo completo salvo.[/dim]")


def print_summary(total_targets: int, total_active: int, output_dir: str, elapsed: str, crawled: int = None):
    lines = [
        f"[bold]Domínios processados:[/bold] {total_targets}",
        f"[bold]Subdomínios ativos encontrados:[/bold] {total_active}",
    ]
    if crawled is not None:
        lines.append(f"[bold]URLs descobertas pelo Katana (filtradas):[/bold] {crawled}")
    lines.append(f"[bold]Tempo total:[/bold] {elapsed}")
    lines.append(f"[bold]Resultados salvos em:[/bold] {output_dir}/")

    console.print(Panel(
        "\n".join(lines),
        title="[bold green]Resumo da Execução[/bold green]",
        border_style="green",
        box=box.ROUNDED,
    ))
