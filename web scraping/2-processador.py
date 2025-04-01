"""
Script para processamento do Anexo 1
Autor: Matheus Grande Giaretta
"""

import os
import pandas as pd
import pdfplumber
from zipfile import ZipFile

PASTA_ORIGEM = "anexos"
PASTA_DESTINO = "dados_processados"
NOME_PDF = "anexo_1.pdf"
NOME_CSV = "dados_ans.csv"
NOME_ZIP = "Teste_Matheus_Giaretta.zip"

ABREVIACOES = {
    "OD": "Odontologia",
    "AMB": "Ambulatorial"
}

def extrair_tabela(pdf_path):
    """Extrai a tabela do PDF e converte para um DataFrame."""
    dados = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                dados.extend(tabela)
    
    if not dados:
        print("Nenhuma tabela encontrada no PDF.")
        return None
    
    df = pd.DataFrame(dados)
    df = df.dropna(how='all')  # Remove linhas completamente vazias
    
    # Renomeia colunas e substitui abreviações
    df.rename(columns={0: "Procedimento", 1: "Descrição", 2: "OD", 3: "AMB"}, inplace=True)
    df.replace(ABREVIACOES, inplace=True)
    
    return df

def salvar_csv(df, pasta=PASTA_DESTINO, nome_arquivo=NOME_CSV):
    """Salva o DataFrame como um CSV."""
    os.makedirs(pasta, exist_ok=True)
    caminho_csv = os.path.join(pasta, nome_arquivo)
    df.to_csv(caminho_csv, index=False, encoding='utf-8')
    print(f"CSV salvo em: {caminho_csv}")
    return caminho_csv

def compactar_csv(caminho_csv, pasta=PASTA_DESTINO, nome_zip=NOME_ZIP):
    """Compacta o CSV em um arquivo ZIP."""
    caminho_zip = os.path.join(pasta, nome_zip)
    
    with ZipFile(caminho_zip, "w") as zipf:
        zipf.write(caminho_csv, os.path.basename(caminho_csv))
    
    print(f"Arquivo ZIP criado: {caminho_zip}")
    return caminho_zip

if __name__ == "__main__":
    caminho_pdf = os.path.join(PASTA_ORIGEM, NOME_PDF)
    
    if os.path.exists(caminho_pdf):
        df = extrair_tabela(caminho_pdf)
        if df is not None:
            csv_path = salvar_csv(df)
            compactar_csv(csv_path)
    else:
        print(f"Arquivo {caminho_pdf} não encontrado!")
