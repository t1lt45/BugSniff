# BugSniff (Descoberta de Subdomínios)

BugSniff é uma ferramenta de automação para a fase inicial de reconhecimento em programas de Bug Bounty e pentests. Esta versão inicial foca em duas tarefas essenciais: descobrir subdomínios de forma massiva e validar quais deles estão realmente ativos e respondendo na web.

A ferramenta foi projetada para ser leve, rápida e a base para fases futuras de reconhecimento, como a descoberta de diretórios (fuzzing).

## Funcionalidades

-   **Enumeração de Subdomínios:** Utiliza o **Subfinder** para descobrir subdomínios de uma lista de alvos.
-   **Enriquecimento com API (Opcional):** Permite o uso de uma chave da API do **Shodan** para obter resultados de subdomínios ainda mais completos e precisos.
-   **Validação de Hosts Ativos:** Utiliza o **Httpx** para verificar quais dos subdomínios encontrados estão respondendo em portas HTTP/HTTPS.
-   **Saída Limpa:** Gera um único arquivo final (`subdominios_ativos_final.txt`) contendo a lista limpa de subdomínios ativos, pronta para ser usada como entrada em outras ferramentas.

## Pré-requisitos (IMPORTANTE)

Para que o BugSniff funcione, você **PRECISA** ter as seguintes ferramentas Go instaladas e configuradas no `PATH` do seu sistema. O Python 3.6+ também é necessário.

**1. Go (Linguagem de Programação)**
   - Verifique se o Go está instalado: `go version`
   - Se não estiver, siga o guia de instalação oficial: [https://golang.org/doc/install](https://golang.org/doc/install)
   - Lembre-se de configurar as variáveis de ambiente (`GOPATH`, `GOBIN`) corretamente.

**2. Python 3.6+**
   - Verifique a versão: `python3 --version`

**3. Ferramentas da ProjectDiscovery**
   - Execute os seguintes comandos no seu terminal para instalar o `subfinder` e o `httpx`:

   ```bash
   go install -v [github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest](https://github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest)
   go install -v [github.com/projectdiscovery/httpx/cmd/httpx@latest](https://github.com/projectdiscovery/httpx/cmd/httpx@latest)
   ```
   - Após a instalação, feche e reabra seu terminal e verifique se as ferramentas são reconhecidas:
   ```bash
   subfinder -h
   httpx -h
   ```

## Instalação

Nenhuma instalação de pacotes Python é necessária. Apenas clone ou baixe os arquivos deste projeto.

```bash
git clone <url_do_seu_repositorio>
cd <nome_do_repositorio>
```

## Como Usar

A ferramenta é executada via linha de comando. Você precisa fornecer um arquivo de texto com os domínios que deseja analisar.

**Sintaxe:**
```bash
python3 main.py -l <arquivo_de_dominios.txt> [opções]
```

### Argumentos

| Argumento Curto | Argumento Longo | Descrição                                                                                                 | Obrigatório |
| :-------------- | :-------------- | :-------------------------------------------------------------------------------------------------------- | :---------- |
| `-l`            | `--list`        | Caminho para o arquivo contendo a lista de domínios (um por linha).                                       | **Sim** |
| `-o`            | `--output`      | Nome da pasta onde os resultados serão salvos. (Padrão: `resultados`)                                     | Não         |
| `-sk`           | `--shodan-key`  | Sua chave da API do Shodan para obter melhores resultados de subdomínios.                                   | Não         |

### Exemplos de Uso

**1. Uso Básico (sem API)**

-   Crie um arquivo `dominios.txt`:
    ```txt
    example.com
    google.com
    ```
-   Execute o comando:
    ```bash
    python3 main.py -l dominios.txt -o meus_resultados
    ```

**2. Uso Avançado (com a API do Shodan)**

-   Execute o comando fornecendo sua chave:
    ```bash
    python3 main.py -l dominios.txt -o meus_resultados -sk SUA_CHAVE_API_DO_SHODAN_AQUI
    ```

### Saída

Ao final da execução, uma pasta de saída (ex: `meus_resultados`) será criada. Dentro dela, você encontrará os arquivos intermediários de cada ferramenta e o resultado principal:

-   **`subdominios_ativos_final.txt`**: Um arquivo de texto limpo contendo todos os subdomínios ativos encontrados, prontos para a próxima fase do seu reconhecimento.