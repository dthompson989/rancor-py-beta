#!usr/bin/python3.7
"""A Python function that zips up a directory or file, and saves the output in the
   same directory/parent directory. Used primarily with terraform-lambda/ """
import shutil
from pathlib import Path


def zip_dir(zip_input, zip_output):
    try:
        shutil.make_archive(zip_output, 'zip', zip_input)
        print("{} -> has been ZIPPED -> {}".format(zip_input, zip_output))
    except shutil.Error as e:
        print("There was an critical error! ZipUtilError: {}".format(e))
    except TypeError as e:
        print("There was an non-critical error! TypeError: {}".format(e))
    except FileNotFoundError as e:
        print("There was an critical error! FileNotFoundError: {}".format(e))
    return


if __name__ == '__main__':
    """ Main Function. Example input: terraform-lambda/rancor-lambda-payload """
    print("Hello! I will zip a directory or file for you and save a copy in the same parent directory")
    input_dir = input("What is the directory or file you want to ZIP? ")
    output_name = Path.joinpath(Path(input_dir).parent, Path(input_dir).anchor, Path(input_dir).resolve().stem)
    zip_dir(input_dir, output_name)
