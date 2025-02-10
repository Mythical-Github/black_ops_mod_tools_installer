import os
import sys
import shutil
import hashlib
from pathlib import Path

import requests


SCRIPT_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def get_sha_256_hash(file_path: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return f"File not found: {file_path}"


def get_all_files_in_tree(directory: str) -> list[str]:
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def download_file(url: str, destination: str) -> bool:
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        return True
    except requests.exceptions.RequestException:
        return False


def calculate_sha256(file_path) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {e}"


def attempt_hash_verified_download_from_download_links(
        executable: str,
        sha_256_hash: str,
        download_links: list[str],
        output_directory: str
    ) -> bool:

    download_success = False

    path_to_dependency = os.path.normpath(f'{output_directory}/{sha_256_hash}/{executable}')

    os.makedirs(os.path.dirname(path_to_dependency), exist_ok=True)

    if os.path.isfile(path_to_dependency):
        os.remove(path_to_dependency)

    for download_link in download_links:
        if download_file(download_link, path_to_dependency):
            if calculate_sha256(path_to_dependency) == sha_256_hash:
                download_success = True
                break
            else:
                os.remove(path_to_dependency)

    if not download_success:
        raise Warning(f"Dependency {executable} could not be downloaded or verified.")

    return download_success


def is_exe():
    return getattr(sys, "frozen", False)


def zip_directory(directory, output_zip):
    shutil.make_archive(output_zip.rstrip('.zip'), 'zip', directory)
