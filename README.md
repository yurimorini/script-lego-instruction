# Generate json lego instruction collection

Local script which transform all the PDF instruction file found in a local directory to a list of item in a JSON file and to an HTML index file (TBD) with preview screenshot.

The Python script is launched passing the source folder and optionally the out file.

```bash
python main.py /home/media/lego/ --output lego.json
```

Thumbnails are created in a `.thumb` folder in the same path as the output file. The script uses Imagemagick `convert` launching a subprocess. If Imagemagick is not installed, raises an exception.

Instructions metadata are parsed from the PDF file name. Expected format is the following, minimal expected format is formed just by set name and code.

```text
{code} - {family} - {set name}.pdf
12345 - Classic - Police station.pdf
```

## PWA

Layout folder include a minimal HTML and JS application which try to load the JSON file in a relative path to the index. It renders a simple grid of instruction previews. Search is possible in a dedicated filtering component. It works if loaded within a local folder HTTP server, complete solution not yet implemented.
