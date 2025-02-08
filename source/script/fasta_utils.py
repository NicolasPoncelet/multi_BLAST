from pathlib import Path

def combine_fasta(list_of_fasta:list,output_file:str) -> None :

    fasta_to_combine:list[Path] =[Path(file) for file in list_of_fasta]

    for file in fasta_to_combine :

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
            
