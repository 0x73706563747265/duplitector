import sys, pathlib, hashlib, time

### Declare classes, functions and variables
class FileRecord:
  name: str = None
  size: int = None
  hash: str = None

  def __init__(self, name, size, hash):
    self.name = name
    self.size = size
    self.hash = hash

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return f"Name: {self.name}, Size: {self.size}, Hash: {self.hash}"
  
  def __eq__(self, other):
    if self.size != other.size:
      return False
    else:
      return self.get_hash() == other.get_hash()

  def get_hash(self):
    if self.hash is None:
      bytes = pathlib.Path(self.name).read_bytes()
      readable_hash = hashlib.sha256(bytes).hexdigest()
      self.hash = readable_hash
    return self.hash

def add_duplicate_record(record_1: FileRecord, record_2: FileRecord):
  if record_1.hash not in duplicate_records:
    duplicate_records[record_1.hash] = []
  if record_1.name not in duplicate_records[record_1.hash]:
    duplicate_records[record_1.hash].append(record_1.name)
  if record_2.name not in duplicate_records[record_2.hash]:
    duplicate_records[record_2.hash].append(record_2.name)

# contains all FileRecords for each file found within the target directory
unsorted_records = []
size_records = {}
duplicate_records = {}

### Read argument and parse
if len(sys.argv) != 2:
    raise ValueError('Please provide a single target directory path to search through.')
root_path = pathlib.Path(sys.argv[1])
if not root_path.exists() or not root_path.is_dir():
  raise ValueError("The provided value for a target directory cannot be verified to be a valid directory.")

### Start timer
start = time.time()

### Add each file to unsorted list
print("Searching target directory and sub-directories for files, this may take some time...")
for file in root_path.rglob('*'):
  if file.is_file():
    file_record = FileRecord(str(file.resolve()), file.stat().st_size, None)
    unsorted_records.append(file_record)
unsorted_record_length = len(unsorted_records)
print(f"{unsorted_record_length} records found. Now searching for duplicates...")

### Loop through collected file records and compare with similar size records to find duplicates
time_counter = time.localtime().tm_sec
for index, file_record in enumerate(unsorted_records):
  # Print out a percentage update
  if time_counter != time.localtime().tm_sec:
    print (f"{((index / unsorted_record_length) * 100):.2f}% complete.", end="\r")
    time_counter = time.localtime().tm_sec
  
  # Check for duplicate
  size_string = str(file_record.size)
  if size_string not in size_records:
    # if a file of this size hasn't been found yet, initialise an empty array for it
    size_records[size_string] = []
  else:
    # if one or more file of this size has already been found, compare the hash for each one and add to the duplicate record list if match
    for other_file_record in size_records[size_string]:
      if file_record == other_file_record:
        add_duplicate_record(file_record, other_file_record)
  size_records[size_string].append(file_record)

### Stop timer
end = time.time()

### Print out report
print(f"Duplicate detection complete for {root_path}.")
report_header = f"{unsorted_record_length} records found. {len(duplicate_records)} duplicates detected. Total execution time was {end - start}."
print(report_header)
print("Saving report to report.txt...", end="")

report_contents = f"Total duplicate hashes: {len(duplicate_records)}\n"
for key, value in duplicate_records.items():
  report_contents += f"{key}:\n"
  for record in value:
    report_contents += f"  - {record}\n"
pathlib.Path('report.txt').write_text(report_header + '\n' + report_contents)

print("complete.")