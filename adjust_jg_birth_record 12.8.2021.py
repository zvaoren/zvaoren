import re
from dateutil.parser import parse
#from clean_jg_input import clean_jg_inp

import datetime as dt

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
    return (year_date - age)


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


data_out = [[]] # temporary output list of lists
none = re.search("xxx", "") #set the value for re.search = none

build_jg_birth(jg_b_input, data_out)

i = 0
for row in data_out:
    if row[17] != "noComment":
        i += 1
        print("comment", row[17], i)
        print("results", row[8:13], "||", row[18], "||", row[20:24])



#source lists - after slight manipulation

[

['', '', '', '     L…..KOVITS', '    ', '    ,Chaje', '   ', '', '    29-May-1863', '    ', '    F', '   ', '', '    Leiser Ah', '    ', '    Ruchel', '   ', '', '    Homonna/178-15', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, name day 4 Jun 1863 Chasen', '   ', '', '    S A Ujhely Archives', '    ', '', ''],

['', '', '', '     L…..KOVITS', '    ', '    ,Ahron Schaje', '   ', '', '    18-Sep-1863', '    ', '    M', '   ', '', '    Pinkas', '    ', '    Blime', '   ', '', '    Homonna/180-11', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, circumcised 25 Sep 1863 P L…kovits, witness Salamon L…kovits', '   ', '', '    S A Ujhely Archives', '    ', '', ''],

['', '', '', '     FRIEDMAN', '    ', '    ,Jakob', '   ', '', '    24-Mar-1862', '    ', '    M', '   ', '', '    Mendl', '    ', '    L. Eszter', '   ', '', '    Nagy-Mihály/311/12-24', '    ', '    Nagy-Mihály', '    ', '    Zemplén', '   ', '', '    Nagy-Mihaly', '   ', '', '    witness- Jakob NEUWIRT', '   ', '', '    S A Ujhely Archive', '    ', '', ''],

['', '', '', '     FRIEDMAN', '    ', '    ,Abraham', '   ', '', '    24-Mar-1862', '    ', '    M', '   ', '', '    Mendl', '    ', '    L. Eszter', '   ', '', '    Nagy-Mihály/311/12-25', '    ', '    Nagy-Mihály', '    ', '    Zemplén', '   ', '', '    Nagy-Mihaly', '   ', '', '    witness- Abraham FRIED', '   ', '', '    S A Ujhely Archive', '    ', '', ''],

['', '', '', '     FLEISCHER', '    ', '    ,Janta', '   ', '', '    04-Jun-1858', '    ', '    F', '   ', '', '    Jakab', '    ', '    L?WINGER Rozalia', '   ', '', '    Szeged/82-20', '    ', "    Local Gov't", '    ', '    Csongrád', '   ', '', '    Szeged', '   ', '', '', '', '    LDS 642787, Vol. 9', '    ', '', ''],

['', '', '', '     [L]EMBICH', '    ', '    ,Emil', '   ', '', '    10-Apr-1885', '    ', '    F', '   ', '', '    Lazar', '    ', '    LANVAN Maria', '   ', '', '    Szeged/54-17', '    ', "    Local Gov't", '    ', '    Csongrád', '   ', '', '    Szeged', '   ', '', '', '', '    LDS 642787, Vol.10.', '    ', '', ''],

['', '', '', '     L.', '    ', '    ,Mozes', '   ', '', '    12-Nov-1851', '    ', '    M', '   ', '', '    Samuel', '    ', '    WEISZ Fani', '   ', '', '    Nagyvarad/412-08', '    ', "    Local Gov't", '    ', '    Bihar', '   ', '', '    Nagyvarad', '   ', '', '    Witness: Isak Michelstadter', '   ', '', "    Romanian Nat'l Archives-Oradea:756", '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Otto', '   ', '', '    04-Jun-1905', '    ', '    M', '   ', '', '    Gyula', '    ', '    SCHWARZ Henriette', '   ', '', '    Moson/130', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 34, born in St. Endre; mother 32, born in Poszony, Mor\'s surname changed to \'Szabolcs\' (1908).', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     L…..KOVITS', '    ', '    ,Leib', '   ', '', '    16-Apr-1863', '    ', '    M', '   ', '', '    Herman', '    ', '    Lani', '   ', '', '    Homonna/178-13', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, circumcised 23 Apr 1863 Pinkas L….kovits, witness Herman Spiegal', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     STEINITZ', '    ', '    ,Franziska', '   ', '', '    26-Nov-1919', '    ', '    F', '   ', '', '    Mor', '    ', '    L;OWINGER Szidonia', '   ', '', '    Pozsony/44-05', '    ', '    Local Govt', '    ', '    Pozsony', '   ', '', '    Pozsony', '   ', '', '    father b. Vittencz / mother b. Pozsony', '   ', '', '    LDS 2442338, Item 1', '    ', '', ''],
['', '', '', '     L……?', '    ', '    ,Ben Leon', '   ', '', '    28-Jun-1860', '    ', '    M', '   ', '', '    Juda', '    ', '    Szoche', '   ', '', '    Homonna/156-19', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ana Grosz, circumcised 5 Jul 1860 Leibis….?, witness Juda L…?', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     L…KOVITS', '    ', '    ,Ilye?', '   ', '', '    03-Aug-1860', '    ', '    M', '   ', '', '    Jakub', '    ', '    Chane', '   ', '', '    Homonna/158-04', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ana Grosz, circumcised 10 Aug 1860 Ch Rosenblutt, witness Samuel L……', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…KOVITS', '    ', '    ,Moses', '   ', '', '    04-Sep-1860', '    ', '    M', '   ', '', '    Lerko', '    ', '    Szari', '   ', '', '    Homonna/158-07', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ana Grosz, circumcised 11 Oct 1860 Leibisch Goldberger, witness Jacub ……..', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…KOVITS', '    ', '    ,Itzchak', '   ', '', '    26-Oct-1860', '    ', '    M', '   ', '', '    Leiser', '    ', '    Ruchel', '   ', '', '    Homonna/158-18', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, circumcised 2 Nov 1860 Ch Rosen…., witness Nathan Langman', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L……MAN', '    ', '    ,Elekszander Sise', '   ', '', '    06-Jan-1861', '    ', '    M', '   ', '', '    Markus', '    ', '    Zilli', '   ', '', '    Homonna/162-01', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Chane Weisz, circumcised 13 Jan 1861 Ch Rosenbluth, witness Ch Rosenbluth', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…..KOVITS', '    ', '    ,Marjem', '   ', '', '    21-Jan-1861', '    ', '    F', '   ', '', '    Pinkas', '    ', '    Lelima', '   ', '', '    Homonna/162-04', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Chane Weisz, name day 26 Jan 18561 Chasen', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…', '    ', '    ,Mendl', '   ', '', '    14-Feb-1861', '    ', '    M', '   ', '', '    Israel', '    ', '    ..randl', '   ', '', '    Homonna/162-13', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Chane Weisz, circumcised 21 Feb 1861 M Taub, witness Sehahim Grunfeld', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…KOVITS', '    ', '    ,Berl?', '   ', '', '    30-Oct-1861', '    ', '    M', '   ', '', '    Herman', '    ', '    Leni', '   ', '', '    Homonna/164-14', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Chane Weisz, circumcised 6 Nov 1861 HL Eichler, witness Salamon L…kovits', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…NOVITS', '    ', '    ,Scheindl', '   ', '', '    25-Oct-1861', '    ', '    F', '   ', '', '    Mendl', '    ', '    Leib', '   ', '', '    Homonna/166-04', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Modra', '   ', '', '    Illegitimate, midwife Hentse, name day 20 Oct 1861 Moses Lanvirth', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L………', '    ', '    ,Abrham Isak', '   ', '', '    23-Apr-1861', '    ', '    M', '   ', '', '    Herman', '    ', '    Hendl', '   ', '', '    Homonna/166-08', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Cz Lolla', '   ', '', '    Midwife Sch…….., circumcised 30 Apr 1862 B Lundar, witness Josef Hendler', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L..AJER', '    ', '    ,Ester', '   ', '', '    30-Dec-1861', '    ', '    F', '   ', '', '    Leib', '    ', '    Szari', '   ', '', '    Homonna/166-12', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Cz Lolla', '   ', '', '    Midwife Sch…….., name day 31 Dec 1862 Josef Hendler', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     L…..KOVITS', '    ', '    ,Mindl', '   ', '', '    23-Apr-1862', '    ', '    F', '   ', '', '    Pinkas', '    ', '    Szlima', '   ', '', '    Homonna/170-10', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, name day 26 Apr 1862 Chasen', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     L…..KOVITS', '    ', '    ,Leah', '   ', '', '    09-May-1862', '    ', '    F', '   ', '', '    Jakub', '    ', '    Rosie', '   ', '', '    Homonna/170-14', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '    Midwife Ch Weisz, name day 17 May 1862 Chasen', '   ', '', '    S A Ujhely Archives', '    ', '', ''],
['', '', '', '     GOLDSTEIN', '    ', '    ,Karlman / Karl', '   ', '', '    27-Dec-1854', '    ', '    M', '   ', '', '    Jacob', '    ', '    L..? Rosi', '   ', '', '    Budapest/198-06', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 4', '    ', '', ''],

['', '', '', '     L…?', '    ', '    ,', '   ', '', '    3-Jul-1851', '    ', '    F', '   ', '', '    Chajim', '    ', '    Blima', '   ', '', '    Homonna/21-Jan', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Koschkoz', '   ', '', '', '', '    LDS', '    ', '     1792090', '    ', '    , Item 2', '    ', '', ''],

['', '', '', '     L...', '    ', '    ,Isak Leiser', '   ', '', '    10-Jul-1853', '    ', '    M', '   ', '', '    Schaje H.', '    ', '    Peszl', '   ', '', '    Homonna/6-20', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Meso Laborz', '   ', '', '', '', '    LDS', '    ', '     1792090', '    ', '    , Item 2', '    ', '', ''],

['', '', '', '     L…?', '    ', '    ,Pan', '   ', '', '    19-Mar-1871', '    ', '    F', '   ', '', '    Wolf', '    ', '    Hani', '   ', '', '    Homonna/41-15', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Homonna', '   ', '', '', '', '    LDS', '    ', '     1792090', '    ', '    , Item 2', '    ', '', ''],

['', '', '', '     L...OVITS? [LAZAROVITS?]', '    ', '    ,Hani / Sali', '   ', '', '    18-Jul-1869', '    ', '    F', '   ', '', '    Abraham', '    ', '    - Betti', '   ', '', '    Tolcsva/30-23', '    ', '    Tokaj', '    ', '    Zemplén', '   ', '', '    Tolcsva', '   ', '', '', '', '    LDS 642959, Vol. 2', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     SIM[E]L', '    ', '    ,stillborn', '   ', '', '    26-Aug-1876', '    ', '    F', '   ', '', '    Ignacz', '    ', '    WEISZLOVICS Hani', '   ', '', '    Kassa/35-14', '    ', "    Local Gov't", '    ', '    Abaúj-Torna', '   ', '', '    Kassa', '   ', '', '    Child died 26-Aug-1876', '   ', '', '    LDS', '    ', '     1920776', '    ', '    , Item 1', '    ', '', ''],

['', '', '', '     ROSENTHAL L.', '    ', '    ,Adolf', '   ', '', '    22-Feb-1875', '    ', '    M', '   ', '', '    Lipot', '    ', '    KRAUSZ …ette', '   ', '', '    Budapest/23-12', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '    Witness: Lipot krausz.  Child died ??-Feb-1877.', '   ', '', '    LDS 642965, Vol. 10', '    ', '', ''],

['', '', '', '     GLUCK', '    ', '    ,Aladar', '   ', '', '    30-Dec-1881', '    ', '    M', '   ', '', '    Dr. Sandor', '    ', '    L..KAUF? Karolina', '   ', '', '    Budapest/168-06', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642967 Vol. 14', '    ', '', ''],

['', '', '', '     CHEIM', '    ', '    ,Adolf', '   ', '', '    8-Aug-1853', '    ', '    M', '   ', '', '    Moritz', '    ', '    KR????L Ro????', '   ', '', '    Szeged/10-11', '    ', "    Local Gov't", '    ', '    Csongrád', '   ', '', '    Szeged', '   ', '', '', '', '    LDS 642785, Vol. 2', '    ', '', ''],

['', '', '', '     SCHESINGER', '    ', '    ,Ignatz', '   ', '', '    9-Jul-1860', '    ', '    M', '   ', '', '    Salomon', '    ', '    L…? Cacilie', '   ', '', '    Szeged/85-05', '    ', "    Local Gov't", '    ', '    Csongrád', '   ', '', '    Szeged', '   ', '', '    Name later changed to SZUES.', '   ', '', '    LDS 642785, Vol. 2', '    ', '', ''],

['', '', '', '     FEUERERSEN', '    ', '    ,Kalman', '   ', '', '    15-Dec-1884', '    ', '    M', '   ', '', '    Lipot', '    ', '    L…GEL Ernesztina', '   ', '', '    Budapest/12-07', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642990, Vol. 3', '    ', '', ''],

['', '', '', '     FEUERERSEN', '    ', '    ,Kalman', '   ', '', '    15-Dec-1884', '    ', '    M', '   ', '', '    Lipot', '    ', '    L…GEL Ernesztina', '   ', '', '    Budapest/12-07', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642990, Vol. 3', '    ', '', ''],

['', '', '', '     L…?', '    ', '    ,Rifka Rohel', '   ', '', '    06-Jun-1844', '    ', '', '', '    Zisman', '    ', '    Ityka', '   ', '', '    Galszecs/013-25', '    ', '    Galszecs', '    ', '    Zemplén', '   ', '', '    Galszecs', '   ', '', '', '', '    SA Ujhely Archives', '    ', '', ''],
['', '', '', '     LORBER', '    ', '    ,Samu', '   ', '', '    28-Mar-1876', '    ', '    M', '   ', '', '    Moritz', '    ', '    LORBER Hani', '   ', '', '    Nyiregyhaza/034-010', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Mohel's name and circumcision date: J. DEUTSCH - 04-Apr-1876/Witness: Israel L. FRIED", '   ', '', '    LDS 642913', '    ', '', ''],

['', '', '', '     SPIRA', '    ', '    ,Menyhard', '   ', '', '    25-May-1876', '    ', '    M', '   ', '', '    Josef', '    ', '    BERKOWITZ Theres', '   ', '', '    Nyiregyhaza/035-023', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Midwife: B. WEISZ/Mohel's name and circumcision date: J. L. KOHN - 02-Jun-1876/Witness: Aron STEINBERGER", '   ', '', '    LDS 642913', '    ', '', ''],

['', '', '', '     FRIEDMAN', '    ', '    ,Chajim', '   ', '', '    05-Jul-1876', '    ', '    M', '   ', '', '    Elyas', '    ', '    FRIEDMAN Lisa', '   ', '', '    Nyiregyhaza/035-028', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Midwife: B. WEISZ/Mohel's name and circumcision date: J. L. KOHN - 12-Jul-1876/Witness: Elyas FRIEDMAN", '   ', '', '    LDS 642913', '    ', '', ''],

['', '', '', '     BLUM', '    ', '    ,Josef', '   ', '', '    26-Jul-1876', '    ', '    M', '   ', '', '    Herman', '    ', '    GUTMAN Rosi', '   ', '', '    Nyiregyhaza/035-033', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Mohel's name and circumcision date: J. L. KOHN - 02-Aug-1876/Witness: M. EGER", '   ', '', '    LDS 642913', '    ', '', ''],

['', '', '', '     STERN', '    ', '    ,Ignatz', '   ', '', '    18-Nov-1879', '    ', '    M', '   ', '', '    Fabian', '    ', '    RUBENSTEIN Pepi', '   ', '', '    Nyiregyhaza/046-078', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Midwife: J. KOHN/Mohel's name and circumcision date: S. REWITZ - 25-Nov-1879/Witness: I. L. FRIED", '   ', '', '    LDS 642913', '    ', '', ''],

['', '', '', '     L…..?', '    ', '    ,Beti', '   ', '', '    31-Apr-1865', '    ', '    F', '   ', '', '    Sandor', '    ', '    CZ….? Beti', '   ', '', '    Polgar/5-18', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 1', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     LAUFER', '    ', '    ,Rosi', '   ', '', '    30-Nov-1873', '    ', '    F', '   ', '', '    Ignatz', '    ', '    L. Rezi', '   ', '', '    Satoraljaujhely/091-003', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Ujhely', '   ', '', '    Midwife: Goldstein', '   ', '', '    LDS 642954', '    ', '', ''],

['', '', '', '     STEIN', '    ', '    ,Isak', '   ', '', '    10-Feb-1873', '    ', '    M', '   ', '', '    Mor', '    ', '    L. Leni', '   ', '', '    Satoraljaujhely/163-018', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Bodzas-Ujlak', '   ', '', '    Mohel: Hersko Weisz', '   ', '', '    LDS 642954', '    ', '', ''],

['', '', '', '     LEICHTENBERG', '    ', '    ,Rezi', '   ', '', '    20-Mar-1873', '    ', '    F', '   ', '', '    Heiman', '    ', '    L. Sali', '   ', '', '    Satoraljaujhely/163-021', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Bodzas-Ujlak', '   ', '', '', '', '    LDS 642954', '    ', '', ''],

['', '', '', '     LAJZEROVICS', '    ', '    ,Gadiel', '   ', '', '    04-Jun-1873', '    ', '    M', '   ', '', '    Mor', '    ', '    L. Kati', '   ', '', '    Satoraljaujhely/164-011', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Magyar-Jesztreb', '   ', '', '    Mohel: Markus Schon', '   ', '', '    LDS 642954', '    ', '', ''],

['', '', '', '     LAJZEROVICS', '    ', '    ,Kati', '   ', '', '    08-Jul-1873', '    ', '    F', '   ', '', '    Abraham', '    ', '    L. fani', '   ', '', '    Satoraljaujhely/164-018', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Magyar-Jesztreb', '   ', '', '', '', '    LDS 642954', '    ', '', ''],
['', '', '', '     SINGER', '    ', '    ,Istvan', '   ', '', '    13-Nov-1892', '    ', '    M', '   ', '', '    Sandor', '    ', '    SCHON Jenny / Sarolta', '   ', '', '    Budapest/44-08', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '    Jenny Schon also known as Sarolta Schon. The family name of Istvan Singer changed to Szabolcs on 28-Mar-1907. Father and mother born locally.', '   ', '', '    LDS 642972, Vol. 22', '    ', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Samuel Meilech', '   ', '', '    28-Aug-1885', '    ', '    M', '   ', '', '    Ignatz', '    ', '    OBER Ida', '   ', '', '    Karasz/2-09', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Karasz', '   ', '', '', '', '    LDS 642913, Vol. 1', '    ', '', ''],

['', '', '', '     HUBER', '    ', '    ,Salomon', '   ', '', '    14-Apr-1883', '    ', '    M', '   ', '', '    Mor', '    ', '    GROSZ Betti', '   ', '', '    Tokaj/142-08', '    ', '    Tokaj', '    ', '    Zemplén', '   ', '', '    Tokaj', '   ', '', '', '', '    LDS 642959', '    ', '', ''],

['', '', '', '     JARA...HOWER?', '    ', '    ,Joseph', '   ', '', '    23-Dec-1860', '    ', '    M', '   ', '', '    Jacob', '    ', '    KUPFERSTEIN Hani', '   ', '', '    Kassa/45-05', '    ', '    Local Gov`t', '    ', '    Abaúj-Torna', '   ', '', '    Kassa', '   ', '', '', '', '    LDS', '    ', '     1920775', '    ', '    , Item 5', '    ', '', ''],

['', '', '', '     HOBER', '    ', '    ,Bernard', '   ', '', '    1-May-1865', '    ', '    M', '   ', '', '    Marcus', '    ', '    STERNBERG Rosalie', '   ', '', '    Budapest/29-10', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963, Vol 7', '    ', '', ''],

['', '', '', '     SCHLESINGER', '    ', '    ,Charlotte', '   ', '', '    12-Jan-1867', '    ', '    F', '   ', '', '    Ignaz', '    ', '    HUBER Ernestine', '   ', '', '    Budapest/167-14', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963 Vol. 7', '    ', '', ''],

['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     NEUBAUER', '    ', '    ,Mary', '   ', '', '    1840', '    ', '    F', '   ', '', '    Jacob', '    ', '    L... H...', '   ', '', '    Bittse/2', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Kollarowitz', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],

['', '', '', '     GRUNBAUM', '    ', '    ,Joachim', '   ', '', '    22-Nov-1840', '    ', '    M', '   ', '', '    Emanuel', '    ', '    L... July', '   ', '', '    Bittse/10', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],

['', '', '', '     LOVENBEIN', '    ', '    ,Sali', '   ', '', '    30-Mar-1877', '    ', '    F', '   ', '', '    Leopold', '    ', '    WEISS JASSNIGER Jetti', '   ', '', '    Illava/2174', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Bellus', '   ', '', '    Godparents or Witnesses: L Schwarz', '   ', '', '    LDS 1981155, item 6', '    ', '', ''],

['', '', '', '     L…D?', '    ', '    ,Wolf', '   ', '', '    1-Aug-1838', '    ', '    M', '   ', '', '    Martony', '    ', '    - Breter', '   ', '', '    Kecskemet/15-15', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Kecskemet', '   ', '', '    See also record 16-22', '   ', '', '    LDS 642857, Vol 1', '    ', '', ''],
['', '', '', '     GROSZ', '    ', '    ,Armin', '   ', '', '    17-Jan-1884', '    ', '    M', '   ', '', '    Fozsef', '    ', '    OBER Fanni', '   ', '', '    Kisvarda/196-07', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Deceased 15-Jun-1886', '   ', '', '    LDS 642905 Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Yetti', '   ', '', '    25-May-1884', '    ', '    F', '   ', '', '    Juda', '    ', '    - Szima', '   ', '', '    Kisvarda/197-08', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905 Vol. 6', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Etelka', '   ', '', '    05-Feb-1887', '    ', '    F', '   ', '', '    Ignacz', '    ', '    OBER Hanni', '   ', '', '    Kisvarda/260-04', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Father born Karasz', '   ', '', '    LDS 642905, Vol 6', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Bernhard / Beil', '   ', '', '    19-Feb-1888', '    ', '    M', '   ', '', '    Izsak / Yiczehavk', '    ', '    OBER Hani / Hinck', '   ', '', '    Kisvarda/291-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Father born Karavz', '   ', '', '    LDS 642905, Vol 6', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Terez / Taube Malke', '   ', '', '    17-Jan-1890', '    ', '    F', '   ', '', '    Ignacz / Jiczchak', '    ', '    OBER Hani', '   ', '', '    Kisvarda/351-06', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    fahtr born Karasz', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     WEISZ', '    ', '    ,Helena', '   ', '', '    03-Mar-1891', '    ', '    F', '   ', '', '    Ignacz', '    ', '    OBER Hani', '   ', '', '    Kisvarda/374-07', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    father born Karasz; mother born Kisvarda', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Jozsef / Jonesz', '   ', '', '    19-Jun-1892', '    ', '    M', '   ', '', '    Ignatz', '    ', '    OBER Ida / Hinde', '   ', '', '    Kisvarda/399-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    father born Karasz; mother born Kisvarda', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     VEISZ', '    ', '    ,Jozsef Jonesz', '   ', '', '    19-Jun-1892', '    ', '    M', '   ', '', '    Ignasz', '    ', '    OBER Ida', '   ', '', '    Kisvarda/420-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    father from Rarosz', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     HUBER', '    ', '    ,Jeno', '   ', '', '    17-May-1891', '    ', '    M', '   ', '', '    -', '    ', '    HUBER Pepi', '   ', '', '    Gyor/419-08', '    ', "    Local Gov't", '    ', '    Györ', '   ', '', '    Gyor', '   ', '', '', '', '    LDS 642804, Vol. 1', '    ', '', ''],
['', '', '', '     OBER', '    ', '    ,Majer', '   ', '', '    12-Mar-1875', '    ', '    M', '   ', '', '    Izrael', '    ', '    ROTH Rezi', '   ', '', '    Kisvarda/76-20', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Etelka', '   ', '', '    05-Nov-1876', '    ', '    F', '   ', '', '    Izrael', '    ', '    ROTH Reizel', '   ', '', '    Kisvarda/86-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Czilla', '   ', '', '    30-Sep-1878', '    ', '    F', '   ', '', '    Herman', '    ', '    EIZDORFER Betti', '   ', '', '    Kisvarda/98-04', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Roza', '   ', '', '    20-Dec-1880', '    ', '    F', '   ', '', '    Josef', '    ', '    KLEIN Cilli', '   ', '', '    Kisvarda/110-08', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905 Vol.6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Wolf', '   ', '', '    16-Jun-1881', '    ', '    M', '   ', '', '    Izrael', '    ', '    ROTH Leni', '   ', '', '    Kisvarda/115-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905  Vol. 6', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     GROSZ', '    ', '    ,Fechiel', '   ', '', '    11-Mar-1882', '    ', '    M', '   ', '', '    Josef', '    ', '    OBER Fani', '   ', '', '    Kisvarda/119-06', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905  Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Wolf', '   ', '', '    22-Apr-1882', '    ', '    M', '   ', '', '    Josef', '    ', '    KLEIN Czilli', '   ', '', '    Kisvarda/120-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905  Vol. 6', '    ', '', ''],

['', '', '', '     GROSZ', '    ', '    ,Amalia', '   ', '', '    6-Dec-1885', '    ', '    F', '   ', '', '    Josef', '    ', '    OBER Fani', '   ', '', '    Kisvarda/129-05', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905  Vol. 6', '    ', '', ''],

['', '', '', '     VEISZ', '    ', '    ,Samuel Meilech', '   ', '', '    28-Aug-1885', '    ', '    M', '   ', '', '    Ignacz', '    ', '    IBER Yda', '   ', '', '    Kisvarda/181-13', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Karasz', '   ', '', '', '', '    LDS 642905 Vol. 6', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Relli', '   ', '', '    13-Jan-1883', '    ', '    F', '   ', '', '    Herman', '    ', '    EISDORFER Betti', '   ', '', '    Kisvarda/191-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905 Vol. 6', '    ', '', ''],
['', '', '', '     OBER', '    ', '    ,Beli?', '   ', '', '    13-Jan-1883', '    ', '    F', '   ', '', '    Herman', '    ', '    EISDORFER Betti', '   ', '', '    Kisvarda/43-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904 Vol.2', '    ', '', ''],

['', '', '', '     GROSZ', '    ', '    ,Armi', '   ', '', '    17-Jan-1883', '    ', '    M', '   ', '', '    Jozsef', '    ', '    OBER Fani', '   ', '', '    Kisvarda/48-07', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS-642904 Vol. 2', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Letti?', '   ', '', '    25-May-1884', '    ', '    F', '   ', '', '    Luda?', '    ', '    - Sima', '   ', '', '    Kisvarda/49-08', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS 642904 Vol. 2', '    ', '', ''],

['', '', '', '     GROSZ', '    ', '    ,Amalia', '   ', '', '    06-Dec-1885', '    ', '    F', '   ', '', '    Joszef', '    ', '    OBER Fani', '   ', '', '    Kisvarda/58-06', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS 642904 Vol. 2', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Ettelka', '   ', '', '    5-Feb-1887', '    ', '    F', '   ', '', '    Ignacz', '    ', '    OBER Hani', '   ', '', '    Kisvarda/16-04', '    ', '    Kis-varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Father born Karasz Baby died 25-May-1887', '   ', '', '    LDS 642904, Vol. 3', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     VEISZ', '    ', '    ,Bernhart', '   ', '', '    19-Feb-1888', '    ', '    M', '   ', '', '    Izsak', '    ', '    OBER Hani', '   ', '', '    Kisvarda/28-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol. 3', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Terez / Taube / Malke', '   ', '', '    17-Jan-1890', '    ', '    F', '   ', '', '    Ignacz / Izchak', '    ', '    OBER Hani', '   ', '', '    Kisvarda/57-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Died 19 Apr 1890; Father from Karacz', '   ', '', '    LDS 642904, Vol. 3', '    ', '', ''],

['', '', '', '     VEISZ', '    ', '    ,Helina / Chaja', '   ', '', '    3-Mar-1891', '    ', '    F', '   ', '', '    Ignaz / Jizhak', '    ', '    OBER Hani', '   ', '', '    Kisvarda/76-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Father from Karasz', '   ', '', '    LDS 642904, Vol. 3', '    ', '', ''],

['', '', '', '     WEISZ', '    ', '    ,Josef / Jonesz', '   ', '', '    19-Jun-1892', '    ', '    M', '   ', '', '    Ignaz', '    ', '    OBER? Ida / Hinda', '   ', '', '    Kisvarda/99-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '    Died 4 Jul 1892 Father from Karasz', '   ', '', '    LDS 642904, Vol. 3', '    ', '', ''],

['', '', '', '     UBER', '    ', '    ,Kalman', '   ', '', '    12-Aug-1868', '    ', '    M', '   ', '', '    Jakob', '    ', '    - Zili', '   ', '', '    Kisvarda/54-09', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '    Mother born Doghe', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],
['', '', '', '     GRUNWALD', '    ', '    ,Rosalie', '   ', '', '    28-Apr-1858', '    ', '    F', '   ', '', '    Kalman', '    ', '    HOBER Anna', '   ', '', '    Budapest/20-11', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],

['', '', '', '     SCHLESINGER', '    ', '    ,Jacob', '   ', '', '    25-Feb-1864', '    ', '    M', '   ', '', '    Ignaz L.', '    ', '    HUBER Ernestine', '   ', '', '    Budapest/89-13', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963, Vol. 6', '    ', '', ''],

['', '', '', '     UBER', '    ', '    ,Salamon', '   ', '', '    12-Aug-1868', '    ', '    M', '   ', '', '    Jakob', '    ', '    - Zily', '   ', '', '    Kisvarda/71-23', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS 642904, Vol. 1', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Majer', '   ', '', '    12-Mar-1875', '    ', '    M', '   ', '', '    Izrael', '    ', '    ROTH Rezi', '   ', '', '    Kisvarda/120-25', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kis Varda', '   ', '', '', '', '    LDS 642904, Vol 1', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     OBER', '    ', '    ,Ettel', '   ', '', '    05-Nov-1876', '    ', '    F', '   ', '', '    Izrael', '    ', '    ROTH Rezl', '   ', '', '    Kisvarda/6-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol. 2', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Lili / Cili', '   ', '', '    30-Sep-1878', '    ', '    F', '   ', '', '    Hermann', '    ', '    EIZDORFER Betti', '   ', '', '    Kisvarda/18-04', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol. 2', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Wolf', '   ', '', '    16-Jun-1881', '    ', '    M', '   ', '', '    Izrael', '    ', '    ROTH Reza', '   ', '', '    Kisvarda/34-01', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol 2', '    ', '', ''],

['', '', '', '     GROSS', '    ', '    ,Yechiel', '   ', '', '    11-Mar-1882', '    ', '    M', '   ', '', '    Josef', '    ', '    OBER Fani', '   ', '', '    Kisvarda/38-06', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol 2', '    ', '', ''],

['', '', '', '     OBER', '    ', '    ,Menase / Wolf', '   ', '', '    22-Apr-1882', '    ', '    M', '   ', '', '    Josef', '    ', '    KLEIN Cili', '   ', '', '    Kisvarda/39-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904, Vol 2', '    ', '', ''],
['', '', '', '     MOZES', '    ', '    ,Marcusz', '   ', '', '    02-Apr-1854', '    ', '    M', '   ', '', '    Jacob', '    ', '    JOZSEF Leni', '   ', '', '    Patroha/001-10', '    ', '    Kis-varda', '    ', '    Szabolcs', '   ', '', '    Patroha', '   ', '', '', '', '    LDS 642915, Item 6', '    ', '', ''],

['', '', '', '     MOZES', '    ', '    ,Marcusz', '   ', '', '    02-Apr-1854', '    ', '    M', '   ', '', '    Jacob', '    ', '    JOZSEF Leni', '   ', '', '    Patroha/001-10', '    ', '    Kis-varda', '    ', '    Szabolcs', '   ', '', '    Patroha', '   ', '', '', '', '    LDS 642915, Item 6', '    ', '', ''],
['', '', '', '     HOBER', '    ', '    ,Jacob', '   ', '', '    30-Sep-1845', '    ', '    M', '   ', '', '    Markus', '    ', '    STERNBERG Salie', '   ', '', '    Budapest/169-04', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '    Surname changed HUBER in 1914', '   ', '', '    LDS 642961, Vol. 1', '    ', '', ''],

['', '', '', '     KLEIN', '    ', '    ,Abraham', '   ', '', '    27-Oct-1845', '    ', '    M', '   ', '', '    Salomon', '    ', '    HUBER Rosalie', '   ', '', '    Budapest/170-11', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol. 1', '    ', '', ''],

['', '', '', '     LEDERER', '    ', '    ,Henrik', '   ', '', '    24-Mar-1851', '    ', '    M', '   ', '', '    David', '    ', '    HAUBER Fanni', '   ', '', '    Budapest/79-03', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol. 2', '    ', '', ''],

['', '', '', '     HUBER', '    ', '    ,Fanni', '   ', '', '    26-May-1855', '    ', '    F', '   ', '', '    Marcus', '    ', '    STERNBERG Salie', '   ', '', '    Budapest/222-13', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],

['', '', '', '     HAUBER', '    ', '    ,Daniel', '   ', '', '    02-Jun-1850', '    ', '    M', '   ', '', '    Heinrich', '    ', '    - Marie', '   ', '', '    Budapest/283-01', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],

['', '', '', '     GAUBER', '    ', '    ,Josef', '   ', '', '    09-Jul-1857', '    ', '    M', '   ', '', '    Ignatz', '    ', '    WEISS Julie', '   ', '', '    Budapest/350-09', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963, Vol.4', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,unnamed', '   ', '', '    14-Aug-1894', '    ', '    M', '   ', '', '    Herman', '    ', '    SPITZER Roza', '   ', '', '    Mateszalka/191-03', '    ', '    Mateszalka', '    ', '    Szatmár', '   ', '', '    Mateszalka', '   ', '', '    stillborn / father b. Er-Szt-Mihaly / mother b. Szatmar', '   ', '', '    LDS 642920, vol. 2', '    ', '', ''],

['', '', '', '     KLEIN', '    ', '    ,Regina', '   ', '', '    16-Jan-1895', '    ', '    F', '   ', '', '    -', '    ', '    KLEIN Ida', '   ', '', '    Mateszalka/196-04', '    ', '    Mateszalka', '    ', '    Szatmár', '   ', '', '    Mateszalka', '   ', '', '    Father is Izsak JOZSEF / mother b. Ny-Mada', '   ', '', '    LDS 642920, vol. 2', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Abraham', '   ', '', '    02-Dec-1878', '    ', '    M', '   ', '', '    Herman', '    ', '    ROSENTHAL Rozalia', '   ', '', '    Beregszasz/246-09', '    ', "    Local Gov't.", '    ', '    Bereg', '   ', '', '    Darocz', '   ', '', '', '', '    LDS', '    ', '     2429478', '    ', '    Item 4', '    ', '', ''],

['', '', '', '     JOZSEF', '    ', '    ,Peppi', '   ', '', '    27-Jun-1876', '    ', '    F', '   ', '', '    Herman', '    ', '    ROZENTHAL Rozi', '   ', '', '    Beregszasz/218-11', '    ', "    Local Gov't.", '    ', '    Bereg', '   ', '', '    Darocz', '   ', '', '', '', '    LDS', '    ', '     2429478', '    ', '    Item 4', '    ', '', ''],

['', '', '', '     LORINTZ', '    ', '    ,Hani', '   ', '', '    19-Mar-1872', '    ', '    F', '   ', '', '    Jakab', '    ', '    JOZSEF Rozi', '   ', '', '    Beregszasz/263-05', '    ', "    Local Gov't.", '    ', '    Bereg', '   ', '', '    Csetfalva', '   ', '', '', '', '    LDS', '    ', '     2429478', '    ', '    Item 4', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     JOSEPH', '    ', '    ,Pepi', '   ', '', '    28-Jul-1863', '    ', '    F', '   ', '', '    Natan', '    ', '    TRIBVASZER Debora', '   ', '', '    Mezokaszony/02-04', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    Barkaszo', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     FRIDMAN', '    ', '    ,Lajos', '   ', '', '    11-Feb-1864', '    ', '    M', '   ', '', '    Hersko', '    ', '    JOSEPH Leni', '   ', '', '    Mezokaszony/03-04', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    K-Begany', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     FRIDMAN', '    ', '    ,Mihaly', '   ', '', '    01-Jun-1865', '    ', '    M', '   ', '', '    Hersko', '    ', '    JOSEPH Leni', '   ', '', '    Mezokaszony/05-11', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    K-Begany', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     JOSEPH', '    ', '    ,Israel', '   ', '', '    09-Nov-1865', '    ', '    M', '   ', '', '    Natan', '    ', '    TRIBVASZER Debora', '   ', '', '    Mezokaszony/06-10', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    Balazser', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     FRIDMAN', '    ', '    ,Bernat', '   ', '', '    01-May-1866', '    ', '    M', '   ', '', '    Hersko', '    ', '    JOZEPH Leni', '   ', '', '    Mezokaszony/07-10', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    K-Begany', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     JOSEPH', '    ', '    ,Sara', '   ', '', '    28-Aug-1866', '    ', '    F', '   ', '', '    Natan', '    ', '    FRID Debora', '   ', '', '    Mezokaszony/08-02', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    Balazser', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     FRIDMAN', '    ', '    ,Bernat', '   ', '', '    21-Jul-1868', '    ', '    M', '   ', '', '    Hersko', '    ', '    JOZSEF Leni', '   ', '', '    Mezokaszony/12-16', '    ', '    Kaszony', '    ', '    Bereg', '   ', '', '    K-Begany', '   ', '', '', '', '    LDS', '    ', '     2429480', '    ', '    Item 8', '    ', '', ''],

['', '', '', '     JOZEF', '    ', '    ,Hani', '   ', '', '    30-Nov-1852', '    ', '    F', '   ', '', '    Herman', '    ', '    KLEIN Rejza', '   ', '', '    Balkany/006-21', '    ', '    Nagy-kallo', '    ', '    Szabolcs', '   ', '', '    Balkany', '   ', '', '', '', '    LDS 642900, Item 6', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Herman', '   ', '', '    13-May-1887', '    ', '    M', '   ', '', '    Mendl', '    ', '    SNITZLER Sali', '   ', '', '    Csenger/31-03', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Munkacs / mother b. Mihalydi / d. 11-Dec-1887', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Adolf', '   ', '', '    05-Oct-1887', '    ', '    M', '   ', '', '    Farkas', '    ', '    ROOS Amalia', '   ', '', '    Csenger/33-01', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Regina', '   ', '', '    12-Mar-1889', '    ', '    F', '   ', '', '    Farkas', '    ', '    ROOS Amalia', '   ', '', '    Csenger/40-03', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Bernat', '   ', '', '    04-Aug-1889', '    ', '    M', '   ', '', '    Mendl', '    ', '    SNITZLER Sali', '   ', '', '    Csenger/43-02', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Munkacs / mother b. Mihalydi / d. 12-Sep-1889', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     JOZSEF', '    ', '    ,Roza', '   ', '', '    02-Jun-1890', '    ', '    F', '   ', '', '    Farkas', '    ', '    ROOZ Amalia', '   ', '', '    Csenger/47-02', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos / d. 06-Jul-1890', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Henrik', '   ', '', '    28-Jul-1891', '    ', '    M', '   ', '', '    Farkas', '    ', '    ROOS Amalia', '   ', '', '    Csenger/53-04', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     JOZSEF', '    ', '    ,Roza', '   ', '', '    17-Oct-1891', '    ', '    F', '   ', '', '    Mendl', '    ', '    SNITZLER Sali', '   ', '', '    Csenger/54-08', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b Munkacs / mother b. Kotaj', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],

['', '', '', '     JOZSEF', '    ', '    ,Bernat', '   ', '', '    16-Sep-1894', '    ', '    M', '   ', '', '    Farkas', '    ', '    ROOS Amalia', '   ', '', '    Csenger/70-06', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],

['', '', '', '     UNGERLEIDER', '    ', '    ,Moses', '   ', '', '    10 May 1863', '    ', '    M', '   ', '', '    Aberham', '    ', '    BRAUN Rosi', '   ', '', '    Gyongyos/126-10', '    ', "    Local Gov't", '    ', '    Heves', '   ', '', '    Gyongyos', '   ', '', "    Jozsef  under Given Name; Gabor under Father's given name", '   ', '', '    LDS 642816, Item 5', '    ', '', ''],
['', '', '', '     JOSEF', '    ', '    ,Majer Volf', '   ', '', '    18-Mar-1858', '    ', '    M', '   ', '', '    Josef', '    ', '    ?', '   ', '', '    Nyirbator/5-12', '    ', '    Nyir-Bator', '    ', '    Szabolcs', '   ', '', '    Nyirbator', '   ', '', '    No name for mother,surname for father', '   ', '', '    LDS 642911, Vol 1', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],

['', '', '', '     JOSEF', '    ', '    ,Eszter', '   ', '', '    03-Nov-1858', '    ', '    F', '   ', '', '    Veron?', '    ', '    Malkeh', '   ', '', '    Nyirbator/5-25', '    ', '    Nyir-Bator', '    ', '    Szabolcs', '   ', '', '    Nyirbator', '   ', '', '', '', '    LDS 642911, Vol 1', '    ', '', ''],

['', '', '', '     JOZEF', '    ', '    ,Saje', '   ', '', '    20-Sep-1852', '    ', '    M', '   ', '', '    Elias', '    ', '    EHRENFELD Rebeka', '   ', '', '    Nyirbator/2-17', '    ', '    Nyir-bator', '    ', '    Szabolcs', '   ', '', '    Nyirbator', '   ', '', '', '', '    LDS 642912, Vol. 8', '    ', '', ''],

['', '', '', '     SANDOR', '    ', '    ,Rozi', '   ', '', '    28-Jan-1853', '    ', '    M', '   ', '', '    Leopold', '    ', '    JOZSEF Hani', '   ', '', '    Szinyer-varalji/3-01', '    ', '    Szinyer-varalji', '    ', '    Szatmár', '   ', '', '    Szinyer-varalji', '   ', '', '', '', '    Register 1598 f 2', '    ', '', ''],

['', '', '', '     GROSZMAN', '    ', '    ,Peppi', '   ', '', '    13-Apr-1871', '    ', '    F', '   ', '', '    Salamon', '    ', '    JOSEF Sali', '   ', '', '    Tolcsva/48-07', '    ', '    Tokaj', '    ', '    Zemplén', '   ', '', '    Tolcsva', '   ', '', '', '', '    LDS 642960, Vol. 7', '    ', '', ''],

['', '', '', '     GROSZMAN', '    ', '    ,David', '   ', '', '    31-Jun-1872', '    ', '    M', '   ', '', '    Salamon', '    ', '    JOSEF Sari', '   ', '', '    Tolcsva/48-48', '    ', '    Tokaj', '    ', '    Zemplén', '   ', '', '    Tolcsva', '   ', '', '', '', '    LDS 642960, Vol. 7', '    ', '', ''],

['', '', '', '     JOZSEF', '    ', '    ,Herman', '   ', '', '    02-Oct-1886', '    ', '    M', '   ', '', '    Farkas', '    ', '    ROTH Amalia', '   ', '', '    Csenger/28-02', '    ', '    Csenger', '    ', '    Szatmár', '   ', '', '    Porcsalma', '   ', '', '    father b. Beregszasz / mother b. Fulpos', '   ', '', '    LDS 642919 vol. 1', '    ', '', ''],
['', '', '', '     KRON', '    ', '    ,Rebeka', '   ', '', '    23-Sep-1885', '    ', '    F', '   ', '', '    Farkas', '    ', '    JOZSEF Eszter', '   ', '', '    Kisvarda/166-14', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Dombrad', '   ', '', '    Mother born Szoloskers', '   ', '', '    LDS 642905 Vol. 6', '    ', '', ''],
['', '', '', '     JOSEF...', '    ', '    ,Abraham Hirs', '   ', '', '    7-Mar-1875', '    ', '    M', '   ', '', '    David', '    ', '    Perl', '   ', '', '    Homonna/51-03', '    ', '    Homonna', '    ', '    Zemplén', '   ', '', '    Udva', '   ', '', '', '', '    LDS', '    ', '     1792090', '    ', '    , Item 2', '    ', '', ''],
['', '', '', '     JOSEF', '    ', '    ,Saye', '   ', '', '    10-Sep-1852', '    ', '    M', '   ', '', '    Elias', '    ', '    EHRENFELD Rebeka', '   ', '', '    Nyirbator/2-17', '    ', '    Nyir-Bator', '    ', '    Szabolcs', '   ', '', '    Nyirbator', '   ', '', '', '', '    LDS 642911, Vol 1', '    ', '', ''],
['', '', '', '     ALTMAN / JOSEPH', '    ', '    ,Samy', '   ', '', '    14-Jan-1854', '    ', '    M', '   ', '', '    Joseph / Mozes', '    ', '    HARTMAN Ele', '   ', '', '    Kisvarda/10-03', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kektse', '   ', '', '    Name might be reversed', '   ', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     JAKOB', '    ', '    ,Markusz', '   ', '', '    2-Apr-1854', '    ', '    M', '   ', '', '    Mozes', '    ', '    JOZSEF Leni', '   ', '', '    Kisvarda/149-10', '    ', '    Kis-varda', '    ', '    Szabolcs', '   ', '', '    Patrola', '   ', '', '', '', '    LDS 642905 Vol. 6', '    ', '', ''],
['', '', '', '     JOSEF', '    ', '    ,-', '   ', '', '    09-Oct-1853', '    ', '    M', '   ', '', '    David', '    ', '    SCHLESINGER Isabelle', '   ', '', '    Budapest/132-01', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     JOSEPH', '    ', '    ,Anton', '   ', '', '    26-May-1861', '    ', '    M', '   ', '', '    Medak', '    ', '    SCHWARZ Rosa', '   ', '', '    Budapest/220-10', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     JOSEPH', '    ', '    ,Isak', '   ', '', '    17-Jul-1853', '    ', '    M', '   ', '', '    Juda', '    ', '    BERNAT Leny', '   ', '', '    Kisvarda/9-10', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS 642904 Vol 3', '    ', '', ''],
['', '', '', '     JOSEPH', '    ', '    ,Hany', '   ', '', '    18-Jul-1853', '    ', '    F', '   ', '', '    Herman', '    ', '    BERNAT Hany', '   ', '', '    Kisvarda/9-11', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Doghe', '   ', '', '', '', '    LDS 642904 Vol 3', '    ', '', ''],
['', '', '', '     WEISS', '    ', '    ,Melach', '   ', '', '    15-Aug-1853', '    ', '    M', '   ', '', '    Herman', '    ', '    JOSEPH Fani', '   ', '', '    Kisvarda/9-21', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904 Vol 3', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     JOSEPH', '    ', '    ,David', '   ', '', '    01-Sep-1856', '    ', '    M', '   ', '', '    Juda', '    ', '    JOSEPH Leny', '   ', '', '    Kisvarda/19-15', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642904 Vol. 5', '    ', '', ''],

['', '', '', '     JOSEPH', '    ', '    ,Isak', '   ', '', '    17-Jul-1853', '    ', '    M', '   ', '', '    Juda', '    ', '    - Leni', '   ', '', '    Kisvarda/8-02', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Dighz?', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     JOSEPH', '    ', '    ,Hani', '   ', '', '    18-Jul-1853', '    ', '    F', '   ', '', '    Herman', '    ', '    BERNATH Hani', '   ', '', '    Kisvarda/8-03', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Karasz', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],

['', '', '', '     VEISZ', '    ', '    ,Melach', '   ', '', '    15-Aug-1853', '    ', '    M', '   ', '', '    Herman', '    ', '    JOSEPH Fany', '   ', '', '    Kisvarda/8-12', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],
['', '', '', '     JOSEPH', '    ', '    ,Ema', '   ', '', '    28-Aug-1851', '    ', '    F', '   ', '', '    Koralek', '    ', '    FLEISCHMAN Eva', '   ', '', '    Budapest/24-05', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     WEIN[BERGER]', '    ', '    ,Herman', '   ', '', '    13 Apr 1865', '    ', '    M', '   ', '', '    ?', '    ', '    YOSEF Fani', '   ', '', '    Ibrony/10-19', '    ', '    Bogdany', '    ', '    Szabolcs', '   ', '', '    Ibrony', '   ', '', '', '', '    LDS 642913', '    ', '', ''],
['', '', '', '     JOZEF', '    ', '    ,Peszel', '   ', '', '    ??-???-1833', '    ', '    F', '   ', '', '', '', '', '    Bodrogkeresztur/Feb-44', '    ', '    Tokai', '    ', '    Zemplén', '   ', '', '    Bodrogkeresztur', '   ', '', '', '', '    LDS 642952', '    ', '', ''],
['', '', '', '     JOSEPH', '    ', '    ,Majer Jacob', '   ', '', '    26-Aug-1860', '    ', '    M', '   ', '', '    Salamon', '    ', '    ROSENTZWEIG Rosalia', '   ', '', '    Satoraljaujhely/038-018', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Ujhely', '   ', '', '    Mohel: W. Grunfeld/Midwife: Rosi Kalmus', '   ', '', '    LDS 642954', '    ', '', ''],
['', '', '', '     -', '    ', '    ,Julis', '   ', '', '    06-Jul-1888', '    ', '    F', '   ', '', '    -', '    ', '    JOSEF Mari', '   ', '', '    Satoraljaujhely/372-008', '    ', '    Satoraljaujhely', '    ', '    Zemplén', '   ', '', '    Legenye', '   ', '', "    Mother's birthplace: Szokoly", '   ', '', '    LDS 642954', '    ', '', ''],

['', '', '', '     FLEISCH', '    ', '    ,Eugenie', '   ', '', '    12-May-1858', '    ', '    F', '   ', '', '    Albert', '    ', '    GOLDNER Rosalie', '   ', '', '    Budapest/23-02', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Oscar', '   ', '', '    22-Sep-1858', '    ', '    M', '   ', '', '    Leopold', '    ', '    FLESCH Fanni', '   ', '', '    Budapest/46-05', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     FLEISCH', '    ', '    ,Heinrich', '   ', '', '    19-Dec-1858', '    ', '    M', '   ', '', '    Salom', '    ', '    ROSENFELD Regine', '   ', '', '    Budapest/61-01', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Farkas', '   ', '', '    22-Apr-1860', '    ', '    M', '   ', '', '    Jacob', '    ', '    WEIT Johanna', '   ', '', '    Budapest/144-11', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Regina', '   ', '', '    26-Jun-1860', '    ', '    F', '   ', '', '    Philipp', '    ', '    FRIEDMAN Katharina', '   ', '', '    Budapest/159-01', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Benedict', '   ', '', '    13-Aug-1860', '    ', '    M', '   ', '', '    Max', '    ', '    NEUBERGER Isabella', '   ', '', '    Budapest/167-11', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 5', '    ', '', ''],
['', '', '', '     GELB', '    ', '    ,Julie', '   ', '', '    17-Jan-1861', '    ', '    F', '   ', '', '    Moritz', '    ', '    FLEISCH Anna', '   ', '', '    Budapest/193-13', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol.5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Ferdinand', '   ', '', '    17-Jun-1861', '    ', '    M', '   ', '', '    Jacob', '    ', '    VEIT Johanna', '   ', '', '    Budapest/226-09', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     SCHLESINGER', '    ', '    ,Mor', '   ', '', '    09-Oct-1884', '    ', '    M', '   ', '', '    Samu', '    ', '    VOROSVARI Babetta', '   ', '', '    Budapest/39-01', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', "    Father b Jekelfalva.  Witness:  Mihaly Vorosvari of Obuda.  Mor's surname changed to 'Szabolcs' (1908).", '   ', '', '    LDS 642968, Vol. 16', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Edvard', '   ', '', '    02-Mar-1851', '    ', '    M', '   ', '', '    Eduard', '    ', '    FLESCH Fani', '   ', '', '    Budapest/77-06', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol. 2', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Ida', '   ', '', '    06-Nov-1852', '    ', '    F', '   ', '', '    Leopold', '    ', '    FLESCH Fani', '   ', '', '    Budapest/82-10', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol.4', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     FLESCH', '    ', '    ,Albert', '   ', '', '    02-Apr-1853', '    ', '    M', '   ', '', '    Samuel', '    ', '    SCHREIBER Regina', '   ', '', '    Budapest/104-06', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Melani', '   ', '', '    18-Nov-1853', '    ', '    F', '   ', '', '    Leopold', '    ', '    FLESCH Fani', '   ', '', '    Budapest/138-05', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Adele', '   ', '', '    01-Feb-1855', '    ', '    F', '   ', '', '    Leopold', '    ', '    FLESCH Fanni', '   ', '', '    Budapest/203-07', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 4', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Fanni', '   ', '', '    20-Mar-1855', '    ', '    F', '   ', '', '    Philip', '    ', '    FRIEDMAN Cathi', '   ', '', '    Budapest/212-04', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962 Vol. 4', '    ', '', ''],
['', '', '', '     FLEISCH', '    ', '    ,Irma', '   ', '', '    20-Apr-1855', '    ', '    F', '   ', '', '    Albert', '    ', '    GOLDNER Rosalie', '   ', '', '    Budapest/217-05', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     FLEISCH', '    ', '    ,Catherine', '   ', '', '    29-Jun-1855', '    ', '    F', '   ', '', '    Samuel', '    ', '    GRANER Nanette', '   ', '', '    Budapest/228-01', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Caroline', '   ', '', '    02-Jan-1856', '    ', '    F', '   ', '', '    Mathias', '    ', '    HESS Rosa', '   ', '', '    Budapest/258-04', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Philip / Soloman', '   ', '', '    19-Feb-1850', '    ', '    M', '   ', '', '    Leopold', '    ', '    FLESCH Fanni', '   ', '', '    Budapest/265-09', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Josef', '   ', '', '    29-Mar-1857', '    ', '    M', '   ', '', '    Philipp', '    ', '    FRIEDMAN Catharine', '   ', '', '    Budapest/333-11', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 4', '    ', '', ''],
['', '', '', '     FLEISCH', '    ', '    ,Sidonie', '   ', '', '    25-Oct-1857', '    ', '    F', '   ', '', '    Salom. / [Salomon]', '    ', '    HASENFELD Regine', '   ', '', '    Budapest/367-09', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963, Vol.4', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     FLESCH', '    ', '    ,Moritz', '   ', '', '    27-Oct-1857', '    ', '    M', '   ', '', '    -', '    ', '    FLESCH Marie', '   ', '', '    Budapest/368-02', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642963, Vol.4', '    ', '', ''],
['', '', '', '     FLEISCH', '    ', '    ,Moritz', '   ', '', '    05-Feb-1858', '    ', '    M', '   ', '', '', '    FLESICH Nanette', '   ', '', '    Budapest/6-03', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642962, Vol. 5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Malvina', '   ', '', '    28-Feb-1891', '    ', '    F', '   ', '', '    Josef', '    ', '    KLEIN Fani', '   ', '', '    Polgar/18-02', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 2', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Margit', '   ', '', '    1-Jan-1893', '    ', '    F', '   ', '', '    Josef', '    ', '    KLEIN Fani', '   ', '', '    Polgar/23-04', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 2', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Frantzi', '   ', '', '    4-Feb-1894', '    ', '    F', '   ', '', '    Josef', '    ', '    KLEIN Fani', '   ', '', '    Polgar/28-03', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 2', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Jeno', '   ', '', '    28-Jun-1887', '    ', '    M', '   ', '', '    Josef', '    ', '    KLEIN Fani', '   ', '', '    Polgar/5-02', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 2', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Bernat', '   ', '', '    04-Jun-1864', '    ', '    M', '   ', '', '    Abraham', '    ', '    LANG Rezi', '   ', '', '    Szerencs/15-09', '    ', '    Szerencs', '    ', '    Zemplén', '   ', '', '    T.Lucz', '   ', '', '', '', '    LDS 642958', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record#', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image#', '   ', ''],
['', '', '', '     FLES', '    ', '    ,Devora', '   ', '', '    05-May-1868', '    ', '    F', '   ', '', '    Abraham', '    ', '    LANG Rezi', '   ', '', '    Szerencs/19-01', '    ', '    Szerencs', '    ', '    Zemplén', '   ', '', '    T. Lucz', '   ', '', '', '', '    LDS 642958', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Karoline', '   ', '', '    17-Sep-1841', '    ', '    F', '   ', '', '    Alois', '    ', '    PINKAS Luise', '   ', '', '    Budapest/77-12', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '    -', '   ', '', '    LDS 642961 Vol. 7', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Anton', '   ', '', '    07-Feb-1843', '    ', '    M', '   ', '', '    Alois', '    ', '    PINKAS Luise', '   ', '', '    Budapest/101-10', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol.1', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Joseph', '   ', '', '    28-Feb-1844', '    ', '    M', '   ', '', '    Alois', '    ', '    PINKAS Lise', '   ', '', '    Budapest/125-07', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol.1', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Alexander', '   ', '', '    04-Feb-1846', '    ', '    M', '   ', '', '    Alois', '    ', '    PINKAS Luise', '   ', '', '    Budapest/180-07', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol. 1', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Alfred', '   ', '', '    14-Apr-1848', '    ', '    M', '   ', '', '    Lipot', '    ', '    FLESCH Fanni', '   ', '', '    Budapest/29-06', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol.2', '    ', '', ''],
['', '', '', '     TAUB', '    ', '    ,Lajos', '   ', '', '    10-Jul-1849', '    ', '    M', '   ', '', '    Leopold', '    ', '    FLESCH Fani', '   ', '', '    Budapest/50-17', '    ', "    Local Gov't.", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '', '', '    LDS 642961, Vol.2', '    ', '', ''],
['', '', '', '     WEIS', '    ', '    ,Rosie', '   ', '', '    Jan-1812', '    ', '    F', '   ', '', '    Joseph', '    ', '    POLLAK Rosie', '   ', '', '    Illava/63', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobosiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Katty', '   ', '', '    Jun-1814', '    ', '    F', '   ', '', '    Hirschl', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/78', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Jeanett', '   ', '', '    Jan-1822', '    ', '    F', '   ', '', '    Isac', '    ', '    BUCHLER Mink', '   ', '', '    Illava/163', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Abraham', '   ', '', '    11-Mar-1822', '    ', '    M', '   ', '', '    Hirs', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/169', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Tobias Jacob', '   ', '', '    08-Dec-1823', '    ', '    M', '   ', '', '    Isak', '    ', '    BUCHLER Mindel', '   ', '', '    Illava/195', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Hany', '   ', '', '    Jan-1824', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mindel', '   ', '', '    Illava/199', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Lesko', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mayer Ber', '   ', '', '    01-Feb-1825', '    ', '    M', '   ', '', '    Juda', '    ', '    POLLAK Mary', '   ', '', '    Illava/212', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klucsov Kopez', '   ', '', '    Godparents or Witnesses: Moses Haas', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     NEUMAN', '    ', '    ,Isac Hirsch', '   ', '', '    Mar-1826', '    ', '    M', '   ', '', '    Noa', '    ', '    POLLAK Rachel', '   ', '', '    Illava/234', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Illava', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Baruch', '   ', '', '    12-Nov-1826', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/246', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLACK', '    ', '    ,Isak', '   ', '', '    27-Oct-1828', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/266', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Milli', '   ', '', '    4-Jul-1880', '    ', '', '', '    Josef', '    ', '    MUNK Juli', '   ', '', '    Polgar/24-13', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 1', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Eszter', '   ', '', '    17-Feb-1889', '    ', '    F', '   ', '', '    Josef', '    ', '    KLEIN Fani', '   ', '', '    Polgar/10-02', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 2', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Ignatz', '   ', '', '    12-Jun-1875', '    ', '    M', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/573', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Bernhard', '   ', '', '    24-Jun-1875', '    ', '    M', '   ', '', '    Herrman', '    ', '    POLLAK Tini', '   ', '', '    Bittse/576', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Heinrich', '   ', '', '    04-Dec-1876', '    ', '    M', '   ', '', '    Herman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/619', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Bertha', '   ', '', '    11-Apr-1877', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/636', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    twin', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Marie Irma', '   ', '', '    11-Apr-1877', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/637', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    twin', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Siegfried', '   ', '', '    23-Sep-1878', '    ', '    M', '   ', '', '    Herrmann', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/682', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Julie', '   ', '', '    26-Aug-1880', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/753', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Charlotte', '   ', '', '    01-Jul-1882', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilli', '   ', '', '    Bittse/808', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Leopold', '   ', '', '    27-Apr-1874', '    ', '    M', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/NONE', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    after #535, should be #536', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Isak', '   ', '', '    09-Feb-1800', '    ', '    M', '   ', '', '    Majer', '    ', '    Pessel', '   ', '', '    Illava/2', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Leskow', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Lobl', '   ', '', '    03-Jul-1806', '    ', '    M', '   ', '', '    Herman', '    ', '    LOWENBEIN Rosy', '   ', '', '    Illava/27', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Kockoviz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Lobl', '   ', '', '    07-Feb-1809', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBAUM Saly', '   ', '', '    Illava/45', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     FREUND', '    ', '    ,Elkan', '   ', '', '    05-Mar-1809', '    ', '    M', '   ', '', '    Bernad', '    ', '    POLLAK Zily', '   ', '', '    Illava/46', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Moritz', '   ', '', '    02-Jan-1837', '    ', '    M', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/417', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    g. Podrad', '   ', '', '    Godparents or Witnesses: Lobl Tauber', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Chany', '   ', '', '    07-Sep-1837', '    ', '    F', '   ', '', '    Lazar', '    ', '    POLLAK Fany', '   ', '', '    Illava/434', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Lobl/Leopold', '   ', '', '    07-Oct-1837', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/436', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Philipp', '   ', '', '    23-Oct-1838', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/464', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Franziska', '   ', '', '    29-Sep-1906', '    ', '    F', '   ', '', '    Gyula', '    ', '    SCHWARZ Henriette', '   ', '', '    Moson/177', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 35, born in Szentendre; mother 32, born in Pozsony', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mina', '   ', '', '    19-Feb-1865', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFER Katty', '   ', '', '    Bittse/213', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Marie', '   ', '', '    25-Jun-1867', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFER Katty', '   ', '', '    Bittse/301', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Leni', '   ', '', '    23-Nov-1870', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFR Katty', '   ', '', '    Bittse/414', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Felix', '   ', '', '    21-May-1872', '    ', '    M', '   ', '', '    Herrman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/473', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Herrmine', '   ', '', '    14-Aug-1872', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/482', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Theresie', '   ', '', '    22-Apr-1874', '    ', '    F', '   ', '', '    Herrman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/535', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Simon Leb', '   ', '', '    ?-?-1866', '    ', '    M', '   ', '', '    Abraham', '    ', '    LANG Rezi', '   ', '', '    Szerencs2/16-12', '    ', '    Szerencs3', '    ', '    Zemplén4', '   ', '', '    T. Lucz1', '   ', '', '', '', '    LDS 642958', '    ', '', ''],
['', '', '', '     SZABOLCS', '    ', '    ,Samuel', '   ', '', '    1-Dec-1857', '    ', '    M', '   ', '', '    -', '    ', '    - -', '   ', '', '    Kisvarda/18-16', '    ', '    Kis-Varda', '    ', '    Szabolcs', '   ', '', '    Kisvarda', '   ', '', '', '', '    LDS 642905, Vol. 6', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     NEUMAN', '    ', '    ,Rosi', '   ', '', '    Dec?-1828', '    ', '    F', '   ', '', '    Noa', '    ', '    POLLAK Rachel', '   ', '', '    Illava/269', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Illava', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Joseph', '   ', '', '    29-Sep-1829', '    ', '    M', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/276', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Herrman', '   ', '', '    25-Sep-1830', '    ', '    M', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/291', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Mina', '   ', '', '    Feb-1831', '    ', '    F', '   ', '', '    Lazar', '    ', '    POLLAK Fany', '   ', '', '    Illava/294', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mary', '   ', '', '    Feb-1832', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mina', '   ', '', '    Illava/310', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Chavia/Josef', '   ', '', '    13-Sep-1832', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/320', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Moses', '   ', '', '    18-Jul-1833', '    ', '    M', '   ', '', '    Lazar', '    ', '    POLLAK Hany', '   ', '', '    Illava/344', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '    Godparents or Witnesses: Joseph Roth', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Saly', '   ', '', '    Apr-1834', '    ', '    F', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/363', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Saly', '   ', '', '    May-1834', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mina', '   ', '', '    Illava/364', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Paulina', '   ', '', '    Aug-1834', '    ', '    F', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/374', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    g. Podhrad', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Samson', '   ', '', '    13-Mar-1836', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/400', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Herrman', '   ', '', '    15-Mar-1840', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/495', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Rosy', '   ', '', '    Jun-1841', '    ', '    F', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/520', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Dobra', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Nanetti', '   ', '', '    04-Aug-1841', '    ', '    F', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/524', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Podhrad', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     KACSER', '    ', '    ,Stefan', '   ', '', '    20-Dec-1841', '    ', '    M', '   ', '', '    Joseph', '    ', '    SCHLESINGR Betty', '   ', '', '    Illava/530', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Rovna', '   ', '', '    Godparents or Witnesses: Joseph Pollak', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image', '   ', ''],
['', '', '', '     FLESCH', '    ', '    ,Aladar', '   ', '', '    20-Dec-1876', '    ', '', '', '    Josef', '    ', '    H….K? July', '   ', '', '    Polgar/18-06', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 1', '    ', '', ''],
['', '', '', '     STEINER', '    ', '    ,Herman', '   ', '', '    29-May-1857', '    ', '    M', '   ', '', '    Marton', '    ', '    FLEISCH Rozalia', '   ', '', '    Kecskemet/97-17', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Kecskemet', '   ', '', '', '', '    LDS 642857, Vol. 1', '    ', '', ''],
['', '', '    Name', '   ', '', '    Date of Birth', '    ', '    Sex', '   ', '', '    Father', '    ', '    Mother', '   ', '', '    TownRegistered / Record', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Town Born', '   ', '', '    Comments', '   ', '', '    Source (Film/Item)', '    ', '    Image', '   ', ''],
['', '', '', '     FLESCH', '    ', '    ,Zali', '   ', '', '    28-Apr-1875', '    ', '    F', '   ', '', '    Jozef', '    ', '    MU….? July', '   ', '', '    Polgar/15-09', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '', '', '    LDS 642916, Vol. 1', '    ', '', ''],
['', '', '', '     GRUNBAUM', '    ', '    ,Amalia', '   ', '', '    19-Apr-1865', '    ', '    F', '   ', '', '    Marczell / Mordechai', '    ', '    FARKAS-FRIEDLANDER Pepi / Perl', '   ', '', '    Hajdunanas/197-016', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', '    Hajdunanas', '   ', '', "    Marriage date: '04-Jul-1886/Year of death: 1944/Listed in Yad Vashem database as Gelberger Amalia father 37, born in M. Szolnok; mother 25, born in Csottokva Somorja", '   ', '', '    LDS 642810', '    ', '', ''],
['', '', '', '     SINGER', '    ', '    ,Gyorgy / Odon', '   ', '', '    17-Jan-1890', '    ', '    M', '   ', '', '    Sandor', '    ', '    SCHON Jenny / Sarolta', '   ', '', '    Budapest/240-02', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Pest', '   ', '', '    Mother b. Pest / Name changed to SZABOLCS in 1907', '   ', '', '    LDS 642970, Vol. 19', '    ', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Jeno', '   ', '', '    6-Dec-1878', '    ', '    M', '   ', '', '    Josef', '    ', '    MUNK July', '   ', '', '    Polgar/22-07', '    ', '    Dada Also', '    ', '    Szabolcs', '   ', '', '    Polgar', '   ', '', '    Died 16-Jul-1879; See Deaths, V.1, 37-07', '   ', '', '    LDS 642916, Vol. 1', '    ', '', ''],
['', '', '', '     KRAUSZ', '    ', '    ,Moritz', '   ', '', '    07-Feb-1886', '    ', '    M', '   ', '', '    Samuel', '    ', '    FARKAS Roza', '   ', '', '    Nyiregyhaza/133-013', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Father's birthplace: Mathe-Szalka, Szabol./Mother's birthplace: Kotaj, Szabolcs/Midwife: Yetti KOHN/Mohel's name and circumcision date: 15-Feb-1886 - Armin KRONENWIRTH/Witness: Salamon BIDERMANN", '   ', '', '    LDS 642913', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FARKAS', '    ', '    ,Sandor', '   ', '', '    14-Feb-1886', '    ', '    M', '   ', '', '    Peter', '    ', '    LAZAR Roza', '   ', '', '    Nyiregyhaza/133-016', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Father's birthplace: Nyiregyhaza/Mother's birthplace: Kotaj, Szabolcs/Midwife: Borbala WEISZ/Mohel's name and circumcision date: 21-Feb-1886 - Armin KRONENWIRTH/Witness: Ignatz SCHONBERGER", '   ', '', '    LDS 642913', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SZAMUELI', '    ', '    ,Marton', '   ', '', '    12-Jun-1886', '    ', '    M', '   ', '', '    Lajos', '    ', '    FARKAS Czeczilia', '   ', '', '    Nyiregyhaza/135-038', '    ', "    Local Gov't.", '    ', '    Szabolcs', '   ', '', '    Nyiregyhaza', '   ', '', "    Father's birthplace: B.Szt Mihaly, Szabol/Mother's birthplace: Nyiregyhaza/Midwife: Borbala WEISZ/Mohel's name and circumcision date: 20-Jun-1886 - Armin KRONENWIRTH/Witness: Ignatz SCHONBERGER", '   ', '', '    LDS 642913', '    ', '', ''],
['', '', '', '     WEISS', '    ', '    ,Janka', '   ', '', '    05-Nov-1903', '    ', '    F', '   ', '', '    Jakab', '    ', '    FLESCH Matild', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father born in Moson1; merchant, mother 30, born in Moson2', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     STADLER', '    ', '    ,Anna', '   ', '', '    20-Dec-1903', '    ', '    F', '   ', '', '    Jakab', '    ', '    FLESCH Riza', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father born in Moson1; mother 34, born in Moson2', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     STADLER', '    ', '    ,Dora', '   ', '', '    03-Mar-1899', '    ', '    F', '   ', '', '    Jakab', '    ', '    FLESCH Riza', '   ', '', '    Moson/28', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 41, born in Moson; mother 30, born in Moson', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Erzsebeth', '   ', '', '    15-Nov-1898', '    ', '    F', '   ', '', '    Jakab', '    ', '    FLESCH Matild', '   ', '', '    Moson/192', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 32, born in Moson; mother 24, born in Moson', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     SCHAY', '    ', '    ,Dorottya', '   ', '', '    11-Aug-1898', '    ', '    F', '   ', '', '    Bernat', '    ', '    FLESCH Hanne', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 55, born in Boldogassony; mother 28, born in Mososn', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     SCHAY', '    ', '    ,Jozsef', '   ', '', '    30-May-1900', '    ', '    M', '   ', '', '    Bernat', '    ', '    FLESCH Hanni', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 57, born in Boldogassony; mother 30, born in Moson', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Izabella', '   ', '', '    30-May-1901', '    ', '    F', '   ', '', '    Jakab', '    ', '    FLESCH Matild', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 35, born in Moson; mother 27, born in Moson', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     SCHAY', '    ', '    ,Hilda', '   ', '', '    16-Dec-1901', '    ', '    F', '   ', '', '    Bernat', '    ', '    FLESCH Hanny', '   ', '', '    Moson/', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 58, born in Boldogassony; mother 31, born in Moson', '   ', '', '    LDS', '    ', '     2343386', '    ', '', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Ella', '   ', '', '    28-Oct-1911', '    ', '    F', '   ', '', '    Aron David', '    ', '    TOPF Anna', '   ', '', '    Moson/167', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 33, mother 28', '   ', '', '    LDS', '    ', '     2343388', '    ', '', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Simon Leb', '   ', '', '    ?-?-1866', '    ', '    M', '   ', '', '    Abraham', '    ', '    LANG Rezi', '   ', '', '    Szerencs/16-12', '    ', '    Szerencs', '    ', '    Zemplén', '   ', '', '    T. Lucz', '   ', '', '', '', '    LDS 642958', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Otto', '   ', '', '    04-Jun-1905', '    ', '    M', '   ', '', '    Gyula', '    ', '    SCHWARZ Henriette', '   ', '', '    Moson/130', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 34, born in St. Endre; mother 32, born in Poszony', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Franziska', '   ', '', '    29-Sep-1906', '    ', '    F', '   ', '', '    Gyula', '    ', '    SCHWARZ Henriette', '   ', '', '    Moson/177', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Moson', '   ', '', '    father 35, born in Szentendre; mother 32, born in Pozsony', '   ', '', '    LDS', '    ', '     2343387', '    ', '', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mina', '   ', '', '    19-Feb-1865', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFER Katty', '   ', '', '    Bittse/213', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Marie', '   ', '', '    25-Jun-1867', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFER Katty', '   ', '', '    Bittse/301', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Leni', '   ', '', '    23-Nov-1870', '    ', '    F', '   ', '', '    Ignatz', '    ', '    LEIMDORFR Katty', '   ', '', '    Bittse/414', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Felix', '   ', '', '    21-May-1872', '    ', '    M', '   ', '', '    Herrman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/473', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Herrmine', '   ', '', '    14-Aug-1872', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/482', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Theresie', '   ', '', '    22-Apr-1874', '    ', '    F', '   ', '', '    Herrman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/535', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Ignatz', '   ', '', '    12-Jun-1875', '    ', '    M', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/573', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Bernhard', '   ', '', '    24-Jun-1875', '    ', '    M', '   ', '', '    Herrman', '    ', '    POLLAK Tini', '   ', '', '    Bittse/576', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittse', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Heinrich', '   ', '', '    04-Dec-1876', '    ', '    M', '   ', '', '    Herman', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/619', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Bertha', '   ', '', '    11-Apr-1877', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/636', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    twin', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Marie Irma', '   ', '', '    11-Apr-1877', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/637', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    twin', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     LEIMDORFER', '    ', '    ,Siegfried', '   ', '', '    23-Sep-1878', '    ', '    M', '   ', '', '    Herrmann', '    ', '    POLLAK Ernestine', '   ', '', '    Bittse/682', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Bittsche', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Julie', '   ', '', '    26-Aug-1880', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/753', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Charlotte', '   ', '', '    01-Jul-1882', '    ', '    F', '   ', '', '    Eduard', '    ', '    KUGEL Cilli', '   ', '', '    Bittse/808', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Leopold', '   ', '', '    27-Apr-1874', '    ', '    M', '   ', '', '    Eduard', '    ', '    KUGEL Cilly', '   ', '', '    Bittse/NONE', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    Papradna', '   ', '', '    after #535, should be #536', '   ', '', '    LDS 1978900(4)', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Isak', '   ', '', '    09-Feb-1800', '    ', '    M', '   ', '', '    Majer', '    ', '    Pessel', '   ', '', '    Illava/2', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Leskow', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Lobl', '   ', '', '    03-Jul-1806', '    ', '    M', '   ', '', '    Herman', '    ', '    LOWENBEIN Rosy', '   ', '', '    Illava/27', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Kockoviz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Lobl', '   ', '', '    07-Feb-1809', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBAUM Saly', '   ', '', '    Illava/45', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     FREUND', '    ', '    ,Elkan', '   ', '', '    05-Mar-1809', '    ', '    M', '   ', '', '    Bernad', '    ', '    POLLAK Zily', '   ', '', '    Illava/46', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     WEIS', '    ', '    ,Rosie', '   ', '', '    Jan-1812', '    ', '    F', '   ', '', '    Joseph', '    ', '    POLLAK Rosie', '   ', '', '    Illava/63', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobosiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Katty', '   ', '', '    Jun-1814', '    ', '    F', '   ', '', '    Hirschl', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/78', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Jeanett', '   ', '', '    Jan-1822', '    ', '    F', '   ', '', '    Isac', '    ', '    BUCHLER Mink', '   ', '', '    Illava/163', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Abraham', '   ', '', '    11-Mar-1822', '    ', '    M', '   ', '', '    Hirs', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/169', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Tobias Jacob', '   ', '', '    08-Dec-1823', '    ', '    M', '   ', '', '    Isak', '    ', '    BUCHLER Mindel', '   ', '', '    Illava/195', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Hany', '   ', '', '    Jan-1824', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mindel', '   ', '', '    Illava/199', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Lesko', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mayer Ber', '   ', '', '    01-Feb-1825', '    ', '    M', '   ', '', '    Juda', '    ', '    POLLAK Mary', '   ', '', '    Illava/212', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klucsov Kopez', '   ', '', '    Godparents or Witnesses: Moses Haas', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     NEUMAN', '    ', '    ,Isac Hirsch', '   ', '', '    Mar-1826', '    ', '    M', '   ', '', '    Noa', '    ', '    POLLAK Rachel', '   ', '', '    Illava/234', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Illava', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Baruch', '   ', '', '    12-Nov-1826', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/246', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLACK', '    ', '    ,Isak', '   ', '', '    27-Oct-1828', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/266', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     NEUMAN', '    ', '    ,Rosi', '   ', '', '    Dec?-1828', '    ', '    F', '   ', '', '    Noa', '    ', '    POLLAK Rachel', '   ', '', '    Illava/269', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Illava', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Joseph', '   ', '', '    29-Sep-1829', '    ', '    M', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/276', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusitz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Herrman', '   ', '', '    25-Sep-1830', '    ', '    M', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/291', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Mina', '   ', '', '    Feb-1831', '    ', '    F', '   ', '', '    Lazar', '    ', '    POLLAK Fany', '   ', '', '    Illava/294', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Mary', '   ', '', '    Feb-1832', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mina', '   ', '', '    Illava/310', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Chavia/Josef', '   ', '', '    13-Sep-1832', '    ', '    M', '   ', '', '    Hirsch', '    ', '    GRUNBLATT Saly', '   ', '', '    Illava/320', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Moses', '   ', '', '    18-Jul-1833', '    ', '    M', '   ', '', '    Lazar', '    ', '    POLLAK Hany', '   ', '', '    Illava/344', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '    Godparents or Witnesses: Joseph Roth', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Saly', '   ', '', '    Apr-1834', '    ', '    F', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/363', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Saly', '   ', '', '    May-1834', '    ', '    F', '   ', '', '    Isak', '    ', '    BUCHLER Mina', '   ', '', '    Illava/364', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Slopna', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Paulina', '   ', '', '    Aug-1834', '    ', '    F', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/374', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    g. Podhrad', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Samson', '   ', '', '    13-Mar-1836', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/400', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Moritz', '   ', '', '    02-Jan-1837', '    ', '    M', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/417', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    g. Podrad', '   ', '', '    Godparents or Witnesses: Lobl Tauber', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Chany', '   ', '', '    07-Sep-1837', '    ', '    F', '   ', '', '    Lazar', '    ', '    POLLAK Fany', '   ', '', '    Illava/434', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Tepliz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Lobl/Leopold', '   ', '', '    07-Oct-1837', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/436', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Philipp', '   ', '', '    23-Oct-1838', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/464', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     MARER', '    ', '    ,Herrman', '   ', '', '    15-Mar-1840', '    ', '    M', '   ', '', '    Joseph', '    ', '    POLLAK Katty', '   ', '', '    Illava/495', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Klobusiz', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Rosy', '   ', '', '    Jun-1841', '    ', '    F', '   ', '', '    Lobl', '    ', '    WEIS Rosy', '   ', '', '    Illava/520', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Dobra', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Nanetti', '   ', '', '    04-Aug-1841', '    ', '    F', '   ', '', '    Joseph', '    ', '    TAUBER Hany', '   ', '', '    Illava/524', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Podhrad', '   ', '', '', '', '    LDS 1981155, item 5', '    ', '', ''],
['', '', '', '     KACSER', '    ', '    ,Stefan', '   ', '', '    20-Dec-1841', '    ', '    M', '   ', '', '    Joseph', '    ', '    SCHLESINGR Betty', '   ', '', '    Illava/530', '    ', '    Illava', '    ', '    Trencsén', '   ', '', '    Rovna', '   ', '', '    Godparents or Witnesses: Joseph Pollak', '   ', '', '    LDS 1981155, item 5', '    ', '', ''],
]
