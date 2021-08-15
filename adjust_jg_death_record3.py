import re
from dateutil.parser import parse
from adjust_jg_birth_record1 import *
import datetime as dt

none = re.search("xxx", "") #set the value for re.search = none

# here we had def is_date(string, fuzzy=False):

#JG Death records
jg_d_input = [

]

empty_list = [
]


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
        return date[-4:] # return 4 last chars - assuming this is the year
# cannot use the same function from Birth build because the INT


#adjust JG Death - one list/line at a time
def adjust_jg_death(row, data_out):

    row_idx = 3
    #Surename [0]
    data_out.append(row[row_idx].strip())
    row_idx += 2

    #given name [1]
    data_out.append(re_comma2space(row[row_idx]).strip())
    row_idx += 3

    #Father name field [2] expected in input offset 8
    data_out.append(row[row_idx].strip())
    if data_out[-1] in ["-", '', "--"]:
        data_out[-1] = 'noFather'
    if not row[row_idx]:
        row_idx -= 1
    row_idx += 2

    #Mother and Maiden [3], [4] expected in input offset 10 (one field to be divided)
    row[row_idx] = row[row_idx].strip()
    if row[row_idx] in ["", "-", "- -", "--", "-- --"]:
        data_out.append('noMother')
        if row[row_idx]:
            row_idx += 1
#           print("check", row[8: row_idx+3], row_idx)
    else:
        data_out.append(row[row_idx].strip()) #add element for mothers Surename
        data_out.append(data_out[-1][data_out[-1].find(' ')+1:]) #add element for mothers name
        data_out[-2] = data_out[-2][:data_out[-2].find(' ')]
        row_idx += 1

    row_idx += 2
    # record# [5]
    data_out.append(row[row_idx].strip())
    if data_out[-1] == "":
        row_idx -= 1
    row_idx += 2

    #Death date [6]
    if row[row_idx].strip() == "":
        row_idx += 1
    data_out.append(row[row_idx].strip())

    #Age at Death [7]
    row_idx += 2

    if row[row_idx].strip() == '':
        data_out.append("noAge")
        row_idx += 1
    else:
        data_out.append(row[row_idx].strip())
        row_idx += 1

    # other family [8]
    row_idx += 1
    if row[row_idx] == "":
        row_idx += 1
    data_out.append(row[row_idx].strip())

    if data_out[-1] in ["", "-"]:
        if data_out[-1] in [""]:
            row_idx -= 1
        data_out[-1] = "noFam"
        row_idx -= 1

    test1 = row[row_idx]

    #town data [9:12]
    row_idx += 3
    # check for "" fields
    if row[row_idx] in ["", " "]:
        test1 = row[row_idx]
        data_out.append("NoTown")
        row_idx += 1
    else:
        data_out.append(row[row_idx].strip())
        row_idx += 2

    if row[row_idx] in ["", " "]:
        test1 = row[row_idx]
        data_out.append("NoTown")
        row_idx += 1
    else:
        data_out.append(row[row_idx].strip())
        row_idx += 2

    if row[row_idx] in ["", " "]:
        test1 = row[row_idx]
        data_out.append("NoTown")
        row_idx += 1
    else:
        data_out.append(row[row_idx].strip())
        row_idx += 2

    if row[row_idx] in ["", " "]:
        test1 = row[row_idx]
        data_out.append("NoTown")
        row_idx += 1
    else:
        data_out.append(row[row_idx].strip())
        row_idx += 3

    #comment field [13]
    data_out.append(row[row_idx]) # dont strip() the comment as it effects patterns like " b " for town born
    if data_out[-1] == '':
        data_out[-1] = "noComment"
        row_idx -= 1

    # source + record + Image details [14]; check for different schemes
    row_idx += 3
#    print("here we go: ", data_out)
    data_out.append(row[row_idx].strip() + " " + row[row_idx+2].strip())
    if len(row) < row_idx + 4:
         data_out[-1] += "#" + data_out[5]
         #row[row_idx+4].strip()

    return

#Done
def extract_family_relation_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split("[,/;]", data)

    for item in comment_split:
        if "wife of" in item.lower():
            return "Husband"
        elif "husband of" in item.lower() or "wife" in item.lower():
            return "Wife"
        elif "widow of" in item.lower():
            return "Widow"
        elif "widower" in item.lower():
            return "Widower"
        elif "unmarried" in item.lower():
            return "Unmarried"
        elif "deceased" in item.lower():
            if "parents" in item.lower():
                return "Parents Deceased"
            elif "father" in item.lower():
                return "Father Deceased"
            elif "other" in item.lower():
                return "Mother Deceased"
        elif "married" in item.lower():
            return "Married"

    return "noFamR"


