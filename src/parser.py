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
        projid_label = CaselessLiteral('Project ID') | CaselessLiteral('ProjectID')
        section_label = (Word(srange("[A-Z]")) + Literal('.')) | (Word(nums) + Literal('.'))
        projobj_label = section_label + (CaselessLiteral('Project Objectives') | CaselessLiteral('Program Objectives') |\
                        CaselessLiteral('Project Objective') | CaselessLiteral('Program Objective'))
        projdes_label = section_label + (CaselessLiteral('Project Description') | CaselessLiteral('Program Description'))
        loc_label = section_label + (CaselessLiteral('Project Location') | CaselessLiteral('Program Location'))
        borrow_label = section_label + (CaselessLiteral('Borrow')) + SkipTo('\n')
        envsoc_label = section_label + CaselessLiteral('Environmental and Social') + SkipTo('\n')
        paragraph = SkipTo('\n')
        field = Word(alphanums)
        colon = Word(':')
        end = SkipTo('/n/n')
        parser = projid_label + Optional(colon) + field.setResultsName('projID') + SkipTo(projobj_label) \
                 + projobj_label + SkipTo(projdes_label).setResultsName('projobj') + SkipTo(projdes_label) \
                 + projdes_label + SkipTo(loc_label).setResultsName('projdes') + SkipTo(borrow_label) + \
                 Optional(borrow_label) + Optional(SkipTo(paragraph).setResultsName('borrow'))
        print()
        print()
        print()
        print(_file)

        for param in parser.searchString(open(_file, encoding="utf8", errors='ignore').read()):
            print(param.projID)
            print(param.projobj)
            print(param.projdes)
            print(param.borrow)




        #data = parseString(open(file, encoding="utf8", errors='ignore').read())
        # parser_projID = Regex('([P]\s*[A-Z0-9]{6,6})').setResultsName('projID')
        # parser = Literal('Project ID') + parser_projID  parser_projID.parseString(open(file, encoding="utf8", errors='ignore').read())
        # print(projID)

def main(folder):

    fileParser(folder)

if __name__ == "__main__":
    
    # Create a parser object 
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default = "./test_folder", type = str,
                       help = "The folder which contains the .txt files that need to be parsed.")
    FLAGS = parser.parse_args()

    main(FLAGS.folder)
