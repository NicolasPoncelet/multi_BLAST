from pathlib import Path
import pandas as pd
import numpy as np

def get_extracted_seqs(report_path,config):
    """Génère les chemins des séquences à extraire."""

    analysis_dir:Path = Path(report_path).parent.parent
    df = pd.read_csv(report_path)

    df = df.dropna(subset=["sstart", "send"])

    # Calcul des coordonnées

    df["start"] = np.minimum(df["sstart"], df["send"]).astype(int)
    df["end"] = np.maximum(df["sstart"], df["send"]).astype(int)
    df["strand"] = np.where(df["sstart"] > df["send"], "minus", "plus")
    
    if config["extraction"]["mode"] == "merged":

        # Regoupement des coordonnées par Assemblage et Brin.

        df_sum = df.groupby(['Assembly','sseqid', 'strand']).agg(
                start=('start', 'min'),
                end=('end', 'max')
        ).reset_index() 

        targets = []

        for _, row in df_sum.iterrows():

            path = (
                f"{analysis_dir}/Extracted_Seqs/"
                f"{row['Assembly']}/"
                f"{row['sseqid']}_{row['start']}-{row['end']}_{row['strand']}.fasta"  
            )
            targets.append(path)

        return targets
    
    elif config["extraction"]["mode"] == "individual" :

        group_cols = ['Assembly', 'sseqid', 'strand']

        if config["extraction"]["frame_handling"] in ["sframe", "both"]:
            group_cols.append('sframe')

        if config["extraction"]["frame_handling"] in ["qframe", "both"]:
            group_cols.append('qframe')
            
        df = df.groupby(group_cols).agg(
            start=('start', 'min'),
            end=('end', 'max')
            ).reset_index()
    
        # Génération des paths

        targets = []

        for _, row in df.iterrows():

            frame_info = []

            if config["extraction"]["frame_handling"] in ["sframe", "both"]:
                frame_info.append(f"s{int(row['sframe'])}")
                
            if config["extraction"]["frame_handling"] in ["qframe", "both"]:
                frame_info.append(f"q{int(row['qframe'])}")
                
            frame_str = "_".join(frame_info) if frame_info else ""
            
            path = (
                f"{analysis_dir}/Extracted_Seqs/"
                f"{row['Assembly']}/"
                f"{row['sseqid']}_{row['start']}-{row['end']}_"
                f"{row['strand']}_{frame_str}.fasta"
            )
            targets.append(path)
                
        return targets

    elif config["extraction"]["mode"] == "none" :

        targets = []

        for _, row in df.iterrows():

            path = (
                f"{analysis_dir}/Extracted_Seqs/"
                f"{row['Assembly']}/"
                f"{row['sseqid']}_{row['sstart']}-{row['send']}_{row['strand']}.fasta"  
            )
            targets.append(path)
                
        return targets
# Test

# import yaml

# with open(Path("../config/config.yaml"), "r") as infile:
#     config_yaml = yaml.load(infile, Loader=yaml.SafeLoader)

# report_path = "/home/nponcelet/Documents/03-Script/00_Projet_Perso/02_Bioinfo/42_Multi_BLAST/Test_data/Output/BLAST_results/compiled_results.csv"
# report_path = Path(report_path)

# get_extracted_seqs(report_path,config_yaml)

