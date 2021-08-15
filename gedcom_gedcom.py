
import re
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from gedcom.element.element import Element
from gedcom.element.family import FamilyElement, NotAnActualFamilyError
from gedcom.element.file import FileElement
from gedcom.element.individual import IndividualElement, NotAnActualIndividualError
from gedcom.element.object import ObjectElement
from gedcom.element.root import RootElement
import gedcom.tags
import sys

# Path to your `.ged` file
file_path = 'C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\Ancestry\SZABOLCS SZEKULESZ.ged'
#file_path = ''

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()

# Iterate through all root child elements
for element in root_child_elements:

    # Is the "element" an actual "IndividualElement"? (Allows usage of extra functions such as "surname_match" and "get_name".)
    if isinstance(element, IndividualElement):

        list = gedcom_parser.get_element_list()
#        list = gedcom_parser.get_element_dictionary()

        print(list)




