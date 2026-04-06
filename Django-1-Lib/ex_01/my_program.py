from path import Path


def main():
	folder = Path("my_folder")
	folder.makedirs_p()

	file_path = folder / "my_file.txt"
	file_path.write_text("This file was created by mchliyah with path.py.\n")

	print(file_path.read_text(), end="")


if __name__ == "__main__":
	main()