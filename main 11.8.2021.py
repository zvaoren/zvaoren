from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
from adjust_jg_death_record3 import build_jg_death
from adjust_jg_birth_record1 import build_jg_birth
# Reading an excel file using Python
import pandas as pd


def write_excel(death_data, birth_data, file):

    death_df = pd.DataFrame(death_data)
    birth_df = pd.DataFrame(birth_data)
    death_sheet_name = "JG_Death"
    birth_sheet_name = "JG_Birth"

    writer = pd.ExcelWriter(file, engine='openpyxl', mode='w', date_format='dd-mm-yyyy')   # was mode='a'
    death_df.to_excel(writer, sheet_name=death_sheet_name, index=False, header=None)
    birth_df.to_excel(writer, sheet_name=birth_sheet_name, index=False, header=None)

    writer.save()
    writer.close()
    print ("after close file")

    return

#    writer = pd.ExcelWriter("pandas_datetime.xlsx",
#                            engine='xlsxwriter',
#                            datetime_format='mmm d yyyy hh:mm:ss',
#                            date_format='mmmm dd yyyy')

#    format1 = workbook.add_format({'num_format': '#,##0.00'})
#    format2 = workbook.add_format({'num_format': '0%'})

    # Set the column width and format.
#    worksheet.set_column('B:B', 18, format1)

    # Set the format but not the column width.
#    worksheet.set_column('C:C', None, format2)
#    file = "C:\ZvikaP\GenSW\Trees\excel_from_main.xlsx"
#    df = pd.DataFrame(data)
#    writer = pd.ExcelWriter(file, engine='xlsxwriter')
#writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
#    df.to_excel(writer, sheet_name=sheet_name, index=False)
#    writer.save()
#    return



#from clean_jg_input import clean_jg_inp
# input list:
# srchX = <search value>
# srchXv = S - Surename, G = GivenName, T = Town, X = AnyField
# srchXt = Q - Phonetically like, D - Sounds like, S - Starts with, E - Is exact, F1 - Fuzzy Match, F2 - Fuzzier match, FM - Fuzziest match

def get_data(table, page):
    url = "https://www.jewishgen.org/databases/jgdetail_2.php"

    name = input("surename: ")
#    name1 = input("surename1: ")

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
    table_html = table.prettify().replace("<hr/>", "<td/><td>")
    table_soup = BeautifulSoup(table_html, "html.parser")

    trs = table_soup.find_all('tr')

    all_data = [tr.text.replace("\xa0", "").split("\n") for tr in trs]

    return all_data



