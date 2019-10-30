from pyparsing import *
import glob
import pandas as pd
import os 
import argparse

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
        
        with open(_file, "r", errors = "surrogateescape") as f:

            for line in f.readlines():
        
                # Look for the Project ID 
                if 'Project ID' in line:
                    print(find_project_id(line.strip()))

def find_project_id(line):
    """
    Find the Project ID in a given string line
    """
    return line.split(":")[-1]

def main(folder):

    fileParser(folder)

if __name__ == "__main__":
    
    # Create a parser object 
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default = "./test_folder", type = str,
                       help = "The folder which contains the .txt files that need to be parsed.")
    FLAGS = parser.parse_args()

    main(FLAGS.folder)
