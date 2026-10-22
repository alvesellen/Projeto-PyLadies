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
    # TODO: Exercício 3 - Implemente a filtragem de registros
    return []


def reverse_complement(seq: str) -> str:
    """
    Returns the reverse complement of a DNA sequence.
    Case-preserving (if input is lower, output is lower. If mixed, preserves matching case).
    A <-> T, C <-> G
    """
    # TODO: Exercício 4 - Implemente o reverso complementar
    return ""


def write_fasta(records: list, path: str) -> None:
    """
    Grava uma lista de registros no formato FASTA em um arquivo de saída.
    """
    # TODO: Exercício 5 - Implemente a gravação do FASTA
    pass


def main():
    """
    Interface de linha de comando (CLI) da ferramenta.
    Deve suportar os seguintes argumentos:
    --input: Arquivo FASTA de entrada (obrigatório)
    --output: Arquivo FASTA de saída (obrigatório)
    --min-len: Comprimento mínimo de sequência (opcional, default: 0)
    --min-gc: Conteúdo GC mínimo (opcional, default: 0.0)
    --rev-comp: Flag para aplicar reverso complementar nas sequências mantidas (opcional, flag booleana)
    """
    # TODO: Exercício 5 - Implemente a CLI
    pass


if __name__ == "__main__":
    main()
