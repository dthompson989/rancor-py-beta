#!usr/bin/python
"""A Python function that zips up a directory. Used with terraform-lambda/ """
import shutil


def zip_dir(zip_input, zip_output):
    shutil.make_archive(zip_output, 'zip', zip_input)
    print("{} -> has been ZIPPED -> {}".format(zip_input, zip_output))
    return


if __name__ == '__main__':
    input_dir = input("What is the directory you want to ZIP? ")
    output_name = input("What is the output ZIP file name?")
    zip_dir(input_dir, output_name)
