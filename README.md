# BugSniff
Welcome to BugSniff, a tool focused on organizing and filtering URLs, designed to automate cybersecurity processes and information gathering. BugSniff streamlines data handling, such as cleaning and organizing URLs for educational and offensive security study purposes.

![image](https://github.com/user-attachments/assets/ac1a71eb-533a-41ee-b84e-15d36b6e31ad)


## Dependencies
### To ensure the script works correctly, make sure the following dependencies are installed:

    Bash: Default scripting language in UNIX/Linux systems.

    Subfinder: Used for discovering subdomains of a target domain.

    sort: Organizes and filters results to keep subdomain and URL lists alphabetical and free of duplicates.

    Httpx: Validates and checks active URLs.

    Katana: A web scanner for discovering accessible URLs and potential vulnerabilities.

    egrep: Applies filters and regex for URL filtering.

## Golang
    #Download Golang https://go.dev/dl
    rm -rf /usr/local/go && tar -C /root -xzf go1.22.0.linux-amd64.tar.gz
    export PATH=$PATH:/root/go/bin
    echo "PATH=\$PATH:/root/go/bin" >> /root/.bashrc


## Automation tools
    #Subfinder
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    
    #HTTPX
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

    #Katana
    go install github.com/projectdiscovery/katana/cmd/katana@latest
    
⚠Ensure these dependencies are installed and accessible in the system PATH for proper functionality.⚠



### 1- Clone this repository to your local environment:
``git clone https://github.com/t1lt4s/BugSniff.git``

### 2- Set up an alias to easily run the script from any directory:
``alias BugSniff='bash /caminho/para/seu/BugSniff/BugSniff.sh'``

### 3- Run the script:
``BugSniff``


## Contribution
I'm new to automation and developing BugSniff to learn and grow! Any suggestions, improvements, or feedback are highly appreciated. Join me to make BugSniff even more functional and powerful. 😄


## DISCLAIMER
### "This project is for educational and experimental purposes only. Use it responsibly and only in authorized environments. The developers are not responsible for any misuse."
