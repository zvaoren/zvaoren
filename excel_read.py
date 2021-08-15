# Reading an excel file using Python
import xlrd
import pandas as pd
import numpy as np
import re


def write_excel(data, file, sheet_name):

#    file = "C:\ZvikaP\GenSW\Trees\excel_from_main.xlsx"
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
#writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    return


def write_excel(death_data, birth_data, file):

    death_df = pd.DataFrame(death_data)
    birth_df = pd.DataFrame(birth_data)
    death_sheet_name = "JG_Death"
    birth_sheet_name = "JG_Birth"

    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    death_df.to_excel(writer, sheet_name=death_sheet_name, index=False, header=None)
    birth_df.to_excel(writer, sheet_name=birth_sheet_name, index=False, header=None)

    writer.save()
    writer.close()

    return



def read_excel(file):
    # Load spreadsheet
    xl = pd.ExcelFile(file)

# Print the sheet names - can have offset numbers as sheet param: first sheet = 0, second sheet = 1 etc.
    print(xl.sheet_names)
    sheet_name = xl.sheet_names

# Load a sheet into a DataFrame by name: df1
    df1 = xl.parse(0)

    list_of_lists = np.array(df1)
    for row in list_of_lists:
        print("DF1 lists:", row)
    return

def read_from_excel(file):
#Insert complete path to the excel file and index of the worksheet
    df = pd.read_excel("C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\excel_test.xlsx",
                   sheet_name=0,
                   na_values="n\a")

    df.head()
    print("df", df.values)

    df_values = df.values
    df_values[:, :-1].tolist()

    print(df_values[0])
    return


def open_workbook(file):
# Give the location of the file
#    loc = ("C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\excel_test.xlsx") # contains 3 sheets of GJ BDM records
#    loc = ("C:\ZvikaO\GenSW\excel_test1.xlsx") #vrable area combined excel
    loc = file

# To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
# For row 0 and column 0
    sheet.cell_value(0, 0)

    for j in range(sheet.nrows):
        list.append([])
        for i in range(sheet.ncols):
            list[j].append(sheet.cell_value(j, i))
#            print(j,i,list[j][i])
            #check if not string - then dont subtitute special characters
            res = isinstance(list[j][i], str)
            if res:
                list[j][i] = re.sub(r'\xa0', ' ', list[j][i])
    del list[-1]
    return



file = "C:\ZvikaP\GenSW\Trees\excel_test1.xlsx"
file_out = "C:\ZvikaP\GenSW\Trees\excel_test2.xlsx"
#file = "C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\excel_test.xlsx"
list = [[]]

open_workbook(file)
for row in list:
    print(row)

sheet_name = "JG_data"
write_excel(list, file_out, sheet_name)
print("Finish")