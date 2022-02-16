#!usr/bin/python3.7
"""Usage: python3 file-zip.py -h"""
import argparse
import shutil
from pathlib import Path
# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 file-zip.py",
                                 description="This is a tool for zipping up a directory or file. The output is a "
                                             "zipped directory, subdirectory, or file with the same name as the "
                                             "input. Output is placed the same directory location as the input.")
# Add parser arguments
parser.add_argument("-i",
                    "--input",
                    dest="input_dir",
                    required=True,
                    help="REQUIRED. The directory or file you want to ZIP. HINT: Enter the relative path to the target.")
parser.add_argument("-d",
                    "--debug",
                    dest="debug",
                    action="store_true",
                    default=False,
                    help="If set, turns on debugging. The default is False")
# Parse the arguments
args = parser.parse_args()
"""Example: python3 file-zip.py -i db-auditor-tool-terraform/terraform/db-security-and-compliance-tool/modules/main/lambda_payload -d"""


def zip_dir(zip_output):
    try:
        shutil.make_archive(zip_output, 'zip', args.input_dir)
        print(f"{args.input_dir} -> has been ZIPPED -> {zip_output}")
    except shutil.Error as se:
        print(f"ERROR! There was an critical error! ZipUtilError: {se}")
    except TypeError as te:
        print(f"ERROR! There was an non-critical error! TypeError: {te}")
    except FileNotFoundError as fnfe:
        print(f"ERROR! There was a critical error! FileNotFoundError: {fnfe}")
    return


if __name__ == '__main__':
    """ Main Function """
    output_name = Path.joinpath(Path(args.input_dir).parent,
                                Path(args.input_dir).anchor,
                                Path(args.input_dir).resolve().stem)
    if args.debug:
        print(f"DEBUG! __main__: output_name: {output_name} \n\t  input_dir: {args.input_dir}")
    zip_dir(output_name)
