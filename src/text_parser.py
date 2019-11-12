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
                                        'Environmental Assessment OP/BP 4.01',
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
        # project_stage = 3 means that it is looking for environmental assessment
        # project_stage = 4 means that it is looking for natural habitat stuff
        # project_stage = 5 menas that it is looking for forest stuff
        # project_stage = 6 means that it is looking for pest management stuff
        # project_stage = 7 means that it is looking for indigenous people stuff
        # project_stage = 8 means that it is looking for involuntary resettlement
        # project_stage = 9 means that it is looking for safety of dams
        # project_stage = 10 means that it is looking for projects in disputed areas





        # Create a bunch of flags to use
        proj_id_flag = False
        proj_obj_flag = False
        proj_desc_flag = False
        proj_env_assess_flag = False
        proj_nat_habitat_flag = False
        forest_flag  = False
        pest_man_flag = False
        indi_people_flag = False
        inv_settle_flag = False
        safety_dam_flag = False
        disputed_area_flag = False

        objective_string = ""
        desc_string = ""
        env_assess = ""
        nat_habitat = ""
        forest_stuff = ""
        pest_man = ""
        indi_people = ""
        inv_settle = ""
        safety_dam = ""
        disputed_area = ""

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

                # Looking for Environmental Assessment
                elif project_stage == 3:

                    if "Environmental Assessment (OP/BP 4.01)" in line:
                        proj_env_assess_flag = True
                        continue

                    if proj_env_assess_flag:
                        print(f"Length: {len(line)} and contents: {line}")
                        if len(line) == 4 and line[1] == "X":
                            env_assess = "No"
                        elif len(line) == 2 and line[0] == "X":
                            env_assess = "Yes"
                        proj_env_assess_flag = False
                        project_stage = 4

                # Looking for Natural Habitat
                elif project_stage == 4:

                    if "Natural Habitats (OP/BP 4.04)" in line:
                        proj_nat_habitat_flag = True
                        continue

                    if proj_nat_habitat_flag:
                        if len(line) == 4 and line[1] == "X":
                            nat_habitat = "No"
                        elif len(line) == 2 and line[0] == "X":
                            nat_habitat = "Yes"
                        proj_nat_habitat_flag = False
                        project_stage = 5

                # Looking for Forest stuff
                elif project_stage == 5:

                    if 'Forests (OP/BP 4.36)' in line:
                        forest_flag = True
                        continue

                    if forest_flag:
                        if len(line) == 4 and line[1] == "X":
                            forest_stuff = "No"
                        elif len(line) == 2 and line[0] == "X":
                            forest_stuff = "Yes"
                        forest_flag = False
                        project_stage = 6

                # Looking for Pest Management Stuff
                elif project_stage == 6:

                    if 'Pest Management (OP 4.09)' in line:
                        pest_man_flag = True
                        continue

                    if pest_man_flag:
                        if len(line) == 4 and line.strip()[1] == "X":
                            pest_man = "No"
                        elif len(line) == 2 and line[0] == "X":
                            pest_man = "Yes"
                        pest_man_flag = False
                        project_stage = 7

                # Looking for Indigenous people
                elif project_stage == 7:

                    if 'Indigenous Peoples (OD 4.20)' in line:
                        indi_people_flag = True
                        continue

                    if indi_people_flag:
                        print(f"Len: {len(line)} and contents: {line}")
                        if len(line) == 4 and line[1] == "X":
                            indi_people = "No"
                        elif len(line) == 2 and line[0] == "X":
                            indi_people = "Yes"
                        indi_people_flag = False
                        project_stage = 8

                # Looking for Involuntary Resettlement
                elif project_stage == 8:

                    if 'Involuntary Resettlement (OP/BP 4.12)' in line:
                        inv_settle_flag = True
                        continue

                    if inv_settle_flag:
                        if len(line) == 4 and line[1] == "X":
                            inv_settle = "No"
                        elif len(line) == 2 and line[0] == "X":
                            inv_settle = "Yes"
                        inv_settle_flag = False
                        project_stage = 9

                # Looking for Safety of Dams
                elif project_stage == 9:

                    if 'Safety of Dams (OP/BP 4.37)' in line:
                        safety_dam_flag = True
                        continue

                    if safety_dam_flag:
                        if len(line) == 4 and line[1] == "X":
                            safety_dam = "No"
                        elif len(line) == 2 and line[0] == "X":
                            safety_dam = "Yes"
                        safety_dam_flag = False
                        project_stage = 10

                # Looking for Indigenous people
                elif project_stage == 10:

                    if 'Projects in Disputed Areas (OP/BP 7.60)' in line:
                        disputed_area_flag = True
                        continue

                    if disputed_area_flag:
                        if len(line) == 4 and line[1] == "X":
                            disputed_area = "No"
                        elif len(line) == 2 and line[0] == "X":
                            disputed_area = "Yes"
                        disputed_area_flag = False
                        project_stage = 11

                        break







        # Setup some debug information to start off with
        #print(f"The project ID: {entry['Project ID']}")
        #print(f"The project Objective is: {objective_string}")
        #print(f"The project Desription is: {desc_string}")

        row = pd.DataFrame([[entry["Project ID"], objective_string, desc_string, env_assess, nat_habitat, forest_stuff,
                             pest_man, indi_people, inv_settle, safety_dam, disputed_area ]],
                     columns=['Project ID', 'Project Objectives', 'Project Description',
                              'Environmental Assessment OP/BP 4.01', 'Natural Habitats OP/BP 4.04',
                              'Forests OP/BP 4.36', 'Pest Management OP 4.09', 'Indigenous Peoples OP/BP 4.10',
                              'Involuntary Resettlement OP/BP 4.12', 'Safety of Dams OP/BP 4.37',
                              'Projects in Disputed Areas OP/BP 7.60'])


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

    # TODO: Clean up the code - FSM has too many conditional statements.

    # Create a parser object
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default = "../test_folder", type = str,
                       help = "The folder which contains the .txt files that need to be parsed.")
    FLAGS = parser.parse_args()

    main(FLAGS.folder)