#Done
def extract_other_family_from_comment(data):
    comment_split = re.split("[,/;.]", data)
    for item in comment_split:
        item_lower = item.lower()
        if "wife of" in item_lower or "husband of" in item_lower or "widow of" in item_lower:
            if "maiden" in item.lower():
                return item[item.find("of") + 3:item.find("aiden")-1].strip()
            elif " in " in item:
                return item[item.find("of") + 3:item.find(" in ")].strip()
            else:
                item = re.sub("nee ", "", item)
                return item[item.find("of") + 3:].strip()
        elif "nee" in item.lower():
            find_nee = item.find("nee ")
            word_after = item[find_nee + 4:]
            return word_after.strip()
    return "noFam"


#DONE
def set_other_family(family, family_relation):
    family_lower = family.lower()
    if "wife" in family_lower:
        family = re.sub("\wife", "", family).strip()
        return (family, "Wife")
    elif "hsband" in family_lower:
        family = re.sub("\wusband", "", family).strip()
        return (family, "Husband")
    elif "spouse" in family_lower:
        family = re.sub("\wpouse", "", family).strip()
        return (family, "Spouse")
    elif "daughter" in family_lower:
        family = re.sub("\waughter", "", family).strip()
        return (family, "Daughter")
    elif "son" in family_lower:
        family = re.sub("\won", "", family).strip()
        return (family, "Son")
    else:
        return family, "noFamR"


#DONE
def extract_age_from_comment(data):
    data_lower = data.lower().strip()
#if infant found - return infant
    if "infant" in data_lower:
        return "Infant"
    elif "stillborn" in data_lower:
        return "Stillborn"
    elif "under 1" in data_lower:
        return 0

#search in each comment portion, order is not guranteed
    data = re_sub_slash2comma(data)
    comment_split = re.split("[,/;]", data.strip())
    for item in comment_split:
        item_split = re.split(" ", item)
        if item_split[0].isdigit() and len(item_split) == 1:
            return (item_split[0])
        elif len(item_split) == 1:
            return check_for_age(item_split[0])
        elif item_split[1] in ["y", "yrs", "years", "Y", "Yrs", "Years"]:
            return item_split[0]
        elif item_split[1] in ["mon", "Mon", "months", "Month", "Months", "months", "mo", "Mo", "Days", "Day", "day", "days", "hours", "Hours"]:
            return 0 #less than 1 Year

        # look for age or Age then clean all NONE digits
        if "age" in item.lower():
            if "age at death" in item.lower():
                return check_for_age(item_split[3])
#                if item_split[4] in ["y", "yrs", "years", "Y", "Yrs", "Years", "year", "Year"]:
#                    return item_split[3]
            elif item_split[1:2] in ["mon", "Mon", "months", "Month", "Months", "months", "mo", "Mo", "Days", "Day",
                                     "day",
                                     "days", "hours", "Hours"]:
                return 0  # less than 1 Year
            elif "mo" in item:
                return 0
            else:
                item = re_sub_minus(item)
            # check for y:m:d format ; should NOT have "mon" and NOT "day"
            if ("mon" not in item.lower()) and ("day" not in item.lower()):
                item = re.sub("[.\-;:]", "", item)

                first_digit = re.search("\d", item)
                if first_digit != none:
                    start_digit = first_digit.start()
                    # assuming age cannot be DDD - 3 digits
                    return item[start_digit: start_digit + 2].strip()
                else:
                    return "noAge"
            else:
                return 0

        #can be only number
        elif item.isdigit():
            return item
    return "noAge"


def check_for_age(item):
    # look for age or Age then clean all NONE digits
    if "age" in item.lower():
        if "age at death" in item.lower():
            if item in ["y", "yrs", "years", "Y", "Yrs", "Years", "year", "Year"]:
                return item
        elif item in ["mon", "Mon", "months", "Month", "Months", "months", "mo", "Mo", "Days", "Day", "day",
                                 "days", "hours", "Hours"]:
            return 0  # less than 1 Year
        elif "mo" in item:
            return 0
        else:
            item = re_sub_minus(item)
        # check for y:m:d format ; should NOT have "mon" and NOT "day"
        if ("mon" not in item.lower()) and ("day" not in item.lower()):
            item = re.sub("[.\-;:]", "", item)

            first_digit = re.search("\d", item)
            if first_digit != none:
                start_digit = first_digit.start()
                # assuming age cannot be DDD - 3 digits
                return item[start_digit: start_digit + 2].strip()
            else:
                return "noAge"
        else:
            return 0
    return "noAge"


