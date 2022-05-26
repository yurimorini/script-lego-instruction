"""Scans an input folder searching for all the PDF files and generates
a structured JSON file containing all the found instruction set.
"""

import json
import os
import subprocess
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
    media = []

    def __init__(self, path: str, media:list[str] = []):
        self.path = str(Path(path).resolve())
        self.fileName = PurePath(path).name
        self.name = PurePath(self.fileName).stem
        parts = self.name.split(" - ")
        self.code = parts[0] 
        self.family = parts[1]
        self.title = "".join(parts[2:])
        self.media = [str(i) for i in media]

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
    _source = None

    # Wrapped file iterator
    _iterator = None

    # Help to generate image files
    _images_generator = None

    def __init__(self, source:str, images):
        self._source = source
        self._images_generator = images
        self._iterator = Path(self._source).glob('*.pdf')

    def __iter__(self):
        for path in self._iterator:
            file = str(path)
            media = self._images_generator.create_media(file)
            yield Instruction(file, media)


class ImagesGenerator:
    """Generates image files from a PDF reference
    and save them in the storage area returning a list of
    file paths.

    Methods
    -------
    create_media(self, file:str)
        Convert the PDF file input to a JPG file in the storage
        folder and return its name in a list. If the file exists
        returns just the file without regenerating it.

    create_folder()
        Ensure base folder exists

    """

    # Defines the paths for the images
    _storage = None

    def __init__(self, storage):
        self._storage = storage

        if not self.converter_exists():
            raise Exception("Image converter \"convert\" does not exists. Install Imagemagick")

    # Create the list of images from the source PDF
    def create_media(self, file:str):
        self.create_folder()

        folder = self._storage.get_media_folder()
        base_name = Path(Path(file).name).stem
        name = f"{base_name}.jpg"
        output = Path(folder / name);

        if not output.is_file():
            subprocess.run([
                "convert", 
                "-density", "300", 
                "-resize", "1000x1000", 
                "-strip", 
                "-flatten",
                "-quality", "100%", 
                "-alpha", "off",
                "-background", "white", 
                f"{file}[0]", f"{output}" 
            ], text=True, check=True)

        return [output]

    # Create the base folder if not exists
    def create_folder(self):
        os.makedirs(
            self._storage.get_media_folder(), 
            exist_ok=True
        )

    # Check the converter software is available in shell
    def converter_exists(self):
        result = subprocess.Popen("convert", shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = result.communicate()[0]
        return result.returncode == 0


class Storage:
    """Helper to manage folder storage from the main storage file

    Methods
    -------
    get_file()
        Returns main path file

    get_media_folder()
        Returns media folder
    """

    # Media folder name
    MEDIA_FOLDER = '.thumbs'

    # Root folder
    _root_folder = None

    # Json outfile
    _outfile = None

    def __init__(self, outfile:str ):
        self._outfile = outfile
        self._root_folder = Path(outfile).parent
        self._media_folder = self._root_folder / self.MEDIA_FOLDER

    def get_file(self):
        return self._outfile

    def get_media_folder(self):
        return self._media_folder

    def save(self, data: str): 
        with open(self.get_file(), 'w') as outfile:
            outfile.write(data)


def parse_options():
    """Parses command line options"""

    import argparse

    parser = argparse.ArgumentParser(description='Generates instruction metadata from files.')
    parser.add_argument('path', help="Source directory for PDF files")
    parser.add_argument('--output', dest="output", default="lego.json", help="JSON output file")

    return parser.parse_args()


def main():
    """Command management"""

    # Parsing options
    args = parse_options()

    # Services
    storage = Storage(args.output)
    pdf_to_images = ImagesGenerator(storage)
    instructions = InstructionGenerator(args.path, pdf_to_images)

    # Print some output info
    print("")
    print("Scanning path: {0}".format(args.path))
    print("Folder:        {0}".format(storage.get_media_folder()))
    print("Output:        {0}".format(storage.get_file()))
    print("")

    # Get list and serialize to JSON
    instruction = [i for i in instructions]
    json_string = json.dumps(instruction, default=vars, indent=2);
    
    # Save file
    storage.save(json_string)

if __name__ == "__main__":
    main()