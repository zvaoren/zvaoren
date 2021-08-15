from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
from gedcom.element.element import Element


# Path to your `.ged` file
file_path = 'C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\Ancestry\SZABOLCS SZEKULESZ.ged'

# Initialize the parser
gedcom_parser = Parser()


# Parse your file
gedcom_parser.parse_file(file_path)
gedcom_parser.parse_file(file_path, False) # Disable strict parsing

root_child_elements = gedcom_parser.get_root_child_elements()

# Iterate through all root child elements
for element in root_child_elements:

    # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
    if isinstance(element, IndividualElement):
        element_list = element.get_element_list()
        print("GEDCOM: ", element_list)

        # Get all individuals whose surname matches "Doe"
#        if element.surname_match('Szekulesz'):


            # Unpack the name tuple
#            (first, last) = element.get_name()

            # Print the first and last name of the found individual
#           print(first + " " + last)




#Parser class
#The Parser class represents the actual parser. Use this class to parse a GEDCOM file.

#Note: May be imported via from gedcom.parser import Parser.

#Method	Parameters	Returns	Description
#invalidate_cache			Empties the element list and dictionary to cause get_element_list() and get_element_dictionary() to return updated data
#get_element_list		list of Element	Returns a list containing all elements from within the GEDCOM file
#get_element_dictionary		dict of Element	Returns a dictionary containing all elements, identified by a pointer, from within the GEDCOM file
#get_root_element		RootElement	Returns a virtual root element containing all logical records as children
#get_root_child_elements		list of Element	Returns a list of logical records in the GEDCOM file
#parse_file	str file_path, bool strict		Opens and parses a file, from the given file path, as GEDCOM 5.5 formatted data
#get_marriages	IndividualElement individual	tuple: (str date, str place)	Returns a list of marriages of an individual formatted as a tuple (str date, str place)
#get_marriage_years	IndividualElement individual	list of int	Returns a list of marriage years (as integers) for an individual
#marriage_year_match	IndividualElement individual, int year	bool	Checks if one of the marriage years of an individual matches the supplied year. Year is an integer.
#marriage_range_match	IndividualElement individual, int from_year, int to_year	bool	Check if one of the marriage years of an individual is in a given range. Years are integers.
#get_families	IndividualElement individual, str family_type = gedcom.tags.GEDCOM_TAG_FAMILY_SPOUSE	list of FamilyElement	Return family elements listed for an individual
#get_ancestors	IndividualElement individual, str ancestor_type = "ALL"	list of Element	Return elements corresponding to ancestors of an individual
#get_parents	IndividualElement individual, str parent_type = "ALL"	list of IndividualElement	Return elements corresponding to parents of an individual
#find_path_to_ancestor	IndividualElement descendant, IndividualElement ancestor, path = None	object	Return path from descendant to ancestor
#get_family_members	FamilyElement family, str members_type = FAMILY_MEMBERS_TYPE_ALL	list of IndividualElement	Return array of family members: individual, spouse, and children
#print_gedcom			Write GEDCOM data to stdout
#save_gedcom	IO open_file		Save GEDCOM data to a file