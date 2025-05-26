import subprocess
import os
import shutil


def clone_repo(url: str, destination: str) -> None:
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:
        subprocess.run(["git", "clone", url, destination], check=True)
        print(f"Repository cloned to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")


def get_files_in_directory(directory: str) -> list[str]:
    try:
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
        return files
    except FileNotFoundError as e:
        print(f"Directory not found: {e}")
        return []
    except Exception as e:
        print(f"Error accessing directory: {e}")
        return []


def remove_directory(directory: str) -> None:
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print(f"Directory {directory} removed successfully.")
        except Exception as e:
            print(f"Error removing directory: {e}")
    else:
        print(f"Directory {directory} does not exist.")


def get_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


if __name__ == "__main__":
    repo_url = "https://github.com/Oya-Tomo/paper-crawler"
    destination_path = "repo"

    if os.path.exists(destination_path):
        remove_directory(destination_path)

    clone_repo(repo_url, destination_path)
    files = get_files_in_directory(destination_path)
    print(f"Files in {destination_path}:")
    for file in files:
        if file.find(".git") == -1:
            print(file)
            print(get_file_content(file))
