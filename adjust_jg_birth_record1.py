import re
from dateutil.parser import parse

import datetime as dt

none = re.search("xxx", "") #set the value for re.search = none

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

#DONE
def year_from_date(date):
    date = date.replace("\'", "")
    if is_date(date):
        dt = parse(date)
        year = int(dt.date().year)
        if year >= 2000:
            return year - 100
        else:
            return year
    else:
        return int(date[-4:]) # return 4 last chars - assuming this is the year

#DONE
def estimated_birth_year(year_date, age):
    return (int(year_date) - int(age))


#JG Birth records
jg_b_input = [

]


[

]


#DONE
#detect lines to be ignored: title and filler lines
def ignore_jg_lines(line):
        if (  len(line) < 3 or line[2] == '    Name' or line[2] == '    Groom' or line[3] == "") :
            return True
        else:
            return False



def re_comma2space(data):
    return re.sub(",", " ", data)


def re_sub_slash(data):
    return re.sub("/", " ", data)


def re_sub_dot(data):
    return re.sub(".", " ", data)


def re_sub_minus(data):
    return re.sub("-", " ", data)


def re_sub_equal_sign(data):
    return re.sub("=", " ", data)


def re_sub_colon(data):
    return re.sub(":", " ", data)


def re_sub_semicolon(data):
    return re.sub(";", " ", data)


def single_quote_to_space(data):
    return re.sub("'", " ", data)


def re_sub_dot(data):
    return re.sub("\.", " ", data)


def re_sub_slash2comma(data):
    return re.sub("/", ",", data)


#adjust JG Birth - one list/line at a time
def adjust_jg_birth(row, data_out):
    lds_record = ''

    row_idx = 3
    #Surename [0]
    data_out.append(row[row_idx].strip())
    row_idx += 2

    #given name [1]
    data_out.append(re_comma2space(row[row_idx]).strip())
    data_out[-1] = data_out[-1].replace("/ ", "")
    row_idx += 3

    #Birth date [6]
    if row[row_idx].strip() == "":
        row_idx += 1
    data_out.append(row[row_idx].strip())
    row_idx += 2

    #Sex [2]
    if row[row_idx].strip() == "":
        row_idx -= 1
        data_out.append('NA')
    else:
        data_out.append(row[row_idx].strip())
    row_idx += 3

    #Father name field [3] expected in input offset 13
    data_out.append(row[row_idx].strip())
    data_out[-1] = data_out[-1].replace("/ ", "")

    if data_out[-1] in ["-", '', "-", "--"]:
        data_out[-1] = 'noFather'
    if not row[row_idx]:
        row_idx -= 1
    row_idx += 2

    #Mother and Maiden [4], [5] expected in input offset 15 (one field to be divided)
    row[row_idx] = row[row_idx].strip()
    if row[row_idx] in ["", "-", "- -", "--", "-- --"]:
        data_out.append('noMother')
        data_out.append('noMother')
        if row[row_idx]:
            row_idx += 1
#           print("check", row[8: row_idx+3], row_idx)
    else:
        data_out.append(row[row_idx].strip()) #add element for mothers Surename
        data_out.append(data_out[-1][data_out[-1].find(' ')+1:]) #add element for mothers name
        data_out[-2] = data_out[-2][:data_out[-2].find(' ')].replace("/", "")
        data_out[-1] = data_out[-1].replace("/ ", "")

        row_idx += 1
    row_idx += 2

    #Towns - town born is the last field. need to change places
    town_reg = row[row_idx].split("/")

    lds_record = town_reg[1]
    data_out.append(town_reg[0].strip())
    row_idx += 2
    data_out.append(row[row_idx].strip())
    row_idx += 2
    data_out.append(row[row_idx].strip())
    row_idx += 3
    data_out.append(row[row_idx].strip())
    row_idx += 3
    data_out.insert(-4, data_out[-1])
    del data_out[-1]

    #comment field [12]
    data_out.append(row[row_idx].strip())
    if data_out[-1] == '':
        data_out[-1] = "noComment"
        row_idx -= 1

    # source + record + Image details [14]; check for different schemes
    row_idx += 3
    data_out.append(row[row_idx].strip() + " " + row[row_idx+2].strip() + " # " + lds_record)

    return


#Done
def name_change_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split(",", data)
    for item in comment_split:
        if "hanged" in item:
            if " to " in item:
                item = single_quote_to_space(item[item.find("hanged to ") + 9:].split()[0]).strip().upper()
            else:
                item = single_quote_to_space(item[item.find("hanged ") + 6:].split()[0]).strip().upper()
            return item
    return "noCName"


def witness_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split(",", data)
    for item in comment_split:
        if "itness" in item:
            if "itnesses" in item:
                item = item[item.find("itness") + 9:].strip()
            else:
                item = item[item.find("itness") + 7:].strip()
            return item
    return "noW"


#Done
def father_age_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split(",", data)
    for item in comment_split:
        if "ather" in item:
            age = item[item.find("ather ")+6:]
            age = re.split(" ", age)
            if age[0].isdigit():
                return int(age[0])
            else:
                return "noFAge"
    return "noFAge"


