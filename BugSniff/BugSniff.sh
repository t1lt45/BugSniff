#!/bin/bash

echo " ****************************************************************************************** ";
echo " ****************************************************************************************** ";
echo " **  ███████████                       █████████              ███     ██████     ██████  ** ";
echo " ** ░░███░░░░░███                     ███░░░░░███            ░░░     ███░░███   ███░░███ ** ";
echo " **  ░███    ░███ █████ ████  ███████░███    ░░░  ████████   ████   ░███ ░░░   ░███ ░░░  ** ";
echo " **  ░██████████ ░░███ ░███  ███░░███░░█████████ ░░███░░███ ░░███  ███████    ███████    ** ";
echo " **  ░███░░░░░███ ░███ ░███ ░███ ░███ ░░░░░░░░███ ░███ ░███  ░███ ░░░███░    ░░░███░     ** ";
echo " **  ░███    ░███ ░███ ░███ ░███ ░███ ███    ░███ ░███ ░███  ░███   ░███       ░███      ** ";
echo " **  ███████████  ░░████████░░███████░░█████████  ████ █████ █████  █████      █████     ** ";
echo " ** ░░░░░░░░░░░    ░░░░░░░░  ░░░░░███ ░░░░░░░░░  ░░░░ ░░░░░ ░░░░░  ░░░░░      ░░░░░      ** ";
echo " **                          ███ ░███                                                    ** ";
echo " **                         ░░██████                                                     ** ";
echo " **                          ░░░░░░                                                      ** ";
echo " **                                                       _     o    ___      ___    __  ** ";
echo " **                                                      |_) \/       | /| |   | |_|(_   ** ";
echo " **                                                      |_) /  o     |  | |__ |   |__)  ** ";
echo " ****************************************************************************************** ";
echo " ****************************************************************************************** ";



# Função de uso
function usage {
    echo "Uso: $0 -l <arquivo_de_dominios>"
    exit 1
}

# Verificando os parâmetros
while getopts ":l:" opt; do
    case $opt in
        l) LISTA_DOMINIOS=$OPTARG ;;
        *) usage ;;
    esac
done

# Verificando se a lista de domínios foi passada
if [ -z "$LISTA_DOMINIOS" ]; then
    usage
fi

# Verificando se o arquivo de domínios existe
if [ ! -f "$LISTA_DOMINIOS" ]; then
    echo "Arquivo de lista de domínios não encontrado!"
    exit 1
fi

# Solicitar o nome da pasta de saída no início
echo "Digite o nome da pasta onde os resultados serão salvos (pressione Enter para usar 'resultados'):"
read OUTPUT_DIR

# Se não for fornecido um nome, use "resultados" como padrão
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="resultados"
fi

# Criando o diretório de saída se não existir
mkdir -p "$OUTPUT_DIR"

# Definindo o nome do arquivo de URLs que será gerado pela função de domínios
URLS_OUTPUT_FILE="$OUTPUT_DIR/purifyURL.txt"

# Função para processar domínios
function processar_dominios {
    while read -r DOMINIO; do
        echo "[*] Processando $DOMINIO..."
        SUBDOMINIOS_ARQUIVO="$OUTPUT_DIR/${DOMINIO}_subdominios.txt"
        VALIDOS_ARQUIVO="$OUTPUT_DIR/${DOMINIO}_validos.txt"
        ONLINE_ARQUIVO="$OUTPUT_DIR/${DOMINIO}_online.txt"

        echo "[*] Buscando subdomínios para $DOMINIO com Subfinder..."
        subfinder -d "$DOMINIO" -o "$SUBDOMINIOS_ARQUIVO"

        echo "[*] Removendo duplicados e organizando subdomínios..."
        sort -u "$SUBDOMINIOS_ARQUIVO" -o "$SUBDOMINIOS_ARQUIVO"

        echo "[*] Validando subdomínios com Httpx..."
        cat "$SUBDOMINIOS_ARQUIVO" | httpx -silent -o "$VALIDOS_ARQUIVO"

        echo "[*] Verificando subdomínios online com Katana..."
        cat "$VALIDOS_ARQUIVO" | katana -silent -o "$ONLINE_ARQUIVO"

        echo "[*] Resultados para $DOMINIO:"
        echo "Subdomínios encontrados: $SUBDOMINIOS_ARQUIVO"
        echo "Subdomínios válidos: $VALIDOS_ARQUIVO"
        echo "Subdomínios online: $ONLINE_ARQUIVO"
        echo ""

        # Adiciona o resultado dos online ao arquivo de URLs
        cat "$ONLINE_ARQUIVO" >> "$URLS_OUTPUT_FILE"

        # Pausa para garantir o tempo de execução do processo
        sleep 2
    done < "$LISTA_DOMINIOS"
}

# Função para filtrar as URLs
function processar_urls {
    echo "[*] Filtrando URLs e salvando no arquivo final..."

    # Limpa o arquivo de saída anterior, se existir
    TEMP_FILE="${OUTPUT_DIR}/temp_purifyURL.txt"
    > "$TEMP_FILE"

    # Processa o arquivo gerado anteriormente pela função de domínios
    cat "$URLS_OUTPUT_FILE" | egrep -a -v '\.css|\.avif|\.svg|\.csv|\.woff2|\.xml|\.png|\.jpg|\.jpeg|\.ico|\.woff|\.doc|\.txt|\.pdf|archiv\.org' > "$TEMP_FILE"

    # Substitui o arquivo de saída pelo filtrado
    mv "$TEMP_FILE" "$URLS_OUTPUT_FILE"

    echo "URLs filtradas salvas no arquivo '$URLS_OUTPUT_FILE'."
}

# Executa as funções em sequência
processar_dominios
processar_urls

echo "[*] Todas as tarefas foram concluídas!"
