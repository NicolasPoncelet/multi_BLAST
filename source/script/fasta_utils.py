from pathlib import Path

def combine_fasta(list_of_fasta:list,output_file:str) -> None :

    #fasta_to_combine:list[Path] =[Path(file) for file in list_of_fasta]
    fasta_to_combine =list_of_fasta


    for file in list_of_fasta :

        with open(file, "r") as infile, open(output_file, "a") as outfile:

            assembly_name = file.parent.name

            for line in infile :

                if line.startswith(">") :

                    original_header = line.replace(">", "").strip()

                    if original_header.endswith('/rc'):
                        original_header = original_header[:-3] 

                    new_header = f'>{assembly_name}_{original_header}\n'

                    outfile.write(new_header)

                else:
                    outfile.write(line)
            
            outfile.write("\n")
            

dir = "/home/nponcelet/Documents/03-Script/00_Projet_Perso/02_Bioinfo/42_Multi_BLAST/Test_data/Output/Extracted_Seqs"
dir = Path(dir).rglob("*/*.fasta")
final = Path()/"test.fasta"

combine_fasta(dir,final)