# MultiBLAST

## Introduction :books:


<div style="display: flex;">

<div style="flex: 1; padding-right: 10px;">
<p>This repository contains a data processing pipeline using Snakemake to BLAST FASTA files to assemblies.</p>
</div>

<div style="flex: 1;">
<img src="Assets/rulegraph.svg" alt="rulegraph of the pipeline" />
</div>

</div>


## Pipeline Structure :deciduous_tree:

The pipeline includes the following steps:




## Repository structure :open_file_folder:

This repository contains several folders:



## Usage :computer: 

1. Clone this repository:

   ```bash
   git clone git@github.com:NicolasPoncelet/multi_BLAST.git <folder_name>
   cd <folder_name>
   ```
2. Edit config.yaml with the paths to the FASTQ files, references, and output directory.

3. Run the pipeline locally with Snakemake:

    ```bash
    snakemake --cores <core_number>
    ```

## Dependencies :floppy_disk:

- Snakemake **7.32.4**
- Python **3.11.0**



## Road map :dart:


## Authors :envelope:

This project was developed and is maintained by Nponcelet.

## Contributing :earth_americas:

Contributions are welcome. Whether it's reporting issues, suggesting new features, or improving the documentation, feel free to submit a pull request or open an issue. 

## License :pencil:
This repository is licensed under the MIT License. See the LICENSE file for more details.
