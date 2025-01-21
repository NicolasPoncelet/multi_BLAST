from pathlib import Path
from itertools import product
import yaml

def compile_outputs() -> dict[str:list[Path]] :

    path_to_yaml:Path = Path('config/config.yaml').resolve()

    with open(path_to_yaml, 'r') as infile:
        config_yaml = yaml.load(infile, Loader=yaml.SafeLoader)
    
    # Get inputs path from yaml file to generate output dict for snakefile.

    path_to_assemblies_dir:Path = Path(config_yaml["assemblies_dir"]).resolve()
    path_to_queries:Path = Path(config_yaml["queries_dir"]).resolve()
    path_to_analysis_dir:Path = Path(config_yaml["analysis_dir"]).resolve()

    queries_name:list[str] = [fasta.stem for fasta in path_to_queries.glob("*.fasta")]
    assemblies_name:list[str] = [fasta.stem for fasta in path_to_assemblies_dir.glob("*.fasta")]

    # Static output in dict:

    # all_outputs:dict[str:[list[Path]]] = {
    #     "reference_report":[f"Ressources/references.csv"],
    #     "fastq_report":[f"Ressources/fastq.csv"]    
    # }
    
    all_outputs = {}

    # Make cartesion product for depth, flagstat, bai output.
    all_combinations = list( product(assemblies_name,queries_name))

    all_blast_out = [f'{path_to_analysis_dir}/BLAST/{assembly_name}/{query}_out_blast.txt' for assembly_name, query in all_combinations]

    all_outputs["blast_out"] = all_blast_out
    
    print("Assemblies:")
    print(assemblies_name)
    print("\nQueries:")
    print(queries_name)
    print("\nCombinations:")
    print(all_combinations)

    return all_outputs

def unpack(final_dict:dict[list[Path]]) -> list[str] :

    flatten_output:list[str] = [str(path) for list in final_dict.values() for path in list]

    return flatten_output

def get() :
    
    output_dic = compile_outputs() 
    
    return unpack(output_dic)

if __name__ == "__main__" :

    get()