#Done
def mother_age_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split(",", data)
    for item in comment_split:
        if "other" in item:
            age = item[item.find("other ")+6:].strip()
            age = re.split(" ", age)
            if age[0].isdigit():
                return int(age[0])
            else:
                return "noMAge"
    return "noMAge"


#DONE
def extract_town_born_from_comment(data):
#search in each comment portion, order is not guranteed, split per commnet, father and mother but not 'parents'
    father_pattern = 'father' # Father
    mother_pattern = 'mother' # Mother
    father_tb = 'noFTB'
    mother_tb = "noMTB"
    item = data.lower()

    find_father = item.find(father_pattern)
    find_mother = item.find(mother_pattern)

    if (find_mother & find_father) == -1: # no father or mother found
        return father_tb, mother_tb
    if (find_mother != -1) & (find_father != -1): #both parents found
        if find_father > find_mother:  # father comes AFTER mother
            father_tb = find_town(data[find_father+6:])
            mother_tb = find_town(data[find_mother+6:find_father-1])
        else:
            mother_tb = find_town(data[find_mother+6:])
            if item.find(" and ") != -1:
                father_tb = find_town(data[find_father + 6:])
            else:
                father_tb = find_town(data[find_father+6:find_mother-1])
    elif find_father == -1: #father not found
        mother_tb = find_town(data[find_mother + 6:])
    else:
        father_tb = find_town(data[find_father + 6:])

    return father_tb, mother_tb



def find_town(item):
    item_lower = item.lower()
    born_idx = item_lower.find('born ')
    gap_idx = 0
    town = "noTB"

    if born_idx != -1:
        if item_lower.find('in ') != -1: # found "born in"
            gap_idx = 3
        semi_col = item.find(";")
        if semi_col == -1:
            town = item[born_idx + 5 + gap_idx:]
        else:
            town = item[born_inx + 8: semi_col]
    elif "b. " in item_lower:
        town = item.split()[1].strip()
    elif "b " in item_lower :
        town = item.split()[1].strip()
    elif item_lower.find("birthplace") != -1:
        birthplace = item.find("irthplace")
        if item.find("/") != -1:
            town = item[birthplace+11: item.find("/")]
        else:
            town = item[birthplace+11:]
    elif item_lower.find("from ") != -1:
        town = item[item_lower.find("from ") + 5 :]

    if item_lower.find("locally") != -1:
        town = "Locally"

    if item.find("aby ") != -1:  # case comment is like "father born <place> Baby died..."
        town = town[: town.find("aby") - 1]

    return town.strip()


#DONE
def death_date_from_comment(data):
#search in each comment portion, order is not guranteed
    data = re_sub_slash2comma(data)
    comment_split = re.split('[,;/]', data)

    for item in comment_split:
#look for ied for the case of upper/lower case initial and missing ide
        if "ied" in item :
            item = item[item.find("ied ") + 4:].strip()
        elif "eath " in item:
            item = item[item.find("eath ") + 5:].strip()
        elif " d. " in item:
            item = item[item.find("d. ") + 3:].strip()
        elif "eceased " in item:
            item = item[item.find("eceased ") + 8:].strip()
        elif "tillborn" in item:
            return "Stillborn"
        else:
            return "noDD"
        item = item[:min(len(item), 11)]
        return item

    return "noDD"


#DONE
def wed_date_from_comment(data):
#search in each comment portion, order is not guranteed
    data = re_sub_slash2comma(data)
    comment_split = re.split('[,;]', data)

    for item in comment_split:
#look for partial word for the case of upper/lower case initial and missing ide
        if "arriage date:" in item:
            item = item[item.find("arriage date:")+13:].strip()
            return year_from_date(item)
        elif "arriage" in item:
            item = item[item.find("arriage") + 7:].strip()
            return year_from_date(item)
    return "noWD"



#Done
def comment_exists(data):
    if data in ["noComment"]:
        return False
    else:
        return True

#DONE
def insert_jg_birth_fields(row):
    org_birth_date_idx = 2
    birth_date_idx = 6
    birth_year_idx = 7
    death_year_idx = 8
    father_age_idx = 9
    mother_age_idx = 10
    est_father_birth_idx = 11
    est_mother_birth_idx = 12
    name_change_idx = 18
    wed_date_idx = 20
    father_town_born_idx = 21
    mother_town_born_idx = 22
    witness_idx = 23

    row.insert(birth_date_idx+1, row[org_birth_date_idx])
    del row[org_birth_date_idx]     # move date to index 6 and remove the original placement date

    row.insert(birth_year_idx, year_from_date(row[birth_date_idx]))  # year of birth from birth date
    row.insert(death_year_idx, "noDD")
    row.insert(father_age_idx, "noFAge")
    row.insert(mother_age_idx, "noMAge")
    row.insert(est_father_birth_idx, "noFY")
    row.insert(est_mother_birth_idx, "noMY")
    row.insert(name_change_idx, "noCName")
    row.insert(wed_date_idx, "noWY") # No Wed date of Year
    row.insert(father_town_born_idx, "noFTB")
    row.insert(mother_town_born_idx, "noMTB")
    row.insert(witness_idx, "noW")

    return


