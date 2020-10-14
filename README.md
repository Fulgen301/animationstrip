# animationstrip
Strips LaTeX beamer animations from PDFs, leaving only the last slide per group.

usage: animationstrip.py [-h] [-f] [-v] input [output]

positional arguments:
  input       input file
  output      output file. if not specified, the input file gets overwritten

optional arguments:
  -h, --help  show this help message and exit
  -f          overwrite existing output files
  -v          verbose output

## Requirements
PyPDF2
