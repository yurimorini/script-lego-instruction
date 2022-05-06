"""Scans an input folder searching for all the PDF files and generates
a structured JSON file containing all the found instruction set.
"""

import json
import sys
from pathlib import PurePath, Path

class Instruction:
    """LEGO instruction file reference.
    
    Given an input path, it create a LEGO instruction entry. It expects 
    an input path as be an absolute file path with its extemsion with 
    the name formatted as "{code} - {family} - {title}". It parse the name 
    splitting it in a set of structured properties.

    Implements a json serializer.

    Attributes
    ----------
    path : str
        original file absolute or relative path
    fileName : str
        file name extracted from the path
    name : str
        name from file name without the extension
    title : int
        instruction set title
    code : int
        instruction set code
    family : int
        instruction set family

    Methods
    -------
    to_json()
        Returns the instruction JSON serialization 
    """

    path = ""
    fileName = ""
    name = ""
    title = ""
    code = ""
    family = ""

    def __init__(self, path: str):
        self.path = str(Path(path).resolve())
        self.fileName = PurePath(path).name
        self.name = PurePath(self.fileName).stem
        parts = self.name.split(" - ")
        self.code = parts[0] 
        self.family = parts[1]
        self.title = "".join(parts[2:])

    def __str__(self):
        return "Title:\"{0}\", Code:\"{1}\", File:\"{2}\"".format(
            self.title, self.code, self.fileName
        )
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)

class InstructionGenerator:
    """Iterate over an instruction directory filtering out only PDF files.
    For every file it generates an instruction structure. 
    """

    # Base path name
    _path = None

    # Wrapped file iterator
    _iterator = None

    def __init__(self, path):
        self._path = path
        self._iterator = Path(self._path).glob('*.pdf')

    def __iter__(self):
        for path in self._iterator:
            file = str(path)
            yield Instruction(file)

def main():
    """Command management"""

    import argparse
    import os

    # Parsing options
    parser = argparse.ArgumentParser(description='Generates instruction metadata from files.')
    parser.add_argument('path', help="Source directory for PDF files")
    parser.add_argument('--output', dest="output", default="lego.json", help="JSON output file")
    args = parser.parse_args()

    # Print some output info
    print("Scanning path: {0}".format(args.path))
    print("Output: {0}".format(args.output))

    # Get list and serialize to JSON
    instruction = [i for i in InstructionGenerator(args.path)]
    json_string = json.dumps(instruction, default=vars, indent=2);
    
    # Save file
    with open(args.output, 'w') as outfile:
        outfile.write(json_string)

if __name__ == "__main__":
    main()
