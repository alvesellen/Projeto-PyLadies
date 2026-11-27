#!/usr/bin/env python3
"""
fastatool.py - Ferramenta de manipulação de arquivos FASTA.
Atividade prática do Dia 1
"""

import sys
import argparse


def read_fasta(path:str)-> list:
    lista_fasta =[]
    dicionario_atual = None

    with open(path, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha =="":
                continue 
                
            if linha.startswith(">"):
                    if dicionario_atual:
                        lista_fasta.append(dicionario_atual)
                    dicionario_atual = {"id": linha[1:], "seq": ""}
            
            
            else:
                if dicionario_atual:
                   dicionario_atual["seq"]+=linha
                else:
                    raise ValueError
            

        if dicionario_atual:
            lista_fasta.append(dicionario_atual)
    return lista_fasta
    pass

def calc_gc(seq: str) -> float:
    
    seq2 = seq.lower()
   
    if "a" not in seq2 and "t" not in seq2 and "c" not in seq2 and "g" not in seq2:
        return 0.0
    else: 
        seq_atgc = seq2.count("a") + seq2.count("g") +seq2.count("t") +seq2.count("c")

        quantidade_g = seq2.count("g")
        quantidade_c = seq2.count("c")

        total_gc = quantidade_c + quantidade_g
        percentagem_gc = (total_gc/seq_atgc)*100

        return percentagem_gc

    
def filter_fasta(records: list, min_len: int = 0, min_gc: float = 0.0) -> list:
    """
    Filtra os registros por comprimento mínimo e conteúdo GC mínimo.
    """
    lista_filtrada = []

    for registo in records:
        sequencia = registo["seq"]

        comprimento = len(sequencia)
        gc = calc_gc(sequencia)

        if comprimento >= min_len and gc >= min_gc:
            lista_filtrada.append(registo)

    return lista_filtrada
    

def reverse_complement(seq: str) -> str:
    tabela = str.maketrans("ATGCatgc", "TACGtacg")
    return seq.translate(tabela)[::-1]


def write_fasta(records: list, path: str) -> None:
    with open(path, "w") as arquivo:
        for registo in records:
            arquivo.write(f">{registo['id']}\n")
            arquivo.write(f"{registo['seq']}\n")


def main():
    parser = argparse.ArgumentParser(description="Ferramenta de manipulação de ficheiros FASTA.")
    parser.add_argument("--input", required=True, help="Ficheiro FASTA de entrada")
    parser.add_argument("--output", required=True, help="Ficheiro FASTA de saída")
    parser.add_argument("--min-len", type=int, default=0, help="Comprimento mínimo da sequência")
    parser.add_argument("--min-gc", type=float, default=0.0, help="Conteúdo GC mínimo (%%)")
    parser.add_argument("--rev-comp", action="store_true", help="Aplicar reverso complementar")
    args = parser.parse_args()

    records = read_fasta(args.input)
    filtrados = filter_fasta(records, min_len=args.min_len, min_gc=args.min_gc)

    if args.rev_comp:
        filtrados = [
            {"id": r["id"], "seq": reverse_complement(r["seq"])}
            for r in filtrados
        ]

    write_fasta(filtrados, args.output)

if __name__ == "__main__":
    main()