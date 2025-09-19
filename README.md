# BugSniff (ReconFlow Engine)

BugSniff é uma ferramenta de automação para a fase inicial de reconhecimento em programas de Bug Bounty. Ela orquestra ferramentas populares para descobrir subdomínios, validar hosts ativos e extrair URLs, apresentando um resultado final filtrado e pronto para análise.

## Funcionalidades

-   **Enumeração de Subdomínios:** Utiliza o **Subfinder** para descobrir subdomínios de uma lista de alvos.
-   **Validação de Hosts:** Utiliza o **Httpx** para verificar quais subdomínios encontrados estão respondendo em portas HTTP/HTTPS.
-   **Extração de URLs:** Utiliza o **Katana** para navegar (crawl) nos hosts ativos e extrair URLs.
-   **Filtragem Inteligente:** Processa a lista final de URLs para remover conteúdo estático e irrelevante (como `.css`, `.jpg`, `.pdf`, etc.).

## Pré-requisitos (IMPORTANTE)

Para que o BugSniff funcione, você **PRECISA** ter as seguintes ferramentas Go instaladas e configuradas no `PATH` do seu sistema:

1.  **Subfinder**
    -   Instalação: `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`
2.  **Httpx**
    -   Instalação: `go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest`
3.  **Katana**
    -   Instalação: `go install -v github.com/projectdiscovery/katana/cmd/katana@latest`
4.  **Python 3.6+**

## Instalação

Nenhuma instalação de pacotes Python é necessária para a versão atual. Apenas clone ou baixe os arquivos deste projeto:

```bash
git clone <url_do_seu_repositorio>
cd <nome_do_repositorio>
```

## Como Usar

A ferramenta é executada via linha de comando, exigindo um arquivo de texto com a lista de domínios que você deseja analisar.

**Sintaxe:**
```bash
python3 main.py -l <arquivo_de_dominios.txt> -o <pasta_de_saida>
```

**Argumentos:**

-   `-l`, `--list`: **(Obrigatório)** Caminho para o arquivo contendo a lista de domínios, um por linha.
-   `-o`, `--output`: **(Opcional)** Nome da pasta onde os resultados serão salvos. Se não for especificado, será criada uma pasta chamada `resultados`.

**Exemplo de uso:**

1.  Crie um arquivo `dominios.txt`:
    ```txt
    example.com
    google.com
    ```
2.  Execute o BugSniff:
    ```bash
    python3 main.py -l dominios.txt -o meus_resultados
    ```
3.  Ao final da execução, uma pasta `meus_resultados` será criada, contendo os arquivos intermediários de cada ferramenta e o arquivo final `URLs_filtradas.txt`.