"""
Script pra baixar todos os anexos 1 e 2 da ANS
Autor: Matheus Grande Giaretta
"""

import os
import requests as req
from zipfile import ZipFile
from urllib.parse import urljoin
from bs4 import BeautifulSoup

PASTA_DESTINO = "anexos"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def baixar_pdfs(url, pasta=PASTA_DESTINO):
    """
    Função principal que faz o trabalho pesado:
    1. Acessa a página da ANS
    2. Procura os links de PDF
    3. Baixa tudo de forma organizada
    4. Junta em um ZIP
    """
    
    # Cria a pasta se ela ainda não existir
    os.makedirs(pasta, exist_ok=True)
    
    print(f"\nIniciando scraping da página: {url}")
    
    try:
        # Tenta acessar a página
        resposta = req.get(
            url, 
            headers={"User-Agent": USER_AGENT},
            timeout=30
        )
        resposta.raise_for_status()  # Se der erro, levanta uma exceção
        
    except Exception as e:
        print(f"\nFalha ao acessar a página: {e}")
        return False

    # Aqui o codigo comeca a procurar procura os PDFs
    soup = BeautifulSoup(resposta.text, "html.parser")
    link_pdf = []
    
    print("\nProcurando anexos PDF na página...")
    
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        
        # Baixa só PDFs que parecem ser anexos
        if href.endswith(".pdf") and "anexo" in href:
            link_completo = urljoin(url, link["href"])
            link_pdf.append(link_completo)
    
    if not link_pdf:
        print("\nNenhum anexo PDF encontrado!")
        return False
    
    print(f"\n{len(link_pdf)} anexos encontrados. baixando:")
    
    # Baixa cada PDF encontrado
    arquivos_baixados = []
    for i, pdf_url in enumerate(link_pdf, 1):
        try:
            nome_arquivo = os.path.join(pasta, f"anexo_{i}.pdf")
            
            print(f"  -> Baixando {os.path.basename(pdf_url)}...", end=" ")
            
            resposta_pdf = req.get(
                pdf_url,
                headers={"User-Agent": USER_AGENT},
                timeout=60
            )
            resposta_pdf.raise_for_status()
            
            with open(nome_arquivo, "wb") as f:
                f.write(resposta_pdf.content)
                
            arquivos_baixados.append(nome_arquivo)
            print("OK!")
            
        except Exception as e:
            print(f"Falha! Erro: {e}")
            continue
    
    if not arquivos_baixados:
        print("\n[!] Falha ai baixar os arquivos!")
        return False
    
    # Compacta tudo em um ZIP organizado
    print("\nCompactando os anexos...")
    caminho_pdf = "anexos_ans.zip"
    
    try:
        with ZipFile(caminho_pdf, "w") as zipf:
            for arquivo in arquivos_baixados:
                zipf.write(arquivo, os.path.basename(arquivo))
        
        print(f"\nConcluído! Arquivos salvos em:")
        print(f"    - Pasta: {pasta}")
        print(f"    - ZIP: {caminho_pdf}")
        
        return True
        
    except Exception as e:
        print(f"\nFalha ao criar ZIP: {e}")
        return False


if __name__ == "__main__":
    # URL
    URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    baixar_pdfs(URL_ANS)