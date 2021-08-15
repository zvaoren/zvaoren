from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from adjust_jg_death_record3 import build_jg_death
from adjust_jg_birth_record1 import build_jg_birth
# Reading an excel file using Python
import pandas as pd


def write_excel(death_data, birth_data, file, surename):

    death_df = pd.DataFrame(death_data)
    birth_df = pd.DataFrame(birth_data)
#    wed_df = pd.DataFrame(wed_data)
    death_sheet_name = "JG_" + surename + "_Death"
    birth_sheet_name = "JG_" + surename + "_Birth"
#    wed_sheet_name = "JG_" + surename + "_Wed"

    writer = pd.ExcelWriter(file, engine='openpyxl', mode='w', date_format='dd-mm-yyyy')   # was mode='a'
    death_df.to_excel(writer, sheet_name=death_sheet_name, index=False, header=None)
    birth_df.to_excel(writer, sheet_name=birth_sheet_name, index=False, header=None)
#    wed_df.to_excel(writer, sheet_name=wed_sheet_name, index=False, header=None)

    writer.save()
    writer.close()
    print ("after close file")

    return

#from clean_jg_input import clean_jg_inp
# input list:
# srchX = <search value>
# srchXv = S - Surename, G = GivenName, T = Town, X = AnyField
# srchXt = Q - Phonetically like, D - Sounds like, S - Starts with, E - Is exact, F1 - Fuzzy Match, F2 - Fuzzier match, FM - Fuzziest match

def get_data(table, page, name):
    url = "https://www.jewishgen.org/databases/jgdetail_2.php"

    body = {
        "df": table,
        "georegion": "0*",
        "srch1": name,
        "srch1v": "S",
        "srch1t": "Q",
#        "srch2": name1,
#        "srch2v": "S",
#        "srch2t": "Q",
        "srchbool": "AND",
        "dates": "all",
        "newwindow": 0,
        "recstart": page, #record offset to start with
        "recjump": 0,
        "submit": "List+595+records"
    }
    headers = {
        "authority": "www.jewishgen.org",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "origin": "https://www.jewishgen.org",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://www.jewishgen.org/databases/jgform.php",
        "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "_gcl_au=1.1.1201294544.1600863242; _gac_UA-11980128-1=1.1600863243.Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB; __utmz=221537415.1601444022.7.4.utmgclid=Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB|utmccn=(not%20set)|utmcmd=(not%20set); _gcl_aw=GCL.1601444038.Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB; ASPSESSIONIDASRQBRRR=AOJJFABAGGAEKDKJKCCHJFLA; __utmc=221537415; jgcure=contact=Zvi+Ezra+Oren&clr=Linkedin8&email=zvaoren%40hotmail%2Ecom&fname=Zvi&jgid=257441; login=https%3A%2F%2Fwww%2Ejewishgen%2Eorg%2F; ASPSESSIONIDASSQARRQ=JIALDMNAILJGKEEHEMMPPEMH; kcut7r7=2vIL9fDMa9CutH4u6YljJMw%2FNZFLMQ%3D%3D; __utma=221537415.1466052572.1600863243.1601901474.1601907600.19; __utmt=1; AWSALB=IWkenjZOwjPfR13UAOVs+o41n+VuktJgYHPn/EKly1Mh2s2Ewvj7dpR23nNQgM4vUPKm3cMvBVpOrpOBv+QeRAhFQchf4zjkN/4IrtQ6dgvRAu2HFzTR0qvqNTGN; AWSALBCORS=IWkenjZOwjPfR13UAOVs+o41n+VuktJgYHPn/EKly1Mh2s2Ewvj7dpR23nNQgM4vUPKm3cMvBVpOrpOBv+QeRAhFQchf4zjkN/4IrtQ6dgvRAu2HFzTR0qvqNTGN; __utmb=221537415.13.10.1601907600"

    }

    res = requests.post(url, data=urlencode(body), headers=headers)
    html = res.content
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("body").find_all("table")[-3]
#    table = soup.find("body").find_all("table")[-5]
    table_html = table.prettify().replace("<hr/>", "<td/><td>")
    table_soup = BeautifulSoup(table_html, "html.parser")

    trs = table_soup.find_all('tr')

    all_data = [tr.text.replace("\xa0", "").split("\n") for tr in trs]

    return all_data


def fetch_data(inp_surename, db_type):
    input_data, output, all_data = [[]], [[]], []

    i = 0
    x = 1
    # get first page
    input_data = get_data(db_type, i, inp_surename)
    all_data = input_data

    print("First Fetch:", len(input_data), len(all_data))
    if len(input_data) == 2:
        output = ["Empty"]
        x = 0
    else:
        while x == 1:
            i += 50
            input_data = get_data(db_type, i, inp_surename)
            all_data = all_data + input_data
            print("Next Fetch:", i, len(input_data), len(all_data))
            if len(input_data) == 2:
                x = 0
        print("After Loop:", i, len(input_data), len(all_data))
        if db_type == "HUNGDEATH26":
            build_jg_death(all_data, output)
        elif db_type == "HUNGBIRTH27":
            build_jg_birth(all_data, output)
        elif db_type == "HUNGMARR26":
            pass
        else:
            pass

    print("After loop:", i, len(input_data), len(all_data), len(output))

    for row in all_data: # output:
        print("Final rows to Excel:", row)

    return output



def main():
    surename = "Empty"

    print("started")
    data_birth_out, data_death_out, data_wed_out = [[]], [[]], [[]]

    #db_type_wed = "HUNGMARR26" # wedding
    db_type_birth = "HUNGBIRTH27" # birth
    db_type_death = "HUNGDEATH26" # death

    surename = input("surename: ").upper()

    file =  "E:\ZvikaP\GenSW\Trees\JG"
    file = file + "_" + surename.upper() + ".xlsx"
    print("full file name :", file)

    data_death_out = fetch_data(surename, db_type_death)
    data_birth_out = fetch_data(surename, db_type_birth)
#    fetch_data(surename, data_wed_out)

    write_excel(data_death_out, data_birth_out, file, surename)

    print("file:", file)
    print("after write excel")

    quit()


def main_wed():
    surename = "Empty"

    print("started")
    data_birth_out, data_death_out, data_wed_out = [[]], [[]], [[]]

    db_type_wed = "HUNGMARR26" # wedding
#    db_type_birth = "HUNGBIRTH27" # birth
#    db_type_death = "HUNGDEATH26" # death

    surename = input("surename: ").upper()

    file =  "E:\ZvikaP\GenSW\Trees\JG"
    file = file + "_" + surename.upper() + ".xlsx"
    print("full file name :", file)

#    data_death_out = fetch_data(surename, db_type_death)
#    data_birth_out = fetch_data(surename, db_type_birth)
    data_wed_out = fetch_data(surename, data_wed_out)

    write_excel(data_death_out, data_birth_out, file, surename)

    print("file:", file)
    print("after write excel")

    quit()

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graphviz = GraphvizOutput(output_file='E:\ZvikaP\GenSW\Out.png')

#with PyCallGraph(output=graphviz):
#    main()

main()
