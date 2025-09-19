# url_processor.py
class URLProcessor:
    def __init__(self):
        self.blacklisted_extensions = (
            '.css', '.avif', '.svg', '.csv', '.woff2', '.xml', 
            '.png', '.jpg', '.jpeg', '.ico', '.woff', '.doc', 
            '.txt', '.pdf'
        )
        self.blacklisted_domains = ('archive.org',)

    def filter_urls(self, url_list):
        """
        Filtra uma lista de URLs, removendo aquelas com extensões e domínios indesejados.
        :param url_list: Lista de URLs para filtrar.
        :return: Uma nova lista contendo apenas as URLs filtradas.
        """
        print("[*] Filtrando URLs encontradas...")
        filtered = []
        for url in url_list:
            # Verifica se a URL termina com alguma das extensões da blacklist
            if not url.lower().endswith(self.blacklisted_extensions):
                # Verifica se a URL não contém nenhum dos domínios da blacklist
                if not any(domain in url for domain in self.blacklisted_domains):
                    filtered.append(url)
        
        print(f"    ✅ Filtragem concluída. {len(filtered)} de {len(url_list)} URLs mantidas.")
        return filtered