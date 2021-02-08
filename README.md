# Dupicate-File-Finder
 A python based script that finds files with the same content in a given directory.
## Usage
```
python.exe .\find_duplicates.py -h
Usage: find_duplicates.py [options]

A tool to find duplicate files that have the same content

Options:
  -h, --help            show this help message and exit
  -p BASEPATH, --path=BASEPATH
                        Path to start the search from
  -b, --compareBytes    Preform byte by byte comparison instead of md5 hash
                        comparison. used to avoid hash collisions
```
