from pathlib import Path
from itertools import product
import yaml

def all_combinations(*args) -> list[tuple] :

    cartesian_product = list( product(*args))

    return cartesian_product

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

    all_outputs = {}

    # Common output files.

    common_combi:list[tuple] = all_combinations(assemblies_name,queries_name)

    # BLASTN output: make cartesian product for assemblies and queries.

    if config_yaml["blast_type"] == "blastn" :

        blast_db_ext:list[str] = ["nto","ntf","nsq","not","njs","nin","nhr"]

        BLASTN_db_combi = all_combinations(assemblies_name,blast_db_ext)
        
        all_BLASTN_db = [f'{path_to_analysis_dir}/Database_nuc/{assembly_name}.{ext}' for assembly_name, ext in BLASTN_db_combi]
        all_outputs["BLASTN_db"] = all_BLASTN_db

        all_BLASTN_queries = [f'{path_to_analysis_dir}/BLASTN/{assembly_name}/{query}_out_blast.txt' for assembly_name, query in common_combi]
        all_outputs["BLASTN_out"] = all_BLASTN_queries

        all_outputs["final_fasta"] = [f"{path_to_analysis_dir}/Extracted_Seqs/combined.fasta"]
        all_outputs["BLASTN_report"] = [f'{path_to_analysis_dir}/BLAST_results/compiled_results.csv']

    # BLASTX output: make cartesian product for assemblies and queries.

    if config_yaml["blast_type"] == "tblastx" :

        blast_db_ext:list[str] = ["nto","ntf","nsq","not","njs","nin","nhr"]

        BLASTX_db_combi = all_combinations(assemblies_name,blast_db_ext)
        all_BLASTX_db = [f'{path_to_analysis_dir}/Database_nuc/{assembly_name}.{ext}' for assembly_name, ext in BLASTX_db_combi]
        all_outputs["BLASTX_db"] = all_BLASTX_db

        all_BLASTX_queries = [f'{path_to_analysis_dir}/TBLASTX/{assembly_name}/{query}_out_blast.txt' for assembly_name, query in common_combi]
        all_outputs["BLASTX_out"] = all_BLASTX_queries

        all_outputs["final_fasta"] = [f"{path_to_analysis_dir}/Extracted_Seqs/combined.fasta"]
        all_outputs["BLASTX_report"] = [f'{path_to_analysis_dir}/BLAST_results/compiled_results.csv']

    # BLASTX output: make cartesian product for assemblies and queries.

    if config_yaml["blast_type"] == "tblastn" :

        blast_db_ext:list[str] = ["nto","ntf","nsq","not","njs","nin","nhr"]

        TBLASTN_db_combi = all_combinations(assemblies_name,blast_db_ext)
        all_TBLASTN_db = [f'{path_to_analysis_dir}/Database_nuc/{assembly_name}.{ext}' for assembly_name, ext in TBLASTN_db_combi]
        all_outputs["TBLASTN_db"] = all_TBLASTN_db

        all_TBLASTN_queries = [f'{path_to_analysis_dir}/TBLASTN/{assembly_name}/{query}_out_blast.txt' for assembly_name, query in common_combi]
        all_outputs["TBLASTN_out"] = all_TBLASTN_queries

        all_outputs["final_fasta"] = [f"{path_to_analysis_dir}/Extracted_Seqs/combined.fasta"]
        all_outputs["BLASTX_report"] = [f'{path_to_analysis_dir}/BLAST_results/compiled_results.csv']


    return all_outputs

def unpack(final_dict:dict[list[Path]]) -> list[str] :

    flatten_output:list[str] = [str(path) for list in final_dict.values() for path in list]

    return flatten_output

def get() :
    
    output_dic = compile_outputs() 
    
    return unpack(output_dic)

if __name__ == "__main__" :

    get()
