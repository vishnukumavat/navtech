import csv
import io

def readInMemoryUploadedCSVFile(file):     
    decoded_file = file.read().decode()
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    dataList = list(reader)
    return dataList