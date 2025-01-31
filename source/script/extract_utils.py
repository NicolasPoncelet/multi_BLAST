from pathlib import Path
import pandas as pd
import numpy as np

def get_extracted_seqs(report_path):
    """Génère les chemins des séquences à extraire."""

    analysis_dir:Path = Path(report_path).parent.parent

    df = pd.read_csv(report_path)
    df = df.dropna(subset=["sstart", "send"])
    df["sstart"] = df["sstart"].astype(int)
    df["send"] = df["send"].astype(int)
    df["sseqid"] = df["sseqid"].str.replace("Scaffold:", "Scaffold_")
    df["Query"] = df["Query"].str.replace("_out_blast", "")
    
    # Gestion du brin négatif
    df["start"] = np.minimum(df["sstart"], df["send"])
    df["end"] = np.maximum(df["sstart"], df["send"])
    df["strand"] = np.where(df["sstart"] > df["send"], "minus", "plus") 
    
    # Regoupement des coordonnées par Assemblage et Brin.
    print(df)
    df_sum = df.groupby(['Assembly','sseqid', 'strand']).agg(
            start=('start', 'min'),
            end=('end', 'max')
    ).reset_index() 
    print(df_sum)

    targets = []
    for _, row in df_sum.iterrows():
        path = (
            f"{analysis_dir}/Extracted_Seqs/"
            f"{row['Assembly']}/"
            f"{row['sseqid']}_{row['start']}-{row['end']}_{row['strand']}.fasta"  
        )
        targets.append(path)
    return targets
