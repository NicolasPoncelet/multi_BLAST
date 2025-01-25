import sys
from pathlib import Path
import pandas as pd

def compile(input_directory: str, output_file: str, blast_output_columns: list) -> None:
    """
    Compiles BLAST output files into a single CSV file.

    Parameters
    ----------
    input_dir_path : Path
        Path to the directory containing BLAST output files.
    output_dir_path : Path
        Path to the directory where the compiled CSV file will be saved.
    blast_output_columns : list
        List of column names corresponding to the fields in the BLAST output files.

    Returns
    -------
    None
        Writes a compiled CSV file to the specified output directory.
    """
    print(f'{input_directory=}, {output_file=}, {blast_output_columns=}')
    input_dir_path = Path(input_directory).resolve()
    output_path = Path(output_file).resolve()

    blast_result_files: list[Path] = input_dir_path.rglob("*_out_blast.txt")
    aggregated_results: list[dict] = []

    output_csv_header: list = ["Assembly", "Query"]
    output_csv_header.extend(blast_output_columns)

    for result_file in blast_result_files:
        query_name: str = result_file.stem
        assembly_name: str = result_file.parent.name
        result_record: dict = {"Assembly": assembly_name, "Query": query_name}

        with open(result_file, "r") as infile:

            for line in infile:

                cells = line.strip().split("\t")
                parsed_line = dict(zip(blast_output_columns, cells))
                result_record.update(parsed_line)

            aggregated_results.append(result_record)

    results_dataframe: pd.DataFrame = pd.DataFrame.from_dict(aggregated_results)
    results_dataframe.to_csv(output_path, columns=output_csv_header, index=False)

if __name__ == "__main__":

    input_directory, output_file, blast_output_columns = sys.argv[1], sys.argv[2] , sys.argv[3]

    compile(input_directory, output_file, blast_output_columns)