def update_comment_result(data, comment_result):
    birth_date_idx = 6
    birth_year_idx = 7
    death_date_idx = 8
    father_age_idx = 9
    mother_age_idx = 10
    father_est_byear = 11
    mother_est_byear = 12
    town_born_idx = 13
    change_name_idx = 18
    wed_date_idx = 20
    father_town_born_idx = 21
    mother_town_born_idx = 22
    witness_idx = 23

    # 0 - Death Date, 1 - Father Age 2 - Mother Age, 3 - Change Name, 4 - Wed Date, 5 - Father Town Born, 6 - Mother Town Born, 7 - witness name

    data[death_date_idx] = comment_result[0]        # Death date/year - not included in original fields
    if data[death_date_idx] == "Stillborn":
        data[death_date_idx] = data[birth_date_idx]

    if data[father_age_idx] == "noFAge":             # Father Age At Child Birth
        if comment_result[1] != "noFAge":
            data[father_age_idx] = comment_result[1]
            data[father_est_byear] = estimated_birth_year(data[birth_year_idx], data[father_age_idx])
    if data[mother_age_idx] == "noMAge":             # Mother Age At Child Birth
        if comment_result[2] != "noMAge":
            data[mother_age_idx] = comment_result[2]
            data[mother_est_byear] = estimated_birth_year(data[birth_year_idx], data[mother_age_idx])

    data[change_name_idx] = comment_result[3]       # Change Name - not included in original fields
    data[wed_date_idx] = comment_result[4]          # wedding date/year - not included in original fields

#    print("before", data[20:22], data[father_town_born_idx], data[mother_town_born_idx])
    if data[father_town_born_idx] == "noFTB":            # Father Town Born
        if "Locally" in comment_result[5]:
            data[father_town_born_idx] = data[town_born_idx]
        else:
            data[father_town_born_idx] = comment_result[5]
    if data[mother_town_born_idx] == "noMTB":            # Mother Town Born
        if "Locally" in comment_result[6]:
            data[mother_town_born_idx] = data[town_born_idx]
        else:
            data[mother_town_born_idx] = comment_result[6]

    if data[witness_idx] == "noW":            # Witness name/s
        data[witness_idx] = comment_result[7]
    return




#todo - death code starts here
def parse_comment(comment, comment_result):
    comment = comment.replace(",","")
    comment_split = re.split("[/;]", comment) # split by period, slash or semicolon
    for item in comment_split:
        parse_comment_item(item, comment_result)
    return



def parse_comment_item(item, comment_result):
    # check the following fields: <data type> in comment will show as <pattern> / process
    # Death Date or Year - Date or Year [0]
    # father age and mother age - [1,2]
    # Change Name - change name <name> [3]
    # Marriage Date or Year - Date or Year [4]
    # Father Town Born & Mother Town born - Place of birth: <place> , in, b., from, born, born in [5,6]
    # witness name - [7]
    #    comment_result = ["noDD", "noFAge", "noMAge", "noCName", "noMD", "noFTB", "noMTB", "noW"]

    parents_town_born = []

    if comment_result[0] == "noDD":
        comment_result[0] = death_date_from_comment(item)

    if comment_result[1] == "noFAge":
        comment_result[1] = father_age_from_comment(item)

    if comment_result[2] == "noMAge":
        comment_result[2] = mother_age_from_comment(item)

    if comment_result[3] == "noCName":
        comment_result[3] = name_change_from_comment(item)


    if comment_result[5] == "noFTB" or comment_result[6] == "noMTB":
        parents_town_born = extract_town_born_from_comment(item)
        if parents_town_born[0] != "noFTB":
            comment_result[5] = parents_town_born[0]
        if parents_town_born[1] != "noMTB":
            comment_result[6] = parents_town_born[1]

    if comment_result[7] == "noW":
        comment_result[7] = witness_from_comment(item)

    #    print(comment_result)
    return



def build_jg_birth(data, data_out):
    idx = 0
    comment_idx = 17

    for row in data:
        if ignore_jg_lines(row):
            continue
        adjust_jg_birth(row, data_out[idx])  # adjust relevant line
        insert_jg_birth_fields(data_out[idx])  # insert elements to full size of row

#        print("row", row, data_out[idx][17])

#TODO - godfather or Sandek,tne Mohel

        comment_result = ["noDD", "noFAge", "noMAge", "noCName", "noMD", "noFTB", "noMTB", "noW"]
        if data_out[idx][comment_idx] != "noComment":
            parse_comment(data_out[idx][comment_idx], comment_result)  # extract data from comment
            update_comment_result(data_out[idx], comment_result)

        # prepare for next line
        idx += 1
        data_out.append([])
    del data_out[idx]
    return

