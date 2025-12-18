import glob
import csv
import os
import sys

# Force UTF-8 for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

files = glob.glob(r"C:\Users\Luc\MediXLM\BE\kg\*.csv")
for f in files:
    try:
        with open(f, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            print(f"File: {os.path.basename(f)}")
            print(f"Headers: {headers}")
            print("-" * 20)
    except Exception as e:
        print(f"Error reading {f}: {e}")
