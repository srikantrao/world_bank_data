from pyparsing import *
import glob
import pandas as pd
import os 
import argparse
from collections import defaultdict
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors="surrogateescape", line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, errors="surrogateescape", line_buffering=True)


def fileParser(folder):


    txt_files = glob.glob(f"{folder}/*.txt")
    compiled_df = pd.DataFrame(columns=['Project ID', 'Project Objectives', 'Project Description',
                                        'Borrowers Institutional Capacity for Safeguard Management',
                                        'Environmental and Social Safeguards Specialists on the Team',
                                        'Environmental Assessment OP/BP 4.01  Triggered ?',
                                        'Environmental Assessment OP/BP 4.01 Comment',
                                        'Natural Habitats OP/BP 4.04', 'NH Comment', 'Forests OP/BP 4.36',
                                        'F Comment','Pest Management OP 4.09', 'PM Comment',
                                        'Physical Cultural Resources OP/BP 4.11', 'PCR Comment',
                                        'Indigenous Peoples OP/BP 4.10', 'IP Comment',
                                        'Involuntary Resettlement OP/BP 4.12', 'IR Comment', 'Safety of Dams OP/BP 4.37',
                                        'SoD Comment', 'Projects in Disputed Areas OP/BP 7.60', 'PiDA Comment'])
    
    for _file in txt_files:

        print(f"Parsing the file: {_file}")

        # Set the project stage to 0
        project_stage = 0

        # project_stage = 0 means that it is looking for project_id
        # project_stage = 1 means that it is looking for project objectives
        # project_stage = 2 means that it is looking for project description
        # project_stage = 3 means that it is looking for specialists on the team
        # project_stage = 4 TBD

        # Create a bunch of flags to use
        proj_id_flag = False
        proj_obj_flag = False
        proj_desc_flag = False


        objective_string = ""
        desc_string = ""

        # Create a default dict to capture all the entries for this particular file
        entry = defaultdict(str)
        
        with open(_file, "r", errors = "surrogateescape") as f:

            for line in f.readlines():

                if project_stage == 0:
        
                    # Look for the Project ID
                    if 'Project ID' in line:
                        entry["Project ID"] = find_project_id(line.strip())
                        # Set the flag to true since it has been found
                        project_stage = 1
                        print(entry["Project ID"])

                        continue

                elif project_stage == 1:

                    # Look for the Project Objectives next
                    if not proj_obj_flag and ('Project Objectives' in line or 'Program Objectives' in line):

                        proj_obj_flag = True
                        continue

                    # You are in the phase of looking for the project Objective here
                    if proj_obj_flag:

                        if "Project Description" not in line and "Program Description" not in line:

                            # Add the line to the objective
                            objective_string = objective_string + " " + line.strip()
                            continue

                        else:

                            # Set the observation flag to False
                            proj_obj_flag = False
                            # Set the description flag to True
                            proj_desc_flag = True

                            project_stage = 2
                            continue

                elif project_stage == 2:

                    # Checking now for the Project Description
                    if proj_desc_flag:

                        if "4." not in line and "D." not in line:

                            # Add the line to the objective
                            desc_string = desc_string + " " + line.strip()
                            continue

                        else:
                            # Set the Description flag to False
                            proj_desc_flag = False
                            project_stage = 3
                            continue


        # Setup some debug information to start off with
        # print(f"The project ID: {entry['Project ID']}")
        # print(f"The project Objective is: {objective_string}")
        # print(f"The project Desription is: {desc_string}")

        row = pd.DataFrame([[entry["Project ID"], objective_string, desc_string]],
                     columns=['Project ID', 'Project Objectives', 'Project Description'])

        print(row.head())

        compiled_df = compiled_df.append(row, ignore_index=True)

    for column in compiled_df:
        compiled_df[column] = compiled_df[column].str.encode('utf-8', errors = "surrogateescape")

    # Generate an xls file from the Pandas dataframe
    compiled_df.to_excel("output.xls", header=True, index=False, encoding='utf-8')


def find_project_id(line):
    """
    Find the Project ID in a given string line
    """
    return line.split(":")[-1]


## Different Columns that need to be recovered
#

def main(folder):

    fileParser(folder)

if __name__ == "__main__":
    
    # Create a parser object 
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default = "./text_file_conversion/samples", type = str,
                       help = "The folder which contains the .txt files that need to be parsed.")
    FLAGS = parser.parse_args()

    main(FLAGS.folder)
