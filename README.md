# Generate json lego instruction collection

Local script which transform all the PDF instruction file found in a local directory to a list of JSON file and to an HTML index file with preview screenshot.

The Python script is launched passing the source folder and optionally the out file.

```bash
python main.py /home/media/lego/ --output lego.json
```

Thumbnails are created in a `.thumb` folder in the same path as the output file. The script uses Imagemagick `convert` launching a subprocess. If Imagemagick is not installed, raises an exception.