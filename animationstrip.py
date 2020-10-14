#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#Copyright (c) 2020, George Tokmaji

#Permission to use, copy, modify, and/or distribute this software for any
#purpose with or without fee is hereby granted, provided that the above
#copyright notice and this permission notice appear in all copies.

#THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

def process(file : str, output : str, overwrite : bool = False):
    reader = PdfFileReader(file)
    writer = PdfFileWriter()
    last = -1

    for number in reader.trailer["/Root"]["/PageLabels"]["/Nums"][2::2]:
        last = number
        writer.addPage(reader.pages[number - 1])

    # TODO: needed?
    lastPage = len(reader.pages)
    if last != lastPage:
        writer.addPage(reader.pages[-1])

    with open(output, "wb" if overwrite else "xb") as fobj:
        writer.write(fobj)

if __name__ == "__main__":
    import argparse
    from errno import EEXIST, ENOENT
    
    parser = argparse.ArgumentParser(description="Strips LaTeX beamer animations from PDFs, leaving only the last slide per group.")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file. if not specified, the input file gets overwritten", nargs="?")
    parser.add_argument("-f", help="overwrite existing output files", action="store_true", dest="overwrite")
    parser.add_argument("-v", help="verbose output", action="store_const", dest="log", const=lambda *args, **kwargs: print(*args, **kwargs), default=lambda *args, **kwargs: None)

    result = parser.parse_args()
    outputFile = result.output or result.input
    result.log(result.input, "->", outputFile)
    try:
        process(result.input, outputFile, result.overwrite or not result.output)
    except FileNotFoundError as e:
        result.log("Error:", result.input, "not found!", file=sys.stderr)
        sys.exit(ENOENT)
    except FileExistsError:
        result.log("Error:", outputFile, "already exists!", file=sys.stderr)
        sys.exit(EEXIST)
    except OSError as e:
        result.log(e.strerror)
        sys.exit(e.errno)

    sys.exit(0)
