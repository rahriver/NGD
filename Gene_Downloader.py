import inspect
from Bio import Entrez
from Bio import Medline
from Bio import SeqIO
from Bio.Seq import Seq
import Bio
import pandas as pd
import re
from time import sleep
from rich.console import Console

# <---------- Visual --------->
def wait(database="database"):

    console = Console()
    console.log(f"[bold cyan]Searching {database}...")

def finished():

    console = Console()
    console.log("[bold green]Finished!")

# <---------- Entrez Access --------->
Entrez.api_key = ''
Entrez.email = ''

# <---------- Functions --------->
def get_pubmed(query):

    wait("pubmed")
    handle = Entrez.esearch(db="pubmed", term=query, retmax="40")
    record = Entrez.read(handle)
    pubmed_ids = record["IdList"]
    post = Entrez.epost("pubmed", id=",".join(pubmed_ids)).read()
    webenv = post["WebEnv"]
    query_key = post["QueryKey"]
    return post, finished()

def translator_fasta(file_name):

    for seq_record in SeqIO.parse(file_name, "fasta"):
        with open("translated.txt", "w") as file:
            file.write(str(seq_record.seq.translate()))
    return "Translated file saved as translated.txt"

def translator_gb(file_name):

    try:
        for seq_record in SeqIO.parse(file_name, "genbank"):
            with open("translated.txt", "w") as file:
                file.write(str(seq_record.seq.translate()))
        return "Translated file saved as translated.txt"

    except Exception as e:
        print(e)
        return "Translated file saved as translated.txt"

def get_gene_info():

    opt = input("Select an option:\n(1) Gene Info\n(2) FASTA File\n(3) Genebank File\n(4) Translate\n\n-> ").lower()
    if opt == "1":
        gene_name = input("Enter a gene name: ")
        wait("gene database")
        gene_search = Entrez.esearch(db="gene", term=gene_name)
        gene_record = Entrez.read(gene_search)
        gene_id = gene_record["IdList"][0]
        gene_info = Entrez.efetch(db="gene", id=gene_id, rttype='fasta', retmode='text')
        finished()
        return gene_info.read()

    elif opt == "2":
        access_num = input('Accession Number: ')
        wait('nucleotide database')

        try:
            gene_seq_fasta = Entrez.efetch(db="nucleotide", id=access_num, rettype="fasta", retmode="text")
            with open("gene.fasta", "w") as file:
                file.write(gene_seq_fasta.read())
            finished()
            print("FASTA file saved as gene.fasta")
        
        except Exception as e:
            return "Invalid accession number!"+"\n"

    elif opt == "3":
        access_num = input('Accession Number: ')
        wait('nucleotide database')

        try:
            gene_seq_gb = Entrez.efetch(db="nucleotide", id=access_num, rettype="gb", retmode="text")
            with open("gene.gb", "w") as file:
                file.write(gene_seq_gb.read())
            return "Genebank file saved as gene.gb", finished()

        except Exception as e:
            return "Invalid accession number!"+"\n"

    elif opt == "4":
        translate = input("Do you want to translate the FASTA file? (y/n)\n-> ").lower()

        if translate == "y":
            file_format = input("Enter the file format: (fasta/gb)\n-> ").lower()
            file_name = input("Enter the file name: ")

            if file_format == "fasta":
                translator_fasta(file_name)

            elif file_format == "gb":
                translator_gb(file_name)

        elif translate == "n":
            pass

    else:
        print("Please enter a valid value!\n")
        return get_gene_info()

# <---------- Initiate --------->
def main():

    while True:
        initiate = input("What do you want to do?\n1: Search in pubmed\n2: Search for a gene\n3: Exit\n\n-> ")

        if initiate == "1":
            query = input("Enter a query: ")
            print(get_pubmed(query))

        elif initiate == "2":
            print(get_gene_info())

        elif initiate == "3":
            print("Bye!")
            break

        else:
            print("Please enter a valid value!\n")
            continue

if __name__ == "__main__":
    main()
