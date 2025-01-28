from pathlib import Path
import pandas as pd
import numpy as np

def get_extracted_seqs(report_path):
    """Génère les chemins des séquences à extraire."""
    df = pd.read_csv(report_path)
    df = df.dropna(subset=["sstart", "send"])
    df["sstart"] = df["sstart"].astype(int)
    df["send"] = df["send"].astype(int)
    df["sseqid"] = df["sseqid"].str.replace("Scaffold:", "Scaffold_")
    
    # Gestion du brin négatif
    df["start"] = np.minimum(df["sstart"], df["send"])
    df["end"] = np.maximum(df["sstart"], df["send"])
    df["strand"] = np.where(df["sstart"] > df["send"], "minus", "plus") 
    
    targets = []
    for _, row in df.iterrows():
        path = (
            f"{Path(report_path).parent.parent}/Extracted_Seqs/"
            f"{row['Assembly']}/"
            f"{row['sseqid']}_{row['start']}-{row['end']}_{row['strand']}.fasta"  # Inclut le brin
        )
        targets.append(path)

    return targets