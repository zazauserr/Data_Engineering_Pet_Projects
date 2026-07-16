from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_DIR / "config" / "expected_files.txt"


def load_expected_files(config_path):
    expected_files = []

    with open(config_path, "r") as file:
        for line in file:
            filename = line.strip()

            if filename:
                expected_files.append(filename)

    return expected_files


expected_files = load_expected_files(CONFIG_PATH)

def validate_files(raw_directory, expected_files):
    files = []
    raw_directory = Path(raw_directory)
    for filename in expected_files:
        file_path = raw_directory / filename
        name = file_path.name
        exists = file_path.exists()
        if not exists:
            size = None
            status = "Missing"
        else:
            size = file_path.stat().st_size
            if size == 0:
                status = "Empty"
            else:
                status = "OK"

        file_info = {
            "filename": name,
            "exists": exists,
            "size_bytes": size,
            "status": status
        }
        files.append(file_info)
    return files

RAW_DATA_PATH = PROJECT_DIR / "data" / "raw"

results = validate_files(RAW_DATA_PATH, expected_files)
for result in results:
    print(
        f'{result["status"]}: '
        f'{result["filename"]} - '
        f'{result["size_bytes"]} bytes'
    )