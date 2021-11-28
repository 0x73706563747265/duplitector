# Duplitector
Duplitector: A simple Python script to find duplicate files.

# How To Use
Execute the script using Python 3, passing in a single argument which is the path to the target directory to search through.

For example:<br>
`python3 duplitector.py "C:\users\dupliuser\Pictures"`

This will iteratively search through the target directory and every sub-directory. The script keeps track of any duplicate files found, which are then reported at the end in a file named *report.txt* which is generated in the same folder that the script is executed in.

NOTE: This script was tested on a Pictures folder containing ~47,000 files at a size of 190GB. Stability cannot be guaranteed, especially when testing on folders with large contents.

# How It Works
1. The script accepts a target directory which will act as the root directory for searching.
2. The script then searches through the target directory and every single sub-directory, looking for files. For each file found, the absolute file path is recorded along with its size in bytes and a blank hash field.
3. Once all files have been found, this list of files is iterated through to search for duplicates:
    1. Each file record is added to a data structure using its size as a unique identifier.
    2. If a list of file records already exist with the same file size, a hash is computed for any size-matching file record that doesn't already have a cached hash value.
    3. The hashes are then compared to confirm if the files match. If they do, Each file path is added to a new data structure, using the hash as the unique identifier.
    4. Any subsequent duplicates are appended to this record using the same hash.
4. A report is generated, showing every file path where duplicates exist for each hash.

This approach optimises the required computation and time spent. As identical files must have the same size in bytes, it is trivial to initially compare using the reported size and discard records which are different. Only files with matching sizes are then hashed to confirm if they are an exact match. Since only file contents are hashed, files with differing names but matching contents will still be reported.