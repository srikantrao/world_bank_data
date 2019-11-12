# Parser to parse files from 7200 to 8400 using the pyparsing module
# Author - Hardeep Sullan

from pyparsing import *
import glob
import pandas as pd
import re
import argparse

def fileParser(folder):

    # Get a list of all the test files in the given folder
    txt_files = glob.glob(f"{folder}/*.txt")

    # Create a dataframe based on the expected final format.
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

    page_rgx  = re.compile('\n[-]\n|\s*(Page)\s*\d*(of)\s*\d*\n*|\s*(Page)\s*\d*\n*|\n(\.)\s\n|\s\n\s|\n\s(?=[a-z])|\n(Public Disclosure Copy)\n*')
    newline_rgx = re.compile('\n(?=[a-z])|\n(?=[(])|\n(?=[1-9])')
    dc = Regex(r'\n[-]\n|\s*(Page)\s*\d*\n*|\n(\.)\s\n|\s\n\s|\n\s(?=[a-z])').sub(r' ')
    line = Regex(r'\n(?=[a-z])|\n(?=[(])|\n(?=[1-9])').sub(r'')
    for _file in txt_files:
        projid_label = Literal('Project ID') ^ Literal('ProjectID') ^ Literal('Project ID:') ^ Literal('ProjectID:')
        section_label = LineStart() + Optional(White(' ',max=50)) + ((Word(srange("[A-Z]")) + Literal('.')) ^ (Word(nums) + Literal('.'))) + \
                        Optional(((Word(srange("[A-Z]")) + Literal('.')) ^ (Word(nums) + Literal('.')))) + \
                        Optional(((Word(srange("[A-Z]")) + Literal('.')) ^ (Word(nums) + Literal('.')))) + \
                        Optional(((Word(srange("[A-Z]")) + Literal('.')) ^ (Word(nums) + Literal('.'))))
        projobj_label = section_label + (CaselessLiteral('Project Objectives') ^ CaselessLiteral('Program Objectives') ^\
                        CaselessLiteral('Project Objective') ^ CaselessLiteral('Program Objective'))
        projdes_label = section_label + (CaselessLiteral('Project Description') ^ CaselessLiteral('Program Description'))
        loc_label = section_label + (CaselessLiteral('Project Location') ^ CaselessLiteral('Program Location'))
        borrow_label = section_label + (CaselessLiteral('Borrow')) + SkipTo('\n')
        envsoc_label = section_label + CaselessLiteral('Environmental and Social Safeguard Specialists') + SkipTo('\n')
        paragraph = SkipTo('\n')
        field = Word(alphanums)
        colon = Word(':')
        end = SkipTo('/n/n')
        #parser = projid_label + Optional(colon) + field.setResultsName('projID')

        parser = projid_label + Optional(colon) + field.setResultsName('projID') + SkipTo(projobj_label) \
                 + projobj_label + Optional(colon) + SkipTo(projdes_label).setResultsName('projobj') + SkipTo(projdes_label) \
                 + projdes_label + Optional(colon) + SkipTo(loc_label).setResultsName('projdes') + \
                 Optional(SkipTo(borrow_label) + borrow_label + SkipTo(section_label).setResultsName('borrow')) + \
                 Optional(SkipTo(envsoc_label) + envsoc_label + SkipTo(section_label).setResultsName('envsoc'))

        print()
        print()
        print()
        print(_file)

        for param in parser.searchString(open(_file, encoding="utf8", errors='ignore').read()):
            param.projobj = re.sub(page_rgx, " ",  param.projobj)
            param.projobj = re.sub(newline_rgx, "", param.projobj)
            param.projdes = re.sub(page_rgx, " ",  param.projdes)
            param.projdes = re.sub(newline_rgx, "", param.projdes)
            param.borrow = re.sub(page_rgx, " ",  param.borrow)
            param.borrow = re.sub(newline_rgx, "", param.borrow)
            #param.borrow = line.transformString(param.borrow)
            print(param.projID)
            print(param.projobj)
            print(param.projdes)
            print(param.borrow)
            print(param.envsoc)
            compiled_df = compiled_df.append({'Project ID': param.projID, 'Project Objectives': param.projobj,
                                              'Project Description': param.projdes,
                                              'Borrowers Institutional Capacity for Safeguard Management': param.borrow,
                                              'Environmental and Social Safeguards Specialists on the Team': param.envsoc}, ignore_index=True)

    print(compiled_df)
    compiled_df.to_csv(folder + 'compiled.csv')




        #data = parseString(open(file, encoding="utf8", errors='ignore').read())
        # parser_projID = Regex('([P]\s*[A-Z0-9]{6,6})').setResultsName('projID')
        # parser = Literal('Project ID') + parser_projID  parser_projID.parseString(open(file, encoding="utf8", errors='ignore').read())
        # print(projID)

def main(folder):

    fileParser(folder)

if __name__ == "__main__":

    # Create a parser object
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default = "../text_file_conversion/samples/", type = str,
                       help = "The folder which contains the .txt files that need to be parsed.")
    FLAGS = parser.parse_args()

    main(FLAGS.folder)
