# =====================================================================
# COMO EXECUTAR TODOS OS TESTES (ALUNO):
# No terminal (com ambiente virtual ativo), execute:
#     pytest test_fastatool.py
# =====================================================================
import os
import importlib
import sys
import subprocess
from fastatool import main

pytest = importlib.import_module("pytest")
from fastatool import read_fasta, calc_gc, filter_fasta, reverse_complement, write_fasta

# =====================================================================
# EXERCÍCIO 1: Testes Completos Fornecidos (Onboarding)
# Objetivo: Apenas faça o código passar por esses testes.
# =====================================================================

def test_read_fasta_valid_single_line(tmp_path):
    # Cria arquivo FASTA temporário de linha única
    fasta_content = ">seq1\nATGC\n>seq2\nCGTA\n"
    fasta_file = tmp_path / "test_simple.fasta"
    fasta_file.write_text(fasta_content)
    
    records = read_fasta(str(fasta_file))
    
    assert len(records) == 2
    assert records[0] == {"id": "seq1", "seq": "ATGC"}
    assert records[1] == {"id": "seq2", "seq": "CGTA"}


def test_read_fasta_valid_multi_line(tmp_path):
    # Cria arquivo FASTA temporário com quebras de linha na sequência e linhas vazias
    fasta_content = "\n>seq1\nATGC\nTTAA\n\n>seq2\nCG\nTA\n"
    fasta_file = tmp_path / "test_multi.fasta"
    fasta_file.write_text(fasta_content)
    
    records = read_fasta(str(fasta_file))
    
    assert len(records) == 2
    assert records[0] == {"id": "seq1", "seq": "ATGCTTAA"}
    assert records[1] == {"id": "seq2", "seq": "CGTA"}


def test_read_fasta_invalid_format(tmp_path):
    # Arquivo que não começa com ">" deve levantar ValueError
    bad_content = "INVALID LINE\n>seq1\nATGC\n"
    bad_file = tmp_path / "bad.fasta"
    bad_file.write_text(bad_content)
    
    with pytest.raises(ValueError):
        read_fasta(str(bad_file))


# =====================================================================
# EXERCÍCIO 2: Testes Parciais (Cálculo de GC)
# Objetivo: Complete a lacuna do teste e depois escreva o código correspondente.
# =====================================================================

def test_calc_gc_standard():
    # Teste básico de cálculo
    assert calc_gc("ATGC") == 50.0
    assert calc_gc("GGCC") == 100.0
    assert calc_gc("AATT") == 0.0


def test_calc_gc_case_and_ambiguous():
    # TODO: Exercício 2 - Complete o teste abaixo substituindo as lacunas (______)
    # 1. Garanta que calc_gc lida com minúsculas ("atgc" -> 50.0)
    assert calc_gc("atgc") == 50.0
    
    # 2. Garanta que caracteres ambíguos (N, X) são desconsiderados no denominador
    # "ATGC-NNN" ou "ATGCN" -> ATGC tem 4 bases, sendo G e C 2 delas. Total deve ser 50.0%
    # Substitua a lacuna pela asserção correta:
    assert calc_gc("ATGCNNN") == 50.0


# =====================================================================
# EXERCÍCIO 3: Testes Parciais (Filtragem)
# Objetivo: Escreva você mesmo os casos de teste que faltam!
# =====================================================================

def test_filter_fasta_by_length():
    records = [
        {"id": "seq1", "seq": "ATGC"},        # len = 4
        {"id": "seq2", "seq": "ATGCTTAA"},    # len = 8
        {"id": "seq3", "seq": "A"},           # len = 1
    ]
    # Filtra apenas por comprimento mínimo de 4
    filtered = filter_fasta(records, min_len=4)
    assert len(filtered) == 2
    assert filtered[0]["id"] == "seq1"
    assert filtered[1]["id"] == "seq2"


def test_filter_fasta_by_gc_and_length():
    # TODO: Exercício 3 - Escreva um teste que filtra registros por min_gc e min_len simulando múltiplos critérios.
    # Exemplo de records para testar:
    records = [
        {"id": "high_gc", "seq": "GCGC"},  # len = 4, GC = 100%
        {"id": "low_gc", "seq": "ATAT"},   # len = 4, GC = 0%
        {"id": "mid_gc_long", "seq": "ATGCATGC"}, # len = 8, GC = 50%
    ]
    # Escreva suas asserções abaixo para garantir que o filtro funciona!
    filtered = filter_fasta(records, min_len=4, min_gc=40.0)
    assert len(filtered) == 2
    assert filtered[0]["id"] == "high_gc"
    assert filtered[1]["id"] == "mid_gc_long"




def test_cli_integration(tmp_path, monkeypatch):
    entrada = tmp_path / "in.fasta"
    saida = tmp_path / "out.fasta"
    entrada.write_text(">s1\nATGC\n>s2\nA\n>s3\nGGCC\n")

    monkeypatch.setattr(sys, "argv", [
        "fastatool.py", "--input", str(entrada), "--output", str(saida),
        "--min-len", "4",
    ])
    main()

    assert saida.read_text() == ">s1\nATGC\n>s3\nGGCC\n"


def test_cli_rev_comp_and_min_gc(tmp_path, monkeypatch):
    entrada = tmp_path / "in.fasta"
    saida = tmp_path / "out.fasta"
    entrada.write_text(">baixo\nATAT\n>alto\nGGCA\n")

    monkeypatch.setattr(sys, "argv", [
        "fastatool.py", "--input", str(entrada), "--output", str(saida),
        "--min-gc", "50", "--rev-comp",
    ])
    main()

    # só "alto" passa no filtro; GGCA -> reverso complementar = TGCC
    assert saida.read_text() == ">alto\nTGCC\n"


def test_cli_missing_required_args():
    resultado = subprocess.run(
        [sys.executable, "fastatool.py", "--input", "x.fasta"],
        capture_output=True, text=True,
    )
    assert resultado.returncode != 0
    assert "--output" in resultado.stderr