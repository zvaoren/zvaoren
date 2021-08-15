# Reading an excel file using Python
import xlrd
import pandas as pd
import numpy as np
import re

# not needed as we have this method under main.py
def write_excel(death_data, birth_data, file):

    death_df = pd.DataFrame(death_data)
#    birth_df = pd.DataFrame(birth_data)
    death_sheet_name = "JG_Death"
#    birth_sheet_name = "JG_Birth"

    writer = pd.ExcelWriter(file, engine='openpyxl', mode='wa', date_format='dd-mm-yyyy')
    death_df.to_excel(writer, sheet_name=death_sheet_name, index=False, header=None)
#    birth_df.to_excel(writer, sheet_name=birth_sheet_name, index=False, header=None)

    writer.save()
    print("saved:", file)
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


def read_sheet(wb, sheet_idx):
    list = [[]]
    sheet = wb.sheet_by_index(sheet_idx)

    # Offset For row 0 and column 0 - start extract from this offset
    sheet.cell_value(0, 0)
    # loop on records per excel records
    print(sheet.nrows)
    for j in range(sheet.nrows):
        list.append([])
        for i in range(sheet.ncols):
            list[j].append(sheet.cell_value(j, i))
#            print(j,i,list[j][i])
            #check if not string - then dont subtitute special characters
            res = isinstance(list[j][i], str)
            if res:
                list[j][i] = re.sub(r'\xa0', ' ', list[j][i])
    del list[-1] # last line that we appened and not need
    del list[0] # first empty line
    return list



def open_workbook(file):
# Give the location of the file
    loc = file

# Open excel Workbook
    wb = xlrd.open_workbook(loc)    
    print("number of sheets", len(wb.sheet_names()))

    return wb


file = "C:\ZvikaP\GenSW\Trees\\"
file_out = "C:\ZvikaP\GenSW\Trees\excel_test2.xlsx"
#file = "C:\ZvikaO\ZvikaP\Zvika Fam Search\Trees\excel_test.xlsx"
death = [[]]
birth = [[]]
wb = ''

sure_name = input("Sure name:")
file = file + "JG_" + sure_name.upper() + ".xlsx"

print(file)
wb = open_workbook(file)

death = read_sheet(wb, 0)
birth = read_sheet(wb, 1)

print("Death:")
for row in death:
    print(row)
print("Birth:")
for row in birth:
    print(row)

build_gen_lists(death, birth) # wed will come later

    
quit()
sheet_name = "JG_data"
write_excel(list, file_out, file_out)

#write_excel(list, file_out, sheet_name)
print("Finish")