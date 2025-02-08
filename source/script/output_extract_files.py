
def generate_output_path(config) -> str:
    """
    Generate the output file path based on the extraction mode and frame handling settings.

    Parameters
    ----------
    config : dict
        A dictionary containing the extraction configuration. Expected keys:
        - "extraction" : dict
            - "mode" : str
                Extraction mode, either "merge" or "individual".
            - "frame_handling" : str, optional
                Frame handling mode, one of "both", "qframe", or "sframe".

    Returns
    -------
    str
        The formatted output file path.

    Examples
    --------
    >>> config = {
    ...     "extraction": {
    ...         "mode": "merge"
    ...     }
    ... }
    >>> generate_output_path(config)
    '{OUTPUT_DIR}/Extracted_Seqs/{assembly}/{sseqid}_{sstart}-{send}_{strand}.fasta'

    >>> config = {
    ...     "extraction": {
    ...         "mode": "individual",
    ...         "frame_handling": "qframe"
    ...     }
    ... }
    >>> generate_output_path(config)
    '{OUTPUT_DIR}/Extracted_Seqs/{assembly}/{sseqid}_{sstart}-{send}_{strand}_{qframe}.fasta'
    """
    
    base_path = "{OUTPUT_DIR}/Extracted_Seqs/{assembly}/{sseqid}_{sstart}-{send}_{strand}"
    
    mode = config["extraction"]["mode"]
    frame_handling = config["extraction"]["frame_handling"]

    if mode in ["merged", "none"]:
        return f"{base_path}.fasta"

    frame_suffix = {
        "both": "{qframe}_{sframe}",
        "qframe": "{qframe}",
        "sframe": "{sframe}"
    }.get(frame_handling, "")

    return f"{base_path}_{frame_suffix}.fasta" if frame_suffix else f"{base_path}.fasta"
