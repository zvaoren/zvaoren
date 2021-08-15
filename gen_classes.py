#trying here to adjust the dtah records AFTER cleaning its nulss and spaces - by a comprehension loop
# the issue is that missing fields are not alaways there and there is no way to identify the content of te field
# moving back to the code with no basic cleaning


from clean_jg_input import clean_jg_inp
import resub

import re


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


def re_sub_dot(data):
    return re.sub("\.", " ", data)


def re_sub_slash2comma(data):
    return re.sub("/", ",", data)



#JG Death records
jg_d_input = [
['', '', '', '     FLESCH', '    ', '    ,Juli', '   ', '', '', '', '', '    301-10', '    ', '    08-Sep-1874', '    ', '', '', '', '', '    Rajka', '    ', '    Rajka', '    ', '    Rajka', '    ', '    Moson', '   ', '', '    age 2 1/2, born in Rajka', '   ', '', '    LDS', '    ', '     691569', '    ', '', ''],
['', '', '', '     LOTH', '    ', '    ,Mathild', '   ', '', '    -', '    ', '    - -', '   ', '', '    24-03', '    ', '    08-Aug-1893', '    ', '    39', '   ', '', '    Arnold', '   ', '', '    Pozsony', '    ', '    Pozsony', '    ', "    Local Gov't", '    ', '    Pozsony', '   ', '', '    b. Hartford USA / wife of Arnold FLESCH', '   ', '', '    LDS 2442344 Item 5', '   ', ''],
['', '', '', '     ROSENBERG', '    ', '    ,Erzsebet', '   ', '', '    -', '    ', '    - -', '   ', '', '    176-07', '    ', '    14-May-1934', '    ', '    59', '   ', '', '', '', '    Bratislava', '    ', '    Pozsony', '    ', "    Local Gov't", '    ', '    Pozsony', '   ', '', '    b. Bregova Nyjava, wife of FLESCH', '   ', '', '    LDS 2442344 Item 5', '   ', ''],
]

class jg_bmd():
    #define basic class for JG BMD records
    def __init__(self, input_list):
        self.surename = input_list[0]
        self.given = input_list[1]
        self.changename = input_list[3]
        self.father = input_list[4]
        self.mothermaiden = input_list[5]
        self.mother = input_list[6]
        self.townborn = input_list[8]
        self.townreg = input_list[9]
        self.jaras = input_list[10]
        self.megye = input_list[11]
        self.comments = input_list[12]
        self.ldsrecord = input_list[13]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


class jg_bmd_death(jg_bmd):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year


#fill in fields to make final record structure
def adjust_jg(list):
    idx = 0
    for row in list:
        print("row", row[1], row[1].find(","))
        if row[1].find(",") != -1:
            row[1] = re_comma2space(row[1]).strip()
        else:
            row.insert(givenname_idx, "noName")

        print("data", data_out[idx])
    print("out", data_out)


givenname_idx = 1
data_out = [[]] # temporary output list of lists
data_d =[[]] # death date list of lists

data_d = clean_jg_inp(jg_d_input) # clean nulls and omit records
adjust_jg(data_d) # fill in to end state record structure

for row in data_out:
    print("row:", row)
    data_out = jg_bmd(row)
    print(data_out)