#DONE
def extract_town_born_from_comment(data):
#search in each comment portion, order is not guranteed, split per commnet
    data = re_sub_colon(data)
    data = re_sub_slash2comma(data)
    town = "noTB"

    comment_split = re.split("[,;]", data)
    for item in comment_split:
        item_lower = item.lower()
#look for Born or born
        if "born in" in item_lower:
            town = item[item.find("in ")+3:]
            townb = town.find("  ")
            if townb == -1:
                town = adjust_town_born(town)
            else:
                town = adjust_town_born(town[: townb].strip())
        elif "b." in item_lower:
            town =  item[item.find(". ")+2:].strip()
        elif " b " in item_lower:
            item = item.strip()
            town =  item[item.find(" ") + 1:].strip()
        elif "place of birth" in item_lower:
            town = item[item.find("irth") + 5:].strip()
        elif "from/b" in item_lower:
            town =  item[item.find("/b") + 3:].strip()
        elif "from " in item_lower:
            town =  item[item.find("rom ") + 4:].strip()
        else:
            continue

        if town.find("eport") != -1: # case comment is like "father born <place>. Father/Mother died..." or "... Died..." or "... reported..."
                                     # comment can have ALL 3 items and not seperated. assuming "report" is first to appear etc.
            town = town[: town.find("eport") - 2]
        elif town.find("ied ") != -1:
            town = town[: town.find("ied") - 1]
        elif town.find("ther ") != -1:
            town = town[: town.find("ther") - 2]

        return town.strip()



def adjust_town_born(data):
    # case of <place>. Residence... since place can have "."
    if "esidence" in data:
        data = data[:data.find("esidence")-2]
        return re_sub_dot(data).strip()
    else:
        return data


#DONE
def extract_maiden_from_comment(data):
#search in each comment portion, order is not guranteed

    comment_split = re.split("[,/;.]", data)
    data = re_sub_dot(data)
    data = re_sub_colon(data)

    for item in comment_split:
        item_lower = item.lower()
        if "maiden name" in item_lower:
            item = item[item.find("name ")+5:].strip().upper()
            item = item.split()[0].replace(".", '')
            return item
        if "nee" in item_lower:
            item = item[item.find("nee ") + 4:].strip().upper()
            item = item.split()[0].replace(".", '')
            return item
    return "noMaiden"


#DONE - no real effect
def insert_jg_death_fields(row):
    maiden_idx = 2
    dd_idx = 7
    dyear_idx = 8
    age_idx = 9
    birth_date_idx = 10
    family_idx = 12
    otherfamrelation = 13
    town_born_idx = 14
    change_name_idx = 20

    row.insert(maiden_idx,"noMaiden")
    row.insert(age_idx,"noBY") #estimated Birth year
    row.insert(dyear_idx, year_from_date(row[dd_idx]))  # year of death from dd
    row.insert(birth_date_idx,"noBD")
    row.insert(otherfamrelation, "noFamR")
    row.insert(town_born_idx,"noTownB")
    row.insert(change_name_idx, "noCName")

    return



def update_comment_result(data, comment_result):
    maiden_idx = 2
    age_idx = 9
    birth_date_idx = 10
    estimated_byear_idx = 11
    family_idx = 12
    family_relation = 13
    town_born_idx = 14
    change_name_idx = 20

    # 0 - maiden, 1 - AgeAtDeath, 2 - Birth Year, 3 - Birth Date, 4 - Family, 5 - Family Relation, 6 - Town Born, 7 - Change Name

    data[maiden_idx] = comment_result[0]            # Maiden - not included in original fields

    if data[age_idx] == "noAge":                    # Age At Death
        data[age_idx] = comment_result[1]
    data[estimated_byear_idx] = comment_result[2]   # Birth Year(estimated or from comment) - not included in original fields
    data[birth_date_idx] = comment_result[3]        # Birth Date - not included in original fields

    data[family_relation] = comment_result[5]       # Other Family relation - not included in original fields

    data[family_idx] = merge_family_data(data[family_idx], comment_result[4])

    if data[town_born_idx] == "noTownB":            # Town Born
        data[town_born_idx] = comment_result[6]
    data[change_name_idx] = comment_result[7]       # Change Name - not included in original fields
    return


