import io
import zipfile
import requests

URL = "https://www.ssa.gov/oact/babynames/names.zip"
OUTPUT_FILE = "ssa-baby-names.csv"

# Use a non-browser User-Agent so SSA's firewall allows the download
response = requests.get(URL, headers={"User-Agent": "Wget/1.21.4"}, timeout=60)
response.raise_for_status()

# Open the downloaded zip archive directly from memory
with zipfile.ZipFile(io.BytesIO(response.content)) as zf, open(
    OUTPUT_FILE, "w", encoding="utf-8"
) as out:
    out.write("year,name,sex,count\n")

    # Process each yearly file (e.g., yob1880.txt) in chronological order
    for filename in sorted(zf.namelist()):
        if filename.startswith("yob") and filename.endswith(".txt"):
            year = filename[3:7]  # Extract the 4-digit year from the filename
            text = zf.read(filename).decode("utf-8")
            for line in text.splitlines():
                if line:
                    out.write(f"{year},{line}\n")

print(f"Created {OUTPUT_FILE}")