def main():
    print("started")
    surename = "gross"
    #db_type_wed = "HUNGMARR26" # wedding
    db_type_birth = "HUNGBIRTH27" # birth
    db_type_death = "HUNGDEATH26" # death
    data_birth_out, data_death_out, data_wed_out, data_birth_total, data_death_total, data_wed_total = [[]], [[]], [[]], [[]], [["", "", "", ""]], [[]]
    data_death = []
    file =  "E:\ZvikaP\GenSW\Trees\JG"
    file = file + "_" + surename.upper() + ".xlsx"
    print("full file name :", file)


    #input("search in:", db_type)
    i = 0
    while len(data_death) != 2:
        data_death = get_data(db_type_death, i)
        for row in data_death:
            print("Death_records first:", i,  row)
        if len(data_death) > 5:
            data_death_total = data_death_total + data_death
            for row in data_death_total:
                print("Before Build:", i, row)
            build_jg_death(data_death_total, data_death_out)
        for row in data_death_total:
            print("Death_records:", i,  row)
        i += 50

    print("list len________:", len(data_death))

    #if len(data_death) == 2:
    #    print("empty search", i)
    #    if len(data_death_total) < 6:
    #        data_death_out = ["Empty"]
    #    else:
    #        data_death_total = data_death_total + data_death
    #        print("Before Build:", len(data_death_total), data_death_total)
    #        build_jg_death(data_death_total, data_death_out)

    print("build")

    for row in data_death_out:
        print("Death:", row)

    write_excel(data_death_out, data_birth_out, file)

    print("file:", file)
    print("after write excel")

    quit()

    print("after print")

    #i += 50
    #data_death = get_data(db_type_death, i)
    #for row in data_death_total:
    #    print("Death_total2:", row)

    #print("after get_data", data_death)
    #if len(data_death) == 2:
    #    print("empty search")
    #else:
    #    data_death_total = data_death_total + data_death
    #    build_jg_death(data_death_total, data_death_out)

    i = 0

    data_birth = get_data(db_type_birth, i)
    build_jg_birth(data_birth, data_birth_out)
    data_birth_total = data_birth_total + data_birth
    for row in data_birth_total:
        print("Birth_total1:", row)

    i += 50
    data_birth = get_data(db_type_birth, i)
    for row in data_birth_total:
        print("Birth_total2:", row)

    if len(data_birth) == 2:
        print("empty search")
        data_birth_out = ["Empty"]
    else:
        data_birth_total = data_birth_total + data_birth
        build_jg_birth(data_birth, data_birth_out)

    print("file:", file)

    write_excel(data_death_out, data_birth_out, file)

    #  print(data)
    for row in data_birth_out:
        print("Birth:", row)



    # curl 'https://www.jewishgen.org/databases/jgdetail_2.php' \
    #   -H 'authority: www.jewishgen.org' \
    #   -H 'cache-control: max-age=0' \
    #   -H 'upgrade-insecure-requests: 1' \
    #   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' \
    #   -H 'origin: https://www.jewishgen.org' \
    #   -H 'content-type: application/x-www-form-urlencoded' \
    #   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    #   -H 'sec-fetch-site: same-origin' \
    #   -H 'sec-fetch-mode: navigate' \
    #   -H 'sec-fetch-user: ?1' \
    #   -H 'sec-fetch-dest: document' \
    #   -H 'referer: https://www.jewishgen.org/databases/jgform.php' \
    #   -H 'accept-language: he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7' \
    #   -H 'cookie: _gcl_au=1.1.1201294544.1600863242; _gac_UA-11980128-1=1.1600863243.Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB; __utmz=221537415.1601444022.7.4.utmgclid=Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB|utmccn=(not%20set)|utmcmd=(not%20set); _gcl_aw=GCL.1601444038.Cj0KCQjwtsv7BRCmARIsANu-CQfyM5R1wr7zq7wcxcfQKtfaBrBbDxiTtzWWcgq0pMve1knwugojrxsaAhhKEALw_wcB; ASPSESSIONIDASRQBRRR=AOJJFABAGGAEKDKJKCCHJFLA; __utmc=221537415; jgcure=contact=Zvi+Ezra+Oren&clr=nidhog22&email=zvaoren%40hotmail%2Ecom&fname=Zvi&jgid=257441; login=https%3A%2F%2Fwww%2Ejewishgen%2Eorg%2F; ASPSESSIONIDASSQARRQ=JIALDMNAILJGKEEHEMMPPEMH; kcut7r7=2vIL9fDMa9CutH4u6YljJMw%2FNZFLMQ%3D%3D; __utma=221537415.1466052572.1600863243.1601901474.1601907600.19; __utmt=1; AWSALB=IWkenjZOwjPfR13UAOVs+o41n+VuktJgYHPn/EKly1Mh2s2Ewvj7dpR23nNQgM4vUPKm3cMvBVpOrpOBv+QeRAhFQchf4zjkN/4IrtQ6dgvRAu2HFzTR0qvqNTGN; AWSALBCORS=IWkenjZOwjPfR13UAOVs+o41n+VuktJgYHPn/EKly1Mh2s2Ewvj7dpR23nNQgM4vUPKm3cMvBVpOrpOBv+QeRAhFQchf4zjkN/4IrtQ6dgvRAu2HFzTR0qvqNTGN; __utmb=221537415.13.10.1601907600' \
    #   --data-raw 'df=HUNGBIRTH27&georegion=0*&srch1=flesch&srch1v=S&srch1t=Q&srchbool=AND&dates=all&newwindow=0&recstart=0&recjump=0&submit=List+595+records' \
    #   --compressed



    quit()

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graphviz = GraphvizOutput(output_file='E:\ZvikaP\GenSW\Out.png')

with PyCallGraph(output=graphviz):

    main()