def merge_family_data(str1, str2):
    if "noFam" in str1:
        return str2
    elif "noFam" in str2:
        return str1

    str_split = re.split("[/ ]", str2)
    for item in str_split:
        if item not in str1: # item from base found in comment result
            str1 = str1 + " " + item
    return str1


def parse_comment(comment, comment_result):
    comment_split = re.split("[,/;]", comment) # split by period, slash or semicolon
    for item in comment_split:
        parse_comment_item(item, comment_result)
    return



def parse_comment_item(item, comment_result):
    # check the following fields: <data type> in comment will show as <pattern> / process
    ## Maiden name - <surename> / UPPER
    ## Age at Death - number of years / extract number of years. using the former extract_age _from_comment method
    #   can appear as:
    #   <number>, <number> [ y, yrs, years, m, mon, month, months, d, day, days],
    #   <number>-<number> [-<number>], <number>:<number> [:<number>]
    #   age , age=, age:,
    ##   under 1 year, infant, stillborn
    ## Birth_year - date of birth: <year> or derived from Birth_date
    ## Birth_date - date of birth: <date>
    # Other Family :
    #       her parents are both deceased, parents in America, father innkeeper (occupation)
    #       wife: nee <surename>
    #       wife of <name> <surename>
    #       husband of <name> nee <surename>
    #       bachelor, married, not married, unmarried, married to <name> <surename>
    #       widower, widow of <name>
    #       grandfather <name>
    ## Town Born - Place of birth: <place> , in, b., from, born, born in
    ## Change Name - change name <name>
    # Others - Hebrew name <name>

    if comment_result[0] == "noMaiden":
        comment_result[0] = extract_maiden_from_comment(item)

    if comment_result[1] == "noAge":
        comment_result[1] = extract_age_from_comment(item)

    bd_pattern = "ate of birth" # date of birth
    find_pattern = item.find(bd_pattern)
    if find_pattern != -1:
        comment_result[3] = item[item.find(bd_pattern) + len(bd_pattern) + 2:].strip().replace("'", "")
        comment_result[2] = comment_result[3][-4:] # year only

    if comment_result[4] == "noFam":
        comment_result[4] = extract_other_family_from_comment(item)
        if comment_result[4].lower() == comment_result[0].lower(): #in case we already got the same "nee" <surename>
            comment_result[4] = "noFam"
    if comment_result[5] == "noFamR":
        comment_result[5] = extract_family_relation_from_comment(item)

#TODO case of "merchant from <place> wife maiden <name>. since no seperators - place will be taken to the end of the line
    #maybe can cut the original "data" item with what we already extracted. can harm other scenarios

    if comment_result[6] == "noTB":
        comment_result[6] = extract_town_born_from_comment(item)

    change_pattern = "hange name"
    
    find_pattern = item.find(change_pattern)
    if find_pattern != -1:
        comment_result[7] = item[item.find(change_pattern)+len(change_pattern):].strip().upper()
    return


def build_jg_death(data, data_out):
    idx = 0
    record_num_idx = 6
    family_idx = 12
    family_relation_idx = 13
    comment_idx = 19

# for each line in input - check if relevant and process
    for row in data:
        if ignore_jg_lines(row):
            continue
        adjust_jg_death(row, data_out[idx]) # adjust relevant line
        insert_jg_death_fields(data_out[idx]) #insert elements to full size of row
        data_out[idx][family_idx], data_out[idx][family_relation_idx] = set_other_family(data_out[idx][family_idx], data_out[idx][family_relation_idx])

        # 0 - maiden, 1 - AgeAtDeath, 2 - Birth Year, 3 - Birth Date, 4 - Family, 5 - Family Relation, 6 - Town Born, 7 - Change Name
        comment_result = ["noMaiden", "noAge", "noBD", "noDD", "noFam", "noFamR", "noTB", "noCName"]
        if "noComment" not in data_out[idx][comment_idx]:
            parse_comment(data_out[idx][comment_idx], comment_result)  # extract data from comment
            update_comment_result(data_out[idx], comment_result)

        data_out[idx][comment_idx] = data_out[idx][comment_idx].strip()
        del data_out[idx][record_num_idx]
        #prepare for next line
        idx += 1
#        print("record number", idx)
        data_out.append([])
    del data_out[idx]
    return

