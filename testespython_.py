def filter_fasta(records: list, min_len: int = 0, min_gc: float = 0.0) -> list:
    """
    Filtra os registros por comprimento mínimo e conteúdo GC mínimo.
    """
    # TODO: Exercício 3 - Implemente a filtragem de registros
    
    listFasta = ()

    for listFasta in records:
        print(listFasta)
       
    
    return []

registos = [
    {"id": "Seq1", "seq": "ATGC"},
    {"id": "Seq2", "seq": "GGCC"},
    {"id": "Seq3", "seq": "AAAA"}
]

for listFasta in registos:
        print(listFasta)
