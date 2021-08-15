import re
from dateutil.parser import parse
from clean_jg_input import clean_jg_inp

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
    if is_date(date):
        dt = parse(date)
        year = int(dt.date().year)
        if year >= 2000:
            return year - 100
        else:
            return year
    else:
        return date[-4:] # return 4 last chars - assuming this is the year

#DONE
def estimated_birth_year(year_date, age):
    return (year_date - age)


#JG wedding records
jg_w_input = [
['', '', '', '     STERN', '    ', '    ,Eduard', '    ', '', '     WEIL', '    ', '    ,Emilie', '   ', '', '    Ignatz/-(-)', '    ', '    -/-(-)', '   ', '', '    29', '    ', '    20', '   ', '', '    25-Oct-1881', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', "    groom from Palanka; bride's grandfather Jacob GRUNBAUM", '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    137', '    ', '', ''],
['', '', '', '     LEITNER', '    ', '    ,Sandor', '    ', '', '     WEISZ', '    ', '    ,Helena', '   ', '', '    Mihaly/Sali(LEITNER)', '    ', '    Simon/Julianna(HAUSLER)', '   ', '', '    27', '    ', '    20', '   ', '', '    16/03/1904', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 18-Jan-1876 in Vamospercs.  Bride born 04-Mar-1886 in Ertarcsa.  Bride's mother is deceased.", '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 2', '    ', '    18-2 & 19-1', '    ', '', ''],
['', '', '', '     LEFKOWITZ', '    ', '    ,Salamon', '    ', '', '     WEISZ', '    ', '    ,Maria', '   ', '', '    David/Anna()', '    ', '    Isak/Rosa()', '   ', '', '    23', '    ', '    20', '   ', '', '    09-Aug-1861', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Szobrancz / Bride born in: Nanas / Groom's year of wed: 1838 / Bride's year of wed: 1841 / Groom's date of death: '30-Mar-1886", '   ', '', '    LDS 642810', '    ', '    282-005', '    ', '', ''],
['', '', '', '     STERN', '    ', '    ,Sandor', '    ', '', '     WAHRMANN', '    ', '    ,Johana', '   ', '', '    -/-(-)', '    ', '    -/-(-)', '   ', '', '    28', '    ', '    17', '   ', '', '    26-Aug-1862', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    bride orphan, born in N.Varad', '   ', '', '    LDS 642857, Vol. 1', '    ', '    119-08', '    ', '', ''],
['', '', '', '     STERN', '    ', '    ,Izrael', '    ', '', '     GRUNBAUM', '    ', '    ,Aranka', '   ', '', '    Lazar/Hani()', '    ', '    Marczell/Pepi(FARKAS-FRIEDLANDER)', '   ', '', '    [23]', '    ', '    17', '   ', '', '    05-May-1874', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's year of birth: 1851 / Bride's birthdate: '25-Oct-1856", '   ', '', '    LDS 642810', '    ', '    291-009', '    ', '', ''],
['', '', '', '     LEWI', '    ', '    ,Abraham', '    ', '', '     GELBERGER', '    ', '    ,Hermina', '   ', '', '    Izrael/Maria(WEISZ)', '    ', '    Peter/Lina(KELLER)', '   ', '', '    29', '    ', '    24', '   ', '', '    09-Mar-1897', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 19-May-1867 in Nagy Bajom.  Bride born 04-Jan-1873 in Vamospercs.', '   ', '', '    LDS', '    ', '     2127458', '    ', '    , Item 3', '    ', '    47-2 & 48-1', '    ', '', ''],
['', '', '', '     GLUCKSTHAL', '    ', '    ,Samuel', '    ', '', '     STERN', '    ', '    ,Hani', '   ', '', '    -/Fani(-)', '    ', '    Bernhard/-(-)', '   ', '', '    24', '    ', '    -', '   ', '', '    17-Oct-1871', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Strecna; bride from Hrabowa', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    88', '    ', '', ''],
['', '', '', '     SCHLOSSER', '    ', '    ,Farkas / Zev', '    ', '', '     STERN', '    ', '    ,Hani  / Hentsha', '   ', '', '    Lazar/Jente()', '    ', '    Jozsef/Sara(WEISZ)', '   ', '', '    32', '    ', '    30', '   ', '', '    19-Mar-1893', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Uj Feherto / Bride born in: Nanas / Groom's year of birth: 1861 / Bride's birthdate: '01-Sep-1863", '   ', '', '    LDS 642810', '    ', '    315-002', '    ', '', ''],
['', '', '', '     SCHLOSSER', '    ', '    ,Ignatz', '    ', '', '     STERN', '    ', '    ,Maria', '   ', '', '    Lazar/Hani()', '    ', '    Josef/Sara()', '   ', '', '    22', '    ', '    19', '   ', '', '    24-Jun-1868', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Uj Feherto / Bride born in: Nanas / Groom's year of birth: 1846 / Bride's year of birth: 1849", '   ', '', '    LDS 642810', '    ', '    287-005', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Mozes', '    ', '', '     GRUNBAUM', '    ', '    ,Regina', '   ', '', '    Akiva/Chaja(FELDMAN)', '    ', '    Lajos/Hani(ZALERMAN)', '   ', '', '    37', '    ', '    33', '   ', '', '    26-May-21', '    ', '    Csecs', '    ', '    Nagy Ida', '    ', '    Kassa', '    ', '    Abaúj-Torna', '   ', '', '', '', '    LDS', '    ', '     2006428', '    ', '    , Item 6', '    ', '    12-01', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GLUCK', '    ', '    ,Yakab', '    ', '', '     TURK', '    ', '    ,Eszter', '   ', '', '    Mozes/Eszter(ROTH)', '    ', '    Mozes/Hani(STERN)', '   ', '', '    24', '    ', '    24', '   ', '', '    12-May-1887', '    ', '    Nagy Ida', '    ', '    Nagy Ida', '    ', '    Kassa', '    ', '    Abaúj-Torna', '   ', '', '    Bride from Miglicz, Groom from Gorgo', '   ', '', '    LDS', '    ', '     2006428', '    ', '    , Item 6', '    ', '    02-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     PORJES', '    ', '    ,Moritz', '    ', '', '     STERN', '    ', '    ,Rosi', '   ', '', '    Jacob/-(-)', '    ', '    Bernat/-(-)', '   ', '', '    24', '    ', '    28', '   ', '', '    02-Mar-1869', '    ', '    Hrabowa', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Pruzina', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    70', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GLUCKSTHAL', '    ', '    ,Samuel', '    ', '', '     STERN', '    ', '    ,Hani', '   ', '', '    -/Fani(-)', '    ', '    Bernhard/-(-)', '   ', '', '    24', '    ', '    -', '   ', '', '    17-Oct-1871', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Strecna; bride from Hrabowa', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    88', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Dawid', '    ', '', '     EPSTEIN', '    ', '    ,Anna', '   ', '', '    -/Julie(-)', '    ', '    Sam./-(-)', '   ', '', '    29', '    ', '    18', '   ', '', '    23-May-1875', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Szered', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    104', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WERNER', '    ', '    ,Adolf', '    ', '', '     STERN', '    ', '    ,Marie', '   ', '', '    Markus/-(-)', '    ', '    Bernhard/-(-)', '   ', '', '    26', '    ', '    24', '   ', '', '    20-Aug-1878', '    ', '    Hrabowa', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Rudna', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    120', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '', ''],
['', '', '', '     TAUSZEK', '    ', '    ,Jacob', '    ', '', '     STERN', '    ', '    ,Regie Rosa', '   ', '', '    Laser/Susanna(SINGER)', '    ', '    Eduard/Hani(SPITZER)', '   ', '', '    25', '    ', '    21', '   ', '', '    19-Feb-1889', '    ', '    Nagy Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Kollarovitz', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    3', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WITTENBERG', '    ', '    ,Samuel', '    ', '', '     DEUTSCH', '    ', '    ,Hani/Anna', '   ', '', '    Moritz/Rosi(MILCH)', '    ', '    Ignatz/Rosa(STERN)', '   ', '', '    32', '    ', '    18', '   ', '', '    10-Jul-1894', '    ', '    Nagy-Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    8', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     MUNK', '    ', '    ,Gabriel', '    ', '', '     DEUTSCH', '    ', '    ,Zili', '   ', '', '    Adalbert/Sali(LICHTENSTEIN)', '    ', '    Ignatz/Rosi(STERN)', '   ', '', '    35', '    ', '    20', '   ', '', '    22-Nov-1892', '    ', '    Nagy Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Nyiregyhaza', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    15', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     GESZTI', '    ', '    ,Dr. Sandor', '    ', '', '     HERMANN', '    ', '    ,Klara', '   ', '', '    Osak/Ester(STERN)', '    ', '    Mano/Sarvita(RANZENHOFER)', '   ', '', '    40', '    ', '    30', '   ', '', '    17-May-00', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    25', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Mor', '    ', '', '     MARKUS', '    ', '    ,Janka', '   ', '', '    Hermann/Fani(FISCHER)', '    ', '    Sandor/Fani(LEINWENDER)', '   ', '', '    25', '    ', '    22', '   ', '', '    10-Nov-1897', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    30', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     BEER', '    ', '    ,Zsigmond', '    ', '', '     STERN', '    ', '    ,Hedwig', '   ', '', '    Benedek/Betti(FORSTER)', '    ', '    Jakab/Borbalya(ZOPF)', '   ', '', '    36', '    ', '    22', '   ', '', '    08-Dec-00', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    35', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GOLDBERGER', '    ', '    ,Hermann', '    ', '', '     STERN', '    ', '    ,Malvina', '   ', '', '    Jozsef/Berta(KOLMAN)', '    ', '    Jakab/Babetta(ZOPZ)', '   ', '', '    30', '    ', '    24', '   ', '', '    07-Jan-06', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    22', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '', ''],
['', '', '', '     LEFKOWITZ', '    ', '    ,Salamon', '    ', '', '     CZIMENT', '    ', '    ,Betti', '   ', '', '    David/Hani()', '    ', '    Samuel / Shmuel Shmelke/Fani  / Freidel(STERN)', '   ', '', '    37', '    ', '    20', '   ', '', '    06-Feb-1874', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Ungvar / Bride born in: Nanas / Groom's year of birth: 1837 / Bride's year of birth: 1854", '   ', '', '    LDS 642810', '    ', '    291-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Izrael', '    ', '', '     GRUNBAUM', '    ', '    ,Aranka', '   ', '', '    Lazar/Hani()', '    ', '    Marczell/Pepi(FARKAS-FRIEDLANDER)', '   ', '', '    23', '    ', '    17', '   ', '', '    05-May-1874', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's year of birth: 1851 / Bride's birthdate: '25-Oct-1856", '   ', '', '    LDS 642810', '    ', '    291-009', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GLUCK', '    ', '    ,Sije', '    ', '', '     STERN', '    ', '    ,Eti', '   ', '', '    Ignatz/Maria()', '    ', '    Lazar/Hani(RUBINSTEIN)', '   ', '', '    23', '    ', '    19', '   ', '', '    27-Jun-1876', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Bokony / Bride born in: Nanas / Groom's year of birth: 1853 / Bride's birthdate: '10-Aug-1856", '   ', '', '    LDS 642810', '    ', '    293-003', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Zsigmond', '    ', '', '     STERN', '    ', '    ,Rebeka', '   ', '', '    Ignacz/Sara(SCHWARTZ)', '    ', '    Jozsef/Sara(WEISZ)', '   ', '', '    23', '    ', '    20', '   ', '', '    20-Jun-1877', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's birthdate: '01-Jun-1854 / Bride's birthdate: '10-Apr-1858", '   ', '', '    LDS 642810', '    ', '    294-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZBERG', '    ', '    ,Samuel', '    ', '', '     CZIMENT', '    ', '    ,Fani', '   ', '', '    Izsak/Sara()', '    ', '    Samuel / Shmuel Shmelke/Fani  / Freidel(STERN)', '   ', '', '    27', '    ', '    20', '   ', '', '    10-Aug-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Tetijlen? / Bride born in: Nanas / Groom's year of birth: 1853 / Bride's birthdate: '11-Sep-1855", '   ', '', '    LDS 642810', '    ', '    298-003', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     ROTH', '    ', '    ,Salamon', '    ', '', '     STERN', '    ', '    ,Fani', '   ', '', '    Jozsef/Maria(ROTH)', '    ', '    Lajos/Katalin(WEISZ)', '   ', '', '    25', '    ', '    20', '   ', '', '    26-Aug-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's birthdate: '29-May-1857 / Bride's birthdate: '10-Jun-1862", '   ', '', '    LDS 642810', '    ', '    298-007', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     HIRSCH', '    ', '    ,Kalman', '    ', '', '     HIRSCH', '    ', '    ,Betti', '   ', '', '    Lazar/Hani(STERN)', '    ', '    Izrael/Rozsa(GLUCKLICH)', '   ', '', '    24', '    ', '    18', '   ', '', '    08-Nov-1881', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Debrecen / Bride born in: Nanas / Groom's year of birth: 1857 / Bride's birthdate: '28-Jul-1863", '   ', '', '    LDS 642810', '    ', '    299-006', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ADLER', '    ', '    ,Mihaly / Elimelech', '    ', '', '     CZIMENT', '    ', '    ,Mari / Breindel', '   ', '', '    Elias Ahron/Edel(SAMUELI)', '    ', '    Samuel / Shmuel Shmelke/Fani  / Freidel(STERN)', '   ', '', '    48', '    ', '    38', '   ', '', '    15-Aug-1888', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Felso Falu / Bride born in: Nanas / Groom's year of birth: 1840 / Bride's year of birth: 1850", '   ', '', '    LDS 642810', '    ', '    307-002', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Mor / Mozes', '    ', '', '     HEIMLICH', '    ', '    ,Fani', '   ', '', '    Ignatz/Hani(KLEIN)', '    ', '    Samuel/Hani / Netti / Necha(STERN)', '   ', '', '    28', '    ', '    22', '   ', '', '    02-Sep-1888', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Patroha / Bride born in: Nanas / Groom's year of birth: 1860 / Bride's birthdate: '03-Sep-1867", '   ', '', '    LDS 642810', '    ', '    307-004', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SCHWARTZ', '    ', '    ,Lajos / Leib', '    ', '', '     STERN', '    ', '    ,Eszter', '   ', '', '    David/Juliana(CSILLAG)', '    ', '    Jozsef/Sara / Sarah Leah(WEISZ)', '   ', '', '    41', '    ', '    29', '   ', '', '    26-Nov-1889', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: H. Hadhaz / Bride born in: Nanas / Groom's year of birth: 1848 / Bride's birthdate: '24-Nov-1860", '   ', '', '    LDS 642810', '    ', '    309-006', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     CZIMENT', '    ', '    ,Farkas / Volf', '    ', '', '     BUNZL', '    ', '    ,Franciska / Fani / Frimet', '   ', '', '    Samuel / Shmuel Shmelke/Fani  / Freidel(STERN)', '    ', '    Gyula / Yonah/Fani(SCHWARTZ)', '   ', '', '    27', '    ', '    21', '   ', '', '    27-Aug-1890', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's birthdate: '30-Apr-1863 / Bride's birthdate: '20-Apr-1870", '   ', '', '    LDS 642810', '    ', '    310-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     CZIMENT', '    ', '    ,Marton / Mordechai', '    ', '', '     LEFKOWITZ', '    ', '    ,Regi / ?', '   ', '', '    Samuel / Shmuel Shmelke/Fani  / Freidel(STERN)', '    ', '    Farkas / Zev yonah/Teri / Sasha Serel?(SPITZER)', '   ', '', '    33', '    ', '    17', '   ', '', '    01-Dec-1891', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: T. Lok / Groom's birthdate: '08-Nov-1858 / Bride's year of birth: 1874", '   ', '', '    LDS 642810', '    ', '    312-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SCHLOSSER', '    ', '    ,Farkas / Zev', '    ', '', '     STERN', '    ', '    ,Hani  / Hentsha', '   ', '', '    Lazar/Jente()', '    ', '    Jozsef/Sara(WEISZ)', '   ', '', '    32', '    ', '    30', '   ', '', '    19-Mar-1893', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Uj Feherto / Bride born in: Nanas / Groom's year of birth: 1861 / Bride's birthdate: '01-Sep-1863", '   ', '', '    LDS 642810', '    ', '    315-002', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     HEIMLICH', '    ', '    ,Abraham', '    ', '', '     ELLBOGEN', '    ', '    ,Eszti', '   ', '', '    Samuel/Hani / Netti / Necha(STERN)', '    ', '    Marton / Naftoli Elimelech/Fani / Feige(HAMMER)', '   ', '', '    24', '    ', '    28', '   ', '', '    13-Mar-1895', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's birthdate: '12-Feb-1872 / Bride's year of birth: 1867", '   ', '', '    LDS 642810', '    ', '    318-003', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GRUNFELD', '    ', '    ,Beni / Baruch', '    ', '', '     GOLDSTEIN', '    ', '    ,Lina / Leah', '   ', '', '    Salamon/Borbala(STERN)', '    ', '    Bernat / Berish/Judit(PETERSEHL)', '   ', '', '    25', '    ', '    22', '   ', '', '    03-Jun-1895', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Vitka [Szatmar M.] / Bride born in: Nanas / Groom's year of birth: 1870 / Bride's birthdate: 'XX-May-1873", '   ', '', '    LDS 642810', '    ', '    318-004', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Ignatz', '    ', '', '     SILBERSTEIN', '    ', '    ,Josefa', '   ', '', '    -/-(-)', '    ', '    David/-(-)', '   ', '', '    28', '    ', '    23', '   ', '', '    3-Mar-1861', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Groom from Gyomar; See also record 114-05', '   ', '', '    LDS 642857, Vol. 1', '    ', '    112-21', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Simon', '    ', '', '     DEUTSCH', '    ', '    ,Katalin', '   ', '', '    -/-(-)', '    ', '    -/-(-)', '   ', '', '    25', '    ', '    26', '   ', '', '    27-Apr-1865', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642857, Vol. 1', '    ', '    140-06', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Gabor', '    ', '', '     SVEIGER', '    ', '    ,Regina', '   ', '', '    -/-(-)', '    ', '    -/-(-)', '   ', '', '    -', '    ', '    -', '   ', '', '    30-Mar-1840', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642857, Vol. 1', '    ', '    22-05', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SVIMER', '    ', '    ,Alexander', '    ', '', '     STERN', '    ', '    ,Leny', '   ', '', '    -/-(-)', '    ', '    -/-(-)', '   ', '', '    -', '    ', '    -', '   ', '', '    12-Aug-1840', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642857, Vol. 1', '    ', '    22-07', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Yakab', '    ', '', '     VEISS', '    ', '    ,Regina', '   ', '', '    David/-(-)', '    ', '    Fulop/-(-)', '   ', '', '    32', '    ', '    28', '   ', '', '    23-Oct-1854', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    See record 72-04', '   ', '', '    LDS 642857, Vol. 1', '    ', '    67-21', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     GROSSINGER', '    ', '    ,Tobias', '    ', '', '     ASSINGER', '    ', '    ,Joresfa?', '   ', '', '    Janos/Kati(STERN)', '    ', '    Jakab/Fani(DEUTSCH)', '   ', '', '    25', '    ', '    32', '   ', '', '    23-Mar-1895', '    ', '    Kecskemet', '    ', '    Kecskemet', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642857, Vol. 2', '    ', '    249-03', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Ignacz', '    ', '', '     WEISZ', '    ', '    ,Iren', '   ', '', '    Mor/Lidia(STERN)', '    ', '    Vilmos/Minni(WEISZ)', '   ', '', '    28', '    ', '    18', '   ', '', '    18-Aug-1891', '    ', '    Keczel', '    ', '    Kiskoros', '    ', '    Solti-also', '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642857, Vol. 3', '    ', '    10-03', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SZEDO', '    ', '    ,Adolf', '    ', '', '     WIESEL', '    ', '    ,Johanna', '   ', '', '    Hermann/Rozalia(STERN)', '    ', '    Lipot/Betti(KLEIN)', '   ', '', '    33', '    ', '    22', '   ', '', '    29-Apr-1888', '    ', '    Kiskoros', '    ', '    Kiskoros', '    ', '    Solti-also', '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Groom from Budapest', '   ', '', '    LDS 642857, Vol. 3', '    ', '    04-04', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Israel', '    ', '', '     EIBENSCHITZ', '    ', '    ,Regina', '   ', '', '    Isak/Eleonora(HELLER)', '    ', '    Adam/Kati(BECK)', '   ', '', '    26', '    ', '    22', '   ', '', '    20-Dec-1871', '    ', '    Kiskunmajsa', '    ', '    Halas', '    ', '    Kis-kun also', '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642860, vol. 1', '    ', '    19-06', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Lazar', '    ', '', '     WEISZ', '    ', '    ,Nesi', '   ', '', '    Herman/Fani(KERSCHNER)', '    ', '    Leopald/Otili(POLLAK)', '   ', '', '    57', '    ', '    56', '   ', '', '    17-Sep-1889', '    ', '    Felegyhaza', '    ', '    Kiskunfelegyhaza', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642860, Vol. 3', '    ', '    117-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Izidor', '    ', '', '     LEDERER', '    ', '    ,Ida', '   ', '', '    Herman/Katalin(ROTHHAUSER)', '    ', '    Gustav/Jozefa(LEDERER)', '   ', '', '    27', '    ', '    19', '   ', '', '    28-Jan-1891', '    ', '    Felegyhaza', '    ', '    Kiskunfelegyhaza', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642860, Vol. 3', '    ', '    121-01', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Aron', '    ', '', '     PERLGRUND', '    ', '    ,Fani', '   ', '', '    Lipot/Katalin(GOSZ)', '    ', '    Zsigmond/Rozalia(BAUER)', '   ', '', '    27', '    ', '    23', '   ', '', '    03-Nov-1891', '    ', '    Felegyhaza', '    ', '    Kiskunfelegyhaza', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642860, Vol. 3', '    ', '    121-05', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Gabor', '    ', '', '     NERMES', '    ', '    ,Roza', '   ', '', '    Jakab/Franczis(SUGAR)', '    ', '    Jozsef/Szali(KRAUSZ)', '   ', '', '    23', '    ', '    24', '   ', '', '    26-Dec-1893', '    ', '    Felegyhaza', '    ', '    Kiskunfelegyhaza', '    ', "    Local Gov't", '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '', '', '    LDS 642860, Vol. 3', '    ', '    123-03', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Israel', '    ', '', '     EIBENSCHISZ', '    ', '    ,Regina', '   ', '', '    Isak/Eleanora(-)', '    ', '    Adam/Kati(BECK)', '   ', '', '    26', '    ', '    22', '   ', '', '    20-Dec-1871', '    ', '    Kiskunmajda', '    ', '    Halas', '    ', '    Kis-kun also', '    ', '    Pest-Pilis-Solt-Kiskun', '   ', '', '    Bride from Becse of Ung megye; Groom from Halas', '   ', '', '    LDS 642860, Vol. 5', '    ', '    10-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Zsigmund', '    ', '', '     FRIDMAN', '    ', '    ,Zelma', '   ', '', '    Edoard/Frida?(GOLDNER)', '    ', '    Ahron/Beti(FRENKEL)', '   ', '', '    32', '    ', '    23', '   ', '', '    31-Aug-1880', '    ', '    Kallosemjen', '    ', '    Kallosemjen', '    ', '    Nagy-Kallo', '    ', '    Szabolcs', '   ', '', '', '', '    LDS 642902', '    ', '    20-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Yalamo', '    ', '', '     ENGEL', '    ', '    ,Hani', '   ', '', '    Lorincz/-(-)', '    ', '    Mihaly/Rosie(GUT…?)', '   ', '', '    25', '    ', '    25', '   ', '', '    15 Sep 1864', '    ', '    Ibrony', '    ', '    Ibrony', '    ', '    Bogdany', '    ', '    Szabolcs', '   ', '', '', '', '    LDS 642913', '    ', '    03-04', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ROTH', '    ', '    ,Moses', '    ', '', '     STERN', '    ', '    ,Lina', '   ', '', '    Simon/-(-)', '    ', '    Abraham/-(-)', '   ', '', '    22', '    ', '    19', '   ', '', '    27 Jun 1871', '    ', '    Ibrony', '    ', '    Ibrony', '    ', '    Bogdany', '    ', '    Szabolcs', '   ', '', '', '', '    LDS 642913', '    ', '    03-07', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Herman', '    ', '', '     KLEIN', '    ', '    ,Etti', '   ', '', '    Leib/-(-)', '    ', '    Lazar/-(-)', '   ', '', '    24', '    ', '    18', '   ', '', '    1 May 1877', '    ', '    Ibrony', '    ', '    Ibrony', '    ', '    Bogdany', '    ', '    Szabolcs', '   ', '', '', '', '    LDS 642913', '    ', '    08-03', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     EHRENREICH', '    ', '    ,Herman', '    ', '', '     STERN', '    ', '    ,Mary', '   ', '', '    -/-(-)', '    ', '    Abraham/Betty(WEIS)', '   ', '', '    25', '    ', '    21', '   ', '', '    9 Mat 1880', '    ', '    Ibrony', '    ', '    Ibrony', '    ', '    Bogdany', '    ', '    Szabolcs', '   ', '', '', '', '    LDS 642913', '    ', '    08-06', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     SCHVAREZ', '    ', '    ,Leopold Samuel', '    ', '', '     ROPSITZ', '    ', '    ,Barbala', '   ', '', '    Leopold Moritz/Mari(VEISZ)', '    ', '    Aron/Hani(BERNAT)', '   ', '', '    25', '    ', '    30', '   ', '', '    7-Jul-1889', '    ', '    Nagy Ida', '    ', '    Nagy Ida', '    ', '    Kassa', '    ', '    Abaúj-Torna', '   ', '', '    Groom from Kassa', '   ', '', '    LDS', '    ', '     2006428', '    ', '    , Item 6', '    ', '    04-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SCHVARTZ', '    ', '    ,Vilmos', '    ', '', '     GROSZ', '    ', '    ,Peszel', '   ', '', '    Hirsch/R.?(PASZTERNAK)', '    ', '    Sandor/Yohanna(VEISZ)', '   ', '', '    21', '    ', '    24', '   ', '', '    21-Nov-1892', '    ', '    Nagy-Yola', '    ', '    Nagy Ida', '    ', '    Kassa', '    ', '    Abaúj-Torna', '   ', '', '    Bride from Abouj-Szanto; Grrom from Szkoros', '   ', '', '    LDS', '    ', '     2006428', '    ', '    , Item 6', '    ', '    07-02', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     MUNK', '    ', '    ,Moritz', '    ', '', '     HUBSCH', '    ', '    ,Regina', '   ', '', '    Joachim/[Henrik]/[Marie]([WEISS])', '    ', '    Eduard/-(-)', '   ', '', '    [30]', '    ', '    21', '   ', '', '    12-Jan-1886', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Tapolcsan;             all bracketed info from No. 1, 1978901(3)', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (1)', '    ', '    165', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FENYO (FREIWILLIG)', '    ', '    ,Mayer', '    ', '', '     HERCSKA', '    ', '    ,Adolfin    (Frumel)', '   ', '', '    Moritz/Regi(WEISZ)', '    ', '    Heinrich/Netti(NEUBAUER)', '   ', '', '    33', '    ', '    20', '   ', '', '    08-Jan-1895', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', "    groom's father FREIWILLIG", '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    1', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jacob', '    ', '', '     NOVAK', '    ', '    ,Berta', '   ', '', '    Adam/Marie(NEUMAN)', '    ', '    Nathan/Josefine(NEUMAN)', '   ', '', '    27', '    ', '    19', '   ', '', '    12-Apr-1888', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Ivanka, Veszprem m.', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    6', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jakab', '    ', '', '     NEUMAN', '    ', '    ,Terez', '   ', '', '    Herman/Hani(HOCHFELDER)', '    ', '    Miksa/Rosa(FELBERT)', '   ', '', '    23', '    ', '    24', '   ', '', '    07-Jul-1895', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    7', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Simon Markus', '    ', '', '     SONNENFELD', '    ', '    ,Marie', '   ', '', '    Samuel/Marie(PREISAK)', '    ', '    Leopold/Hani(LOVENBEIN)', '   ', '', '    26', '    ', '    23', '   ', '', '    11-Sep-1894', '    ', '    Nagy-Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    12', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     HOCHFELDER', '    ', '    ,Gyula (Kohn)', '    ', '', '     WEISZ', '    ', '    ,Jeannette', '   ', '', '    Jozsef (Kohn)/Josefina(TAUSSIK)', '    ', '    Armin/Hanni(HOCHFELDER)', '   ', '', '    24', '    ', '    20', '   ', '', '    02-Sep-1890', '    ', '    Viszoka-     Makov', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    13', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     LEWI', '    ', '    ,Abraham', '    ', '', '     GELBERGER', '    ', '    ,Hermina', '   ', '', '    Izrael/Maria(WEISZ)', '    ', '    Peter/Lina(KELLER)', '   ', '', '    29', '    ', '    24', '   ', '', '    09-Mar-1897', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 19-May-1867 in Nagy Bajom.  Bride born 04-Jan-1873 in Vamospercs.', '   ', '', '    LDS', '    ', '     2127458', '    ', '    , Item 3', '    ', '    47-2 & 48-1', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Jakab', '    ', '', '     ROSENFELD', '    ', '    ,Fani', '   ', '', '    Moritz/Sali(KELLER)', '    ', '    Jozsef/Veronika(WEISZ)', '   ', '', '    24', '    ', '    21', '   ', '', '    28-Apr-1897', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 17-Aug-1872 in Vamospercs.  Bride born 20-Feb-1876 in Vamospercs.', '   ', '', '    LDS', '    ', '     2127458', '    ', '    , Item 3', '    ', '    50-2 & 51-1', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     FRANK', '    ', '    ,Sie Sami', '    ', '', '     ROSENFELD', '    ', '    ,Helen', '   ', '', '    Matyas/Lina(HELEN)', '    ', '    Jozsef/Verona(WEISZ)', '   ', '', '    25', '    ', '    20', '   ', '', '    23/10/1901', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 30-Oct-1875 in Vamospercs.  Bride born 11-Jul-1881 in Vamospercs.  Record duplicated on 35-2 & 36-1.', '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 1', '    ', '    107-2 & 108-1', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Jonas', '    ', '', '     EGRI', '    ', '    ,Vilma', '   ', '', '    Jozsef/Veronika(WEISZ)', '    ', '    Abraham/Hani(LEICHTMANN)', '   ', '', '    25', '    ', '    19', '   ', '', '    17/06/1903', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 12-Dec-1877 in Vamospercs.  Bride born 14-Aug-1884 in Peneszlek.', '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 1', '    ', '    160-2 & 161-1', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,David', '    ', '', '     ROSENFELD', '    ', '    ,Regina', '   ', '', '    Herman/LOVINGER(Klara)', '    ', '    Jozsef/FEHAR(Borbala)', '   ', '', '    23', '    ', '    22', '   ', '', '    13/10/1909', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 21-Feb-1886, residence=Margitta.  Bride born 08-Aug-1887, residence=Vamospercs.  Groom's father is deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1909-27', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jeno', '    ', '', '     STEINER', '    ', '    ,Berta', '   ', '', '    Simon/HEUSLER(Juliska)', '    ', '    Jakab/WEISHAUS(Leni)', '   ', '', '    22', '    ', '    19', '   ', '', '    29/03/1911', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 24-Oct-1888, residence=Vamospercs.  Bride born 14-Jun-1891, residence=Vamospercs.  Groom's father and Bride's father are both deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1911-24', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Antal', '    ', '', '     WEISZ', '    ', '    ,Hermina', '   ', '', '    Mayer/FARKAS(Julianna)', '    ', '    Jakab/SCHWARCZ(Regina)', '   ', '', '    21', '    ', '    23', '   ', '', '    05-Jul-13', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 18-Feb-1892, residence Ovasfelsofalu.  Bride born 14-Dec-1889, residence=Vamospercs.  Grooms' mother is deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1913-18', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Juda', '    ', '', '     KRAUSZ', '    ', '    ,Jenny', '   ', '', '    Moricz/Fanny(KŐNIG)', '    ', '    Tivadar/Leonora(BISENZER)', '   ', '', '    25', '    ', '    21', '   ', '', '    12-Sep-1897', '    ', '    Magyar-Ovár', '    ', '    Magyar-Ovár', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Groom born in Dunaszerdahely, bride born in Moson', '   ', '', '    LDS', '    ', '     2343271', '    ', '', '    16', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ŐSTREICHER', '    ', '    ,Miksa Mihaly', '    ', '', '     UNGAR', '    ', '    ,Leonora', '   ', '', '    Josef/Katalin(WEISZ)', '    ', '    Lipot/Betty(KESZTLER)', '   ', '', '    27', '    ', '    21', '   ', '', '    09-May-05', '    ', '    Magyar-Ovár', '    ', '    Magyar-Ovár', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Groom born in Karczag, bride born in Moson', '   ', '', '    LDS', '    ', '     2343271', '    ', '', '    26', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Miksa', '    ', '', '     BRUDER', '    ', '    ,Eva', '   ', '', '    Gabor/Fani(SPULLER)', '    ', '    Jakab/Franziska(HOMMERL)', '   ', '', '    36', '    ', '    35', '   ', '', '    02-Feb-1896', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    5', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Armin Israel', '    ', '', '     KOHN', '    ', '    ,Juli', '   ', '', '    Zsigmund/Rosalia(WEISS)', '    ', '    Jakab/Kati(LINDNER)', '   ', '', '    26', '    ', '    21', '   ', '', '    13/02/1902', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    9', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     NEUMANN', '    ', '    ,Jakab', '    ', '', '     WEISS', '    ', '    ,Anna', '   ', '', '    Mano/Leni(MUNK)', '    ', '    Adolf/Janka(LOWIN)', '   ', '', '    32', '    ', '    21', '   ', '', '    02-Feb-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    15', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Jozsef', '    ', '', '     WIDDER', '    ', '    ,Rgina', '   ', '', '    Henrik/Juli(FLESCH)', '    ', '    Sandor/Juli(MANDL)', '   ', '', '    39', '    ', '    31', '   ', '', '    06-Feb-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    16', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FISCHER', '    ', '    ,Gyula', '    ', '', '     WEISS', '    ', '    ,Riza', '   ', '', '    Vilmos/Betti(WOTTITZ)', '    ', '    Henrik/Juli(FLESCH)', '   ', '', '    28', '    ', '    25', '   ', '', '    03-Jun-00', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    17', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SZIGETI', '    ', '    ,Bernat', '    ', '', '     STEINER', '    ', '    ,Berta', '   ', '', '    Mor/Betti(WEISS)', '    ', '    Daniel/Julia(KOHN)', '   ', '', '    26', '    ', '    22', '   ', '', '    05-Jul-01', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    17', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Jakab', '    ', '', '     FLESCH', '    ', '    ,Matild', '   ', '', '    Henrik/Juli(FLESCH)', '    ', '    Zsigmond/Rozalia(WEISS)', '   ', '', '    32', '    ', '    23', '   ', '', '    15-Aug-1897', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    19', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     BAUMEL', '    ', '    ,Israel', '    ', '', '     WEINBERGER', '    ', '    ,Terez', '   ', '', '    Marton/Cilli(WEISS)', '    ', '    Israel/Pepi(WEISS)', '   ', '', '    51', '    ', '    38', '   ', '', '    20-Mar-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    19', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Ignacz', '    ', '', '     WEISS', '    ', '    ,Maria', '   ', '', '    David/Rozi(WEISS)', '    ', '    Henrik/Maria(LEHNER)', '   ', '', '    34', '    ', '    23', '   ', '', '    05-Jul-1896', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    20', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KNAPP', '    ', '    ,Jaka', '    ', '', '     LOWIN', '    ', '    ,Sara', '   ', '', '    Moricz/Betti(WEISZ)', '    ', '    Miksa/Roza(LOWIN)', '   ', '', '    28', '    ', '    21', '   ', '', '    01-Apr-05', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    1', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FELLNER', '    ', '    ,Jozef', '    ', '', '     FLESCH', '    ', '    ,Berta', '   ', '', '    Ignacz/Nettie(KRANCZ)', '    ', '    Szigmund/Sali(WEISZ)', '   ', '', '    27', '    ', '    22', '   ', '', '    27/06/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    22', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KERTESZ', '    ', '    ,Jakab', '    ', '', '     OSTERREICHER', '    ', '    ,Marcza', '   ', '', '    Lipot/Rozalia(WEISZ)', '    ', '    Lazar/Josefin(DEUTSCH)', '   ', '', '    31', '    ', '    24', '   ', '', '    09-Aug-03', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', "    Groom's father's name Krautblatt", '   ', '', '    LDS', '    ', '     2343389', '    ', '', '    34', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     SINGER', '    ', '    ,Iszak Ignaz', '    ', '', '     WEISS', '    ', '    ,Regi', '   ', '', '    Jakab/Rozi(GUTMANN)', '    ', '    Gabor/Fanni(WEISS)', '   ', '', '    53', '    ', '    39', '   ', '', '    29/08/1906', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    36', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     HAUSER', '    ', '    ,Nathan Ignac', '    ', '', '     WEISZ', '    ', '    ,Roza', '   ', '', '    Adolf/Katalin(WEINER)', '    ', '    Adolf/Hanni(LOWIN)', '   ', '', '    30', '    ', '    28', '   ', '', '    11-Jan-03', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    43', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     DEUTSCH', '    ', '    ,Jakab Salamon', '    ', '', '     WEISS', '    ', '    ,Regina', '   ', '', '    Abraham/Betti(BLAU)', '    ', '    Gabriel/Fanni(SPULLER)', '   ', '', '    39', '    ', '    39', '   ', '', '    17/11/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    47', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     BASS', '    ', '    ,Rafael', '    ', '', '     GERSTMANN', '    ', '    ,Malvina', '   ', '', '    Samuel/Fanni(SCHNABLE)', '    ', '    Samu/Laura(DEUTSCH)', '   ', '', '    28', '    ', '    22', '   ', '', '    22/11/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    50', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ZILZER', '    ', '    ,Dr. JenO', '    ', '', '     SOMMER', '    ', '    ,Dr. Adolf', '   ', '', '    Jozsef/Regina(WEISS)', '    ', '    Ilona/Roza(SCHNABL)', '   ', '', '    28', '    ', '    20', '   ', '', '    25/12/1905', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    53', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Moses', '    ', '', '     SCHWIMMER', '    ', '    ,Kati', '   ', '', '    Marton/Katti()', '    ', '    Salamon / [Samuel]/Mari([WEISZ])', '   ', '', '    21', '    ', '    17', '   ', '', '    06-Nov-1861', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Groom's year of wed: 1840 / Bride's year of wed: 1844", '   ', '', '    LDS 642810', '    ', '    282-009', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     LICHTMAN', '    ', '    ,Jonas', '    ', '', '     WEISZ', '    ', '    ,Mina', '   ', '', '    Isak/Fani()', '    ', '    Isak/Rosa()', '   ', '', '    23', '    ', '    17', '   ', '', '    27-Aug-1862', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Bokony Szabolcs / Bride born in: Nanas / Groom's year of wed: 1839 / Bride's year of wed: 1845 / Groom's date of death: '25-Aug-1894", '   ', '', '    LDS 642810', '    ', '    283-005', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Ludwig', '    ', '', '     LEFKOWITZ', '    ', '    ,Mari', '   ', '', '    Jonas/Hani()', '    ', '    David/Anna()', '   ', '', '    27', '    ', '    20', '   ', '', '    26-Apr-1865', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Dada / Bride born in: Szobrancz / Groom's year of wed: 1838 / Bride's year of wed: 1845", '   ', '', '    LDS 642810', '    ', '    284-007', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Abraham', '    ', '', '     WEISZ', '    ', '    ,Zsuzsana', '   ', '', '    -/-()', '    ', '    -/-()', '   ', '', '    56', '    ', '    52', '   ', '', '    13-Oct-1870', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Zenta / Bride born in: T. Dob / Groom's year of wed: 1814 / Bride's year of wed: 1818", '   ', '', '    LDS 642810', '    ', '    289-009', '    ', '', ''],
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', ''],
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Zsigmond', '    ', '', '     STERN', '    ', '    ,Rebeka', '   ', '', '    Ignacz/Sara(SCHWARTZ)', '    ', '    Jozsef/Sara(WEISZ)', '   ', '', '    23', '    ', '    20', '   ', '', '    20-Jun-1877', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '01-Jun-1854 / Bride's weddate: '10-Apr-1858", '   ', '', '    LDS 642810', '    ', '    294-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Ludwig / Lazar', '    ', '', '     FREIREICH', '    ', '    ,Klara', '   ', '', '    Ignatz/Hani()', '    ', '    Mozes/Hani / Hinde(SCHWARTZ)', '   ', '', '    23', '    ', '    18', '   ', '', '    05-Mar-1878', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Mad / Bride born in: Nanas / Groom's year of wed: 1855 / Bride's year of wed: 1860", '   ', '', '    LDS 642810', '    ', '    296-002', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     ROTH', '    ', '    ,Salamon', '    ', '', '     STERN', '    ', '    ,Fani', '   ', '', '    Jozsef/Maria(ROTH)', '    ', '    Lajos/Katalin(WEISZ)', '   ', '', '    25', '    ', '    20', '   ', '', '    26-Aug-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '29-May-1857 / Bride's weddate: '10-Jun-1862", '   ', '', '    LDS 642810', '    ', '    298-007', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KELEMEN', '    ', '    ,Herman', '    ', '', '     ELLBOGEN', '    ', '    ,Mari', '   ', '', '    Jozsef/Sara(WEISZ)', '    ', '    Marton/Juliana(FRIEDMAN)', '   ', '', '    24', '    ', '    21', '   ', '', '    19-Oct-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: H. Dorog / Bride born in: Nanas / Groom's year of wed: 1856 / Bride's year of wed: 1859", '   ', '', '    LDS 642810', '    ', '    298-008', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     FOGEL', '    ', '    ,Mozes', '    ', '', '     LANDESZMAN', '    ', '    ,Regina', '   ', '', '    Ferencz / Tzvi Hirsch/Hani / Chanah(GOLDSTEIN)', '    ', '    Bernat / Jakab / Yisachar Ber/Fani / Feige(WEISZ)', '   ', '', '    24', '    ', '    21', '   ', '', '    19-Oct-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '02-May-1858 / Bride's year of wed: 1859", '   ', '', '    LDS 642810', '    ', '    298-009', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KATZ', '    ', '    ,Moritz', '    ', '', '     SCHWARTZ', '    ', '    ,Lina', '   ', '', '    Herman/Rebeka(WEISZ)', '    ', '    Emanuel/Rozalia(SPITZER)', '   ', '', '    23', '    ', '    18', '   ', '', '    30-May-1882', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nyir Mada / Bride born in: Nanas / Groom's year of wed: 1859 / Bride's year of wed: 1864", '   ', '', '    LDS 642810', '    ', '    300-002', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Ignatz', '    ', '', '     LICHTMAN', '    ', '    ,Zali', '   ', '', '    Gershon/Fani(SCHWARTZ)', '    ', '    Jonasz/Luzi(WEISZ)', '   ', '', '    24', '    ', '    19', '   ', '', '    08-May-1883', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '14-Feb-1857 / Bride's year of wed: 1864", '   ', '', '    LDS 642810', '    ', '    301-003', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Hersch Arje', '    ', '', '     GOLDBERGER', '    ', '    ,Betti', '   ', '', '    Zindel/Leni(WEISZ)', '    ', '    Izsak/Mindel(KUPFERSTEIN)', '   ', '', '    23', '    ', '    19', '   ', '', '    12-Feb-1884', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: M. Szighet / Bride born in: Nanas / Groom's year of wed: 1861 / Bride's weddate: '03-Nov-1864", '   ', '', '    LDS 642810', '    ', '    302-001', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     KELEMEN', '    ', '    ,Aron', '    ', '', '     HAMMER', '    ', '    ,Mari / Golde', '   ', '', '    Jozsef/Sara / Serel(WEISZ)', '    ', '    Samuel / Shmuel Dov/Sara(FELDMAN)', '   ', '', '    29', '    ', '    23', '   ', '', '    16-Mar-1886', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Hajdu Dorog / Bride born in: Nanas / Groom's year of wed: 1857 / Bride's weddate: '02-Jan-1861", '   ', '', '    LDS 642810', '    ', '    303-002', '    ', '', ''],
['', '', '', '', ''],
['', '', '', '     SILBER', '    ', '    ,Samuel / Shmuel', '    ', '', '     LUSZTIG', '    ', '    ,Mari / Mattel', '   ', '', '    Gabriel/Sara(KLEIN)', '    ', '    Jozsef/Hani(WEISZ)', '   ', '', '    86', '    ', '    35', '   ', '', '    11-Apr-1886', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Jozefof Germany / Bride born in: T. Lok / Groom's year of wed: 1800 / Bride's year of wed: 1851", '   ', '', '    LDS 642810', '    ', '    303-003', '    ', '', ''],
]


#DONE - cannot use this as after this we cannot identify the field content
#cleans records list from "" or space elements
def clean_jg_input(data_in):
        return [[element.strip() for element in row if element.strip() != ''] for row in data_in]


#DONE
#detect lines to be ignored: title and filler lines
def ignore_jg_lines(line):
        if ( line[2] == '    Name' or line[2] == '    Groom' or line[3] == "") :
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


def single_quote_erase(data):
    return re.sub("'", "", data)

def single_quote_s_erase(data):
    return re.sub("'s", "", data)

def re_sub_dot(data):
    return re.sub("\.", " ", data)


def re_sub_slash2comma(data):
    return re.sub("/", ",", data)


def parents_names(item, data_out):
#    print("date in:", item)
    data_out.append(item[:item.rfind("/")]) #father name
    data_out.append(item[item.rfind("(")+1:item.rfind(")")]) # Mother maiden
    data_out.append(item[item.rfind("/")+1:item.find("(")]) # mother name
    return


#adjust JG wed - one list/line input - 2 lines output : Groom and Bride
def adjust_jg_wed(row, groom_out, bride_out):
    groom_sure_idx = 0

    row_idx = 3
    #Grooms & Brides Surename [0]
    groom_out.append(row[row_idx].strip())
    bride_out.append(row[row_idx].strip())
    row_idx += 2

    #Grooms given name [1]
    groom_out.append(re_comma2space(row[row_idx]).strip())
    row_idx += 5

    #Bride given name [1]
    bride_out.append(re_comma2space(row[row_idx]).strip())
    row_idx -=2

    #Brides Maiden [0] grooms maiden is fathers surename (if not changed then same, but this way each individual has its surename)
    bride_out.append(row[row_idx].strip())
    groom_out.append(groom_out[groom_sure_idx])
    row_idx += 5

    #Groom parents [2-5]: father sure, father name, mothers maiden, mother name
    parents_names(row[row_idx].strip(), groom_out)
    row_idx += 2

    #Brides parents [2-5]: father sure, father name, mothers maiden, mother name
    parents_names(row[row_idx].strip(), bride_out)
    row_idx += 8

    # wedding date [6]; year field will be inserted in insert method
    bride_out.append(row[row_idx].strip())
    groom_out.append(bride_out[-1])
    row_idx -= 5

    #Groom age [8]
    groom_out.append(row[row_idx].strip())
    if groom_out[-1].find("-") == -1:
        groom_out[-1] = re.sub('[^0-9]', "", groom_out[-1])
    else:
        bride_out[-1] = "noAge"
    row_idx +=2

    #bride age [8]
    bride_out.append(row[row_idx].strip())
    if bride_out[-1].find("-") == -1:
        bride_out[-1] = re.sub('[^0-9]', "", bride_out[-1])
    else:
        bride_out[-1] = "noAge"
    row_idx += 5

    #Towns - town born is the last field. need to change places
    groom_out.append(row[row_idx].strip())
    bride_out.append(row[row_idx].strip())
    row_idx += 2
    groom_out.append(row[row_idx].strip())
    bride_out.append(row[row_idx].strip())
    row_idx += 2
    groom_out.append(row[row_idx].strip())
    bride_out.append(row[row_idx].strip())
    row_idx += 2
    groom_out.append(row[row_idx].strip())
    bride_out.append(row[row_idx].strip())
    row_idx += 3

    #comment field [12]
    groom_out.append(row[row_idx].strip())
    if groom_out[-1] == '':
        groom_out[-1] = "noComment"
        bride_out.append(groom_out[-1])
        row_idx -= 1
    else:
        bride_out.append(row[row_idx].strip())

    # source + record + Image details [14]; check for different schemes
    row_idx += 3
    groom_out.append(row[row_idx].strip() + " " + row[row_idx+2].strip())
    if row[row_idx+4] != '':
        groom_out[-1] += (row[row_idx+4].strip() + " # " + row[row_idx+6].strip())

    bride_out.append(groom_out[-1])
#    print("check:",  bride_out, "||" , groom_out, "||" , row[row_idx-2:row_idx+10])

    return


#Done
def name_change_from_comment(data):
    data = re_sub_slash2comma(data)
    comment_split = re.split(",", data)
    for item in comment_split:
        if re.search("hanged", item) != none:
            item = single_quote_to_space(item[item.find("hanged to ") + 9:].split()[0]).strip().upper()
            return item
    return "noCName"



#DONE
def town_born_from_comment(data):
#search in each comment portion, order is not guranteed, split per commnet, father and mother but not 'parents'
    data = re_sub_colon(data)
    groom_pattern = 'room' # Groom #todo saw one time with grrom
    bride_pattern = 'ride' # Bride
    groom_tb = 'noTB'
    bride_tb = "noTB"
    item = data

    find_groom = item.find(groom_pattern)
    find_bride = item.find(bride_pattern)
#    print("found:", find_groom, find_bride)
    if (find_bride & find_groom) == -1: #no father or mother found
        return groom_tb, bride_tb
    if (find_bride != -1) & (find_groom != -1): #both parents found
        if find_groom > find_bride:  # father comes AFTER mother
            groom_tb = find_town(item[find_groom+5:])
            bride_tb = find_town(item[find_bride+5:find_groom-2])
        else:
            bride_tb = find_town(item[find_bride+5:])
            groom_tb = find_town(item[find_groom+5:find_bride-2])
    elif find_groom == -1: #father not found
        bride_tb = find_town(item[find_bride + 5:])
    else:
        groom_tb = find_town(item[find_groom + 5:])
#    print("towns:", groom_tb, "||", bride_tb, "||", data)
    return groom_tb, bride_tb


def find_town(item):
    from_town = item.find('from ')
    born_in = item.find('orn in')
#    print("input for town search:", item)
    if from_town != -1:
        semi_col = item.find(";")
        if semi_col == -1:
            return item[from_town +5:]
        else:
            return item[from_town +5: semi_col]
    elif born_in != -1: # found "orn in"
        if item.find("/") != -1:
            return item[born_in + 6: item.find("/")].strip()
        else:
            return item[born_in + 6: item.find(",")].strip()
    elif item.find(" in ") != -1:
        return item[item.find(" in ") + 4: item.find(".")].strip()
    elif item.find("b ") != -1 or item.find("B ") != -1:
        return item.split()[1].strip()
    elif item.find("irthplace") != -1:
        town = item.find("irthplace")
        return item[town+11: item.find("/")].strip()
    elif item.find("residence") != -1:
        town = item.find("residence")
        return item[town+10:item.find(".")].strip()
    else:
        return "noTB"

#DONE
def birth_date_from_comment(data):
#search in each comment portion, order is not guranteed, split per commnet
    data = re_sub_colon(data)
    birth_date_pattern = "irthdate" #date
#    birth_year_pattern = "of birth" #year
    born_date_pattern = "born"
#    wed_year_pattern = "of wed" #year
    wed_date_pattern = "weddate" #date
    groom_pattern = 'room' # Groom #todo saw one time with grrom
    bride_pattern = 'ride' # Bride
    groom_bd = 'noBD'
    bride_bd = "noBD"
    find_bd = -1
    find_born = -1
    find_weddate = -1
    find_bd = data.find(birth_date_pattern)
    find_born = data.find(born_date_pattern)
    find_weddate = data.find(wed_date_pattern)

#    print("found:", find_groom, find_bride)
    if (find_bd & find_born & find_weddate) == -1: # no birth date/year pattern found
        return groom_bd, bride_bd
    comment_split = re.split(r'[.,;/]', data) # split comment by ,  or ; or /
#    print("Date split:", comment_split)
    for item in comment_split:
        find_bd = item.find(birth_date_pattern)
        find_born = item.find(born_date_pattern)
        find_weddate = item.find(wed_date_pattern)

        if (find_bd != -1):
            find_groom = item[find_bd - 8:].find(groom_pattern)
            if (find_groom != -1 ): # find groom
                groom_bd = find_birth_date(item[find_bd:], len(birth_date_pattern))
            else:
                bride_bd = find_birth_date(item[find_bd:], len(birth_date_pattern))
        elif (find_born != -1) & (item.find("orn in") == -1): #"born" but not "born in <place>"
            find_groom = item[find_born - 6:].find(groom_pattern)
            if (find_groom != -1 ): # find groom
                groom_bd = find_birth_date(item[find_born:], len(born_date_pattern))
            else:
                bride_bd = find_birth_date(item[find_born:], len(born_date_pattern))
        elif (find_weddate != -1) : #find weddate
            find_groom = item[find_weddate - 8:].find(groom_pattern)
            if (find_groom != -1 ): # find groom
                groom_bd = find_birth_date(item[find_weddate:], len(wed_date_pattern))
            else:
                bride_bd = find_birth_date(item[find_weddate:], len(wed_date_pattern))
    groom_bd = single_quote_erase(groom_bd)
    bride_bd = single_quote_erase(bride_bd)
    return groom_bd, bride_bd


def death_date_from_comment(data):
    death_date_pattern = "date of death"
    find_death_date = data.find(death_date_pattern)
    groom_dd = "noDD"
    bride_dd = "noDD"

    if find_death_date != -1:
        groom_pattern = 'room'  # Groom #todo saw one time with grrom
        bride_pattern = 'ride'  # Bride
        find_groom = data[find_death_date - 7:].find(groom_pattern)
        find_bride = data[find_death_date - 7:].find(bride_pattern)
        if (find_groom != -1 ): # find groom
            groom_dd = data[find_death_date+14:].strip()
            groom_dd = single_quote_erase(groom_dd)
        else:
            bride_dd = data[find_death_date+14:].strip()
            bride_dd = single_quote_erase(bride_dd)

    return groom_dd, bride_dd
        


#DONE
def birth_year_from_comment(data):
#search in each comment portion, order is not guranteed, split per commnet
    data = re_sub_colon(data)
    birth_year_pattern = "of birth" #year
    wed_year_pattern = "of wed" #year
    groom_pattern = 'room' # Groom #todo saw one time with grrom
    bride_pattern = 'ride' # Bride
    groom_by = 'noBY'
    bride_by = "noBY"
    find_by = -1
    find_wed = -1

    find_by = data.find(birth_year_pattern)
    find_wed = data.find(wed_year_pattern)

    if (find_by & find_wed) == -1:  # no birth year pattern found
        return groom_by, bride_by

    comment_split = re.split(r'[,;/]', data)  # split comment by ,  or ; or /
    for item in comment_split:
        find_by = item.find(birth_year_pattern)
        find_wed = item.find(wed_year_pattern)

        if find_by != -1:
            find_groom = item[find_by - 13:].find(groom_pattern)
            if find_groom != -1:  # find groom
                groom_by = find_birth_date(item[find_by:], len(birth_year_pattern))
            else:
                bride_by = find_birth_date(item[find_by:], len(birth_year_pattern))
        elif find_wed != -1 : #find wed
             find_groom = item[find_wed - 16:].find(groom_pattern)
             if find_groom != -1: # find groom
                 groom_by = find_birth_date(item[find_wed:], len(wed_year_pattern))
             else:
                 bride_by = find_birth_date(item[find_wed:], len(wed_year_pattern))
    return groom_by, bride_by


def family_from_comment(data):
    data = re_sub_colon(data)
    orphan_pattern = "orphan"
    deceased_pattern = "deceased"
    father_pattern = "father"
    mother_pattern = "mother"
    both_pattern = "both"
    both_parents_pattern = "are both"
    groom_pattern = 'room' # Groom #todo saw one time with grrom
    bride_pattern = 'ride' # Bride
    groom_fam = "noFM noFR"
    bride_fam = "noFM noFR"

    find_orphan = data.find(orphan_pattern)
    find_deceased = data.find(deceased_pattern)
    find_father = data.find(father_pattern)
    find_mother = data.find(mother_pattern)
    find_both = data.find(both_pattern)
    find_both_parents = data.find(both_parents_pattern)

    if (find_orphan & find_deceased & find_father & find_mother) == -1:
        return groom_fam, bride_fam

    comment_split = re.split(r'[,.;/]', data)  # split comment by ,  or ; or /
    for item in comment_split:
        find_orphan = item.find(orphan_pattern)
        find_deceased = item.find(deceased_pattern)
        find_father = item.find(father_pattern)
        find_mother = item.find(mother_pattern)
        find_both = item.find(both_pattern)
        item = item.strip()

        if find_deceased != -1: #find Deceased
            find_groom = item.find(groom_pattern)
            find_bride = item.find(bride_pattern)

            if find_both != -1:
                if find_groom != -1:
                    groom_fam = both_pattern + " " + deceased_pattern
                if find_bride != -1:
                    bride_fam = both_pattern + " " + deceased_pattern
            if find_groom != -1:  # find groom
                if find_both != -1: #todo check what kind of BOTH this is - can be "Groom's father and Bride's father are both deceased."
                    groom_fam = both_pattern + " " + deceased_pattern
                elif find_father != -1:
                    groom_fam = father_pattern + " " + deceased_pattern
                else:
                    groom_fam = mother_pattern + " " + deceased_pattern
            else:
                if find_both != -1:
                    bride_fam = both_pattern + " " + deceased_pattern
                elif find_father != -1:
                    bride_fam = father_pattern + " " + deceased_pattern
                else:
                    bride_fam = mother_pattern + " " + deceased_pattern
        elif find_orphan != -1:  # find orphan
            find_groom = item.find(groom_pattern)
            if find_groom != -1:  # find groom
                groom_fam = both_pattern + " " + deceased_pattern
            else:
                bride_fam = both_pattern + " " + deceased_pattern
        elif find_father != -1: # father's name
            find_groom = item.find(groom_pattern)
            find_bride = item.find(bride_pattern)
            if find_groom != -1:  # find groom
                groom_fam = item[item.find(" "):]
            else:
                bride_fam = item[item.find(" "):]
        elif find_mother != -1: # Mother's name
            find_groom = item.find(groom_pattern)
            find_bride = item.find(bride_pattern)
            if find_groom != -1:  # find groom
                groom_fam = item[find_groom:]
            else:
                bride_fam = item[find_bride:]
        else:
            continue
    groom_fam = single_quote_s_erase(groom_fam).strip()
    groom_fam = re.sub("name ", "", groom_fam)
    bride_fam = single_quote_s_erase(bride_fam).strip()
    bride_fam = re.sub("name ", "", bride_fam)

#    print("families:", groom_fam , "||", bride_fam)
    return groom_fam, bride_fam


#DONE
def find_birth_date(data, find):
#found the pattern - need to retrieve the actual requested data
    return data[find:].split()[0].strip()


#Done
def comment_exists(data):
    if data in ["noComment"]:
        return False
    else:
        return True

#DONE
def insert_jg_wed_fields(row):
    wed_date_idx = 6
    wed_year_idx = 7
    birth_date_idx = 9
    birth_year_idx = 20
    death_date_idx = 21
    death_year_idx = 22
    other_fam_idx = 10
    other_fam_relation_idx = 11
    town_born_idx = 12
    name_change_idx = 18

    row.insert(wed_year_idx,year_from_date(row[wed_date_idx]))  # year of wed from wed date
    row.insert(birth_date_idx,"noBD")
    row.insert(other_fam_idx,"noOF")
    row.insert(other_fam_relation_idx,"noFR")
    row.insert(birth_year_idx,"noBY")
    row.insert(town_born_idx,"noTB")
    row.insert(name_change_idx,"noCName")
    row.insert(death_date_idx,"noDD")
    row.insert(death_year_idx, "noDY")
    return


def build_jg_wed(data, data_out):
    groom_idx = 0
    bride_idx = 1
    comment_idx = 17
    wed_year_idx = 7
    wed_age_idx = 8
    birth_date_idx = 9
    birth_year_idx = 20
    death_date_idx = 21
    death_year_idx = 22
    other_fam_idx = 10
    other_fam_rel_idx = 11
    town_born_idx = 12
    name_change_idx = 18
    couple_town = []
    couple_birth = []
    couple_death = []

    for row in data:
        if ignore_jg_lines(row):
            continue
        data_out.append([])
        data_out.append([])
        groom = data_out[groom_idx]
        bride = data_out[bride_idx]

        adjust_jg_wed(row, groom, bride)  # adjust relevant line
        insert_jg_wed_fields(groom)  # insert elements to full size of row
        insert_jg_wed_fields(bride)  # insert elements to full size of row
        comment = data_out[groom_idx][comment_idx]

        if comment_exists(comment):  #check if comment != ""

            couple_town = town_born_from_comment(comment)
            groom[town_born_idx] = couple_town[0]
            bride[town_born_idx] = couple_town[1]

            couple_birth = birth_date_from_comment(comment)
            groom[birth_date_idx] = couple_birth[0]
            bride[birth_date_idx] = couple_birth[1]

            couple_year = birth_year_from_comment(comment)
            if (groom[birth_date_idx] != "noBD"): #if date exists - take year from date
                groom[birth_year_idx] = year_from_date(groom[birth_date_idx])
            elif (groom[wed_age_idx] == "noAge"):
                groom[birth_year_idx] = couple_year[0]
            else:
                groom[birth_year_idx] = estimated_birth_year(groom[wed_year_idx], int(groom[wed_age_idx])) #calculate from wed year and age

            if (bride[birth_date_idx] != "noBD"):#if date exists - take year from date
                bride[birth_year_idx] = year_from_date(bride[birth_date_idx])
            elif (bride[wed_age_idx] == "noAge") :
                bride[birth_year_idx] = couple_year[1]
            else:
                bride[birth_year_idx] = estimated_birth_year(bride[wed_year_idx], int(bride[wed_age_idx]))

#            print("groom comment:",  comment)

            couple_death = death_date_from_comment(comment)
            groom[death_date_idx] = couple_death[0]
            groom[death_year_idx] = year_from_date(groom[death_date_idx])
            bride[death_date_idx] = couple_death[1]
            bride[death_year_idx] = year_from_date(bride[death_date_idx])

            couple_family = family_from_comment(comment)
            find_space_groom = couple_family[0].find(" ")
            find_space_bride = couple_family[1].find(" ")
            groom[other_fam_idx] = couple_family[0][:find_space_groom]
            groom[other_fam_rel_idx] = couple_family[0][find_space_groom+1:]
            bride[other_fam_idx] = couple_family[1][:find_space_bride]
            bride[other_fam_rel_idx] = couple_family[1][find_space_bride+1:]
#            print("groom:", groom[other_fam_idx], "||", groom[other_fam_rel_idx])
#            print("bride:", bride[other_fam_idx], "||", bride[other_fam_rel_idx])

        #prepare for next lines
        groom_idx += 2
        bride_idx += 2
    return



data_out = [[]] # temporary output list of lists
#data_w =[[]] # wed date list of lists
none = re.search("xxx", "") #set the value for re.search = none

build_jg_wed(jg_w_input, data_out)

for row in data_out:
    print(row[17])





#[
['', '', '', '     FENYO (FREIWILLIG)', '    ', '    ,Mayer', '    ', '', '     HERCSKA', '    ', '    ,Adolfin    (Frumel)', '   ', '', '    Moritz/Regi(WEISZ)', '    ', '    Heinrich/Netti(NEUBAUER)', '   ', '', '    33', '    ', '    20', '   ', '', '    08-Jan-1895', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', "    groom's father FREIWILLIG", '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jacob', '    ', '', '     NOVAK', '    ', '    ,Berta', '   ', '', '    Adam/Marie(NEUMAN)', '    ', '    Nathan/Josefine(NEUMAN)', '   ', '', '    27', '    ', '    19', '   ', '', '    12-Apr-1888', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '    groom from Ivanka, Veszprem m.', '   ', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    6', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jakab', '    ', '', '     NEUMAN', '    ', '    ,Terez', '   ', '', '    Herman/Hani(HOCHFELDER)', '    ', '    Miksa/Rosa(FELBERT)', '   ', '', '    23', '    ', '    24', '   ', '', '    07-Jul-1895', '    ', '    Hlinik', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    7', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Simon Markus', '    ', '', '     SONNENFELD', '    ', '    ,Marie', '   ', '', '    Samuel/Marie(PREISAK)', '    ', '    Leopold/Hani(LOVENBEIN)', '   ', '', '    26', '    ', '    23', '   ', '', '    11-Sep-1894', '    ', '    Nagy-Bittse', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    12', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     HOCHFELDER', '    ', '    ,Gyula (Kohn)', '    ', '', '     WEISZ', '    ', '    ,Jeannette', '   ', '', '    Jozsef (Kohn)/Josefina(TAUSSIK)', '    ', '    Armin/Hanni(HOCHFELDER)', '   ', '', '    24', '    ', '    20', '   ', '', '    02-Sep-1890', '    ', '    Viszoka-     Makov', '    ', '    Bittse', '    ', '    Bittse', '    ', '    Trencsén', '   ', '', '', '', '    LDS', '    ', '     1978901', '    ', '    (3)', '    ', '    13', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     LEWI', '    ', '    ,Abraham', '    ', '', '     GELBERGER', '    ', '    ,Hermina', '   ', '', '    Izrael/Maria(WEISZ)', '    ', '    Peter/Lina(KELLER)', '   ', '', '    29', '    ', '    24', '   ', '', '    09-Mar-1897', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 19-May-1867 in Nagy Bajom.  Bride born 04-Jan-1873 in Vamospercs.', '   ', '', '    LDS', '    ', '     2127458', '    ', '    , Item 3', '    ', '    47-2 & 48-1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Jakab', '    ', '', '     ROSENFELD', '    ', '    ,Fani', '   ', '', '    Moritz/Sali(KELLER)', '    ', '    Jozsef/Veronika(WEISZ)', '   ', '', '    24', '    ', '    21', '   ', '', '    28-Apr-1897', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 17-Aug-1872 in Vamospercs.  Bride born 20-Feb-1876 in Vamospercs.', '   ', '', '    LDS', '    ', '     2127458', '    ', '    , Item 3', '    ', '    50-2 & 51-1', '    ', '', '']
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', '']
['', '', '', '', ''],
['', '', '', '     FRANK', '    ', '    ,Sie Sami', '    ', '', '     ROSENFELD', '    ', '    ,Helen', '   ', '', '    Matyas/Lina(HELEN)', '    ', '    Jozsef/Verona(WEISZ)', '   ', '', '    25', '    ', '    20', '   ', '', '    23/10/1901', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 30-Oct-1875 in Vamospercs.  Bride born 11-Jul-1881 in Vamospercs.  Record duplicated on 35-2 & 36-1.', '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 1', '    ', '    107-2 & 108-1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     ROSENFELD', '    ', '    ,Jonas', '    ', '', '     EGRI', '    ', '    ,Vilma', '   ', '', '    Jozsef/Veronika(WEISZ)', '    ', '    Abraham/Hani(LEICHTMANN)', '   ', '', '    25', '    ', '    19', '   ', '', '    17/06/1903', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', '    Groom born 12-Dec-1877 in Vamospercs.  Bride born 14-Aug-1884 in Peneszlek.', '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 1', '    ', '    160-2 & 161-1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     LEITNER', '    ', '    ,Sandor', '    ', '', '     WEISZ', '    ', '    ,Helena', '   ', '', '    Mihaly/Sali(LEITNER)', '    ', '    Simon/Julianna(HAUSLER)', '   ', '', '    27', '    ', '    20', '   ', '', '    16/03/1904', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 18-Jan-1876 in Vamospercs.  Bride born 04-Mar-1886 in Ertarcsa.  Bride's mother is deceased.", '   ', '', '    LDS', '    ', '     2127459', '    ', '    , Item 2', '    ', '    18-2 & 19-1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,David', '    ', '', '     ROSENFELD', '    ', '    ,Regina', '   ', '', '    Herman/LOVINGER(Klara)', '    ', '    Jozsef/FEHAR(Borbala)', '   ', '', '    23', '    ', '    22', '   ', '', '    13/10/1909', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 21-Feb-1886, residence=Margitta.  Bride born 08-Aug-1887, residence=Vamospercs.  Groom's father is deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1909-27', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Jeno', '    ', '', '     STEINER', '    ', '    ,Berta', '   ', '', '    Simon/HEUSLER(Juliska)', '    ', '    Jakab/WEISHAUS(Leni)', '   ', '', '    22', '    ', '    19', '   ', '', '    29/03/1911', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 24-Oct-1888, residence=Vamospercs.  Bride born 14-Jun-1891, residence=Vamospercs.  Groom's father and Bride's father are both deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1911-24', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Antal', '    ', '', '     WEISZ', '    ', '    ,Hermina', '   ', '', '    Mayer/FARKAS(Julianna)', '    ', '    Jakab/SCHWARCZ(Regina)', '   ', '', '    21', '    ', '    23', '   ', '', '    05-Jul-13', '    ', '    Vamospercs', '    ', '    Vamospercs', '    ', '    Balmazujvaros', '    ', '    Hajdú', '   ', '', "    Groom born 18-Feb-1892, residence Ovasfelsofalu.  Bride born 14-Dec-1889, residence=Vamospercs.  Grooms' mother is deceased.", '   ', '', '    LDS', '    ', '     2261504', '    ', '    , Item 2', '    ', '    1913-18', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Juda', '    ', '', '     KRAUSZ', '    ', '    ,Jenny', '   ', '', '    Moricz/Fanny(KŐNIG)', '    ', '    Tivadar/Leonora(BISENZER)', '   ', '', '    25', '    ', '    21', '   ', '', '    12-Sep-1897', '    ', '    Magyar-Ovár', '    ', '    Magyar-Ovár', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Groom born in Dunaszerdahely, bride born in Moson', '   ', '', '    LDS', '    ', '     2343271', '    ', '', '    16', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     ŐSTREICHER', '    ', '    ,Miksa Mihaly', '    ', '', '     UNGAR', '    ', '    ,Leonora', '   ', '', '    Josef/Katalin(WEISZ)', '    ', '    Lipot/Betty(KESZTLER)', '   ', '', '    27', '    ', '    21', '   ', '', '    09-May-05', '    ', '    Magyar-Ovár', '    ', '    Magyar-Ovár', '    ', '    Moson', '    ', '    Moson', '   ', '', '    Groom born in Karczag, bride born in Moson', '   ', '', '    LDS', '    ', '     2343271', '    ', '', '    26', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Miksa', '    ', '', '     BRUDER', '    ', '    ,Eva', '   ', '', '    Gabor/Fani(SPULLER)', '    ', '    Jakab/Franziska(HOMMERL)', '   ', '', '    36', '    ', '    35', '   ', '', '    02-Feb-1896', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    5', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     FLESCH', '    ', '    ,Armin Israel', '    ', '', '     KOHN', '    ', '    ,Juli', '   ', '', '    Zsigmund/Rosalia(WEISS)', '    ', '    Jakab/Kati(LINDNER)', '   ', '', '    26', '    ', '    21', '   ', '', '    13/02/1902', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    9', '    ', '', '']
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', '']
['', '', '', '', ''],
['', '', '', '     NEUMANN', '    ', '    ,Jakab', '    ', '', '     WEISS', '    ', '    ,Anna', '   ', '', '    Mano/Leni(MUNK)', '    ', '    Adolf/Janka(LOWIN)', '   ', '', '    32', '    ', '    21', '   ', '', '    02-Feb-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    15', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Jozsef', '    ', '', '     WIDDER', '    ', '    ,Rgina', '   ', '', '    Henrik/Juli(FLESCH)', '    ', '    Sandor/Juli(MANDL)', '   ', '', '    39', '    ', '    31', '   ', '', '    06-Feb-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    16', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     FISCHER', '    ', '    ,Gyula', '    ', '', '     WEISS', '    ', '    ,Riza', '   ', '', '    Vilmos/Betti(WOTTITZ)', '    ', '    Henrik/Juli(FLESCH)', '   ', '', '    28', '    ', '    25', '   ', '', '    03-Jun-00', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    17', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     SZIGETI', '    ', '    ,Bernat', '    ', '', '     STEINER', '    ', '    ,Berta', '   ', '', '    Mor/Betti(WEISS)', '    ', '    Daniel/Julia(KOHN)', '   ', '', '    26', '    ', '    22', '   ', '', '    05-Jul-01', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    17', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Jakab', '    ', '', '     FLESCH', '    ', '    ,Matild', '   ', '', '    Henrik/Juli(FLESCH)', '    ', '    Zsigmond/Rozalia(WEISS)', '   ', '', '    32', '    ', '    23', '   ', '', '    15-Aug-1897', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    19', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     BAUMEL', '    ', '    ,Israel', '    ', '', '     WEINBERGER', '    ', '    ,Terez', '   ', '', '    Marton/Cilli(WEISS)', '    ', '    Israel/Pepi(WEISS)', '   ', '', '    51', '    ', '    38', '   ', '', '    20-Mar-1898', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    19', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISS', '    ', '    ,Ignacz', '    ', '', '     WEISS', '    ', '    ,Maria', '   ', '', '    David/Rozi(WEISS)', '    ', '    Henrik/Maria(LEHNER)', '   ', '', '    34', '    ', '    23', '   ', '', '    05-Jul-1896', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343388', '    ', '', '    20', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KNAPP', '    ', '    ,Jaka', '    ', '', '     LOWIN', '    ', '    ,Sara', '   ', '', '    Moricz/Betti(WEISZ)', '    ', '    Miksa/Roza(LOWIN)', '   ', '', '    28', '    ', '    21', '   ', '', '    01-Apr-05', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    1', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     FELLNER', '    ', '    ,Jozef', '    ', '', '     FLESCH', '    ', '    ,Berta', '   ', '', '    Ignacz/Nettie(KRANCZ)', '    ', '    Szigmund/Sali(WEISZ)', '   ', '', '    27', '    ', '    22', '   ', '', '    27/06/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    22', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KERTESZ', '    ', '    ,Jakab', '    ', '', '     OSTERREICHER', '    ', '    ,Marcza', '   ', '', '    Lipot/Rozalia(WEISZ)', '    ', '    Lazar/Josefin(DEUTSCH)', '   ', '', '    31', '    ', '    24', '   ', '', '    09-Aug-03', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', "    Groom's father's name Krautblatt", '   ', '', '    LDS', '    ', '     2343389', '    ', '', '    34', '    ', '', '']
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', '']
['', '', '', '', ''],
['', '', '', '     SINGER', '    ', '    ,Iszak Ignaz', '    ', '', '     WEISS', '    ', '    ,Regi', '   ', '', '    Jakab/Rozi(GUTMANN)', '    ', '    Gabor/Fanni(WEISS)', '   ', '', '    53', '    ', '    39', '   ', '', '    29/08/1906', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    36', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     HAUSER', '    ', '    ,Nathan Ignac', '    ', '', '     WEISZ', '    ', '    ,Roza', '   ', '', '    Adolf/Katalin(WEINER)', '    ', '    Adolf/Hanni(LOWIN)', '   ', '', '    30', '    ', '    28', '   ', '', '    11-Jan-03', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    43', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     DEUTSCH', '    ', '    ,Jakab Salamon', '    ', '', '     WEISS', '    ', '    ,Regina', '   ', '', '    Abraham/Betti(BLAU)', '    ', '    Gabriel/Fanni(SPULLER)', '   ', '', '    39', '    ', '    39', '   ', '', '    17/11/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    47', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     BASS', '    ', '    ,Rafael', '    ', '', '     GERSTMANN', '    ', '    ,Malvina', '   ', '', '    Samuel/Fanni(SCHNABLE)', '    ', '    Samu/Laura(DEUTSCH)', '   ', '', '    28', '    ', '    22', '   ', '', '    22/11/1903', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    50', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     ZILZER', '    ', '    ,Dr. JenO', '    ', '', '     SOMMER', '    ', '    ,Dr. Adolf', '   ', '', '    Jozsef/Regina(WEISS)', '    ', '    Ilona/Roza(SCHNABL)', '   ', '', '    28', '    ', '    20', '   ', '', '    25/12/1905', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '    ', '    Moson', '   ', '', '', '', '    LDS', '    ', '     2343389', '    ', '', '    53', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     LEFKOWITZ', '    ', '    ,Salamon', '    ', '', '     WEISZ', '    ', '    ,Maria', '   ', '', '    David/Anna()', '    ', '    Isak/Rosa()', '   ', '', '    23', '    ', '    20', '   ', '', '    09-Aug-1861', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Szobrancz / Bride born in: Nanas / Groom's year of wed: 1838 / Bride's year of wed: 1841 / Groom's date of death: '30-Mar-1886", '   ', '', '    LDS 642810', '    ', '    282-005', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Moses', '    ', '', '     SCHWIMMER', '    ', '    ,Kati', '   ', '', '    Marton/Katti()', '    ', '    Salamon / [Samuel]/Mari([WEISZ])', '   ', '', '    21', '    ', '    17', '   ', '', '    06-Nov-1861', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Groom's year of wed: 1840 / Bride's year of wed: 1844", '   ', '', '    LDS 642810', '    ', '    282-009', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     LICHTMAN', '    ', '    ,Jonas', '    ', '', '     WEISZ', '    ', '    ,Mina', '   ', '', '    Isak/Fani()', '    ', '    Isak/Rosa()', '   ', '', '    23', '    ', '    17', '   ', '', '    27-Aug-1862', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Bokony Szabolcs / Bride born in: Nanas / Groom's year of wed: 1839 / Bride's year of wed: 1845 / Groom's date of death: '25-Aug-1894", '   ', '', '    LDS 642810', '    ', '    283-005', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Ludwig', '    ', '', '     LEFKOWITZ', '    ', '    ,Mari', '   ', '', '    Jonas/Hani()', '    ', '    David/Anna()', '   ', '', '    27', '    ', '    20', '   ', '', '    26-Apr-1865', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Dada / Bride born in: Szobrancz / Groom's year of wed: 1838 / Bride's year of wed: 1845", '   ', '', '    LDS 642810', '    ', '    284-007', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     POLLAK', '    ', '    ,Abraham', '    ', '', '     WEISZ', '    ', '    ,Zsuzsana', '   ', '', '    -/-()', '    ', '    -/-()', '   ', '', '    56', '    ', '    52', '   ', '', '    13-Oct-1870', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Zenta / Bride born in: T. Dob / Groom's year of wed: 1814 / Bride's year of wed: 1818", '   ', '', '    LDS 642810', '    ', '    289-009', '    ', '', '']
['', '', '    Groom', '    ', '    Bride', '   ', '', "    Groom's Father / Mother", '    ', "    Bride's Father / Mother", '   ', '', '    Groom Age', '    ', '    Bride Age', '   ', '', '    MarriageDate', '    ', '    Marriage Town', '    ', '    Registration', '    ', '    Town', '    ', '    Jaras', '    ', '    Megye', '   ', '', '    Comments', '   ', '', '    Source', '    ', '    Record', '    ', '    Image#', '   ', '']
['', '', '', '', ''],
['', '', '', '     STERN', '    ', '    ,Zsigmond', '    ', '', '     STERN', '    ', '    ,Rebeka', '   ', '', '    Ignacz/Sara(SCHWARTZ)', '    ', '    Jozsef/Sara(WEISZ)', '   ', '', '    23', '    ', '    20', '   ', '', '    20-Jun-1877', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '01-Jun-1854 / Bride's weddate: '10-Apr-1858", '   ', '', '    LDS 642810', '    ', '    294-008', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     WEISZ', '    ', '    ,Ludwig / Lazar', '    ', '', '     FREIREICH', '    ', '    ,Klara', '   ', '', '    Ignatz/Hani()', '    ', '    Mozes/Hani / Hinde(SCHWARTZ)', '   ', '', '    23', '    ', '    18', '   ', '', '    05-Mar-1878', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Mad / Bride born in: Nanas / Groom's year of wed: 1855 / Bride's year of wed: 1860", '   ', '', '    LDS 642810', '    ', '    296-002', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     ROTH', '    ', '    ,Salamon', '    ', '', '     STERN', '    ', '    ,Fani', '   ', '', '    Jozsef/Maria(ROTH)', '    ', '    Lajos/Katalin(WEISZ)', '   ', '', '    25', '    ', '    20', '   ', '', '    26-Aug-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '29-May-1857 / Bride's weddate: '10-Jun-1862", '   ', '', '    LDS 642810', '    ', '    298-007', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KELEMEN', '    ', '    ,Herman', '    ', '', '     ELLBOGEN', '    ', '    ,Mari', '   ', '', '    Jozsef/Sara(WEISZ)', '    ', '    Marton/Juliana(FRIEDMAN)', '   ', '', '    24', '    ', '    21', '   ', '', '    19-Oct-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: H. Dorog / Bride born in: Nanas / Groom's year of wed: 1856 / Bride's year of wed: 1859", '   ', '', '    LDS 642810', '    ', '    298-008', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     FOGEL', '    ', '    ,Mozes', '    ', '', '     LANDESZMAN', '    ', '    ,Regina', '   ', '', '    Ferencz / Tzvi Hirsch/Hani / Chanah(GOLDSTEIN)', '    ', '    Bernat / Jakab / Yisachar Ber/Fani / Feige(WEISZ)', '   ', '', '    24', '    ', '    21', '   ', '', '    19-Oct-1880', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '02-May-1858 / Bride's year of wed: 1859", '   ', '', '    LDS 642810', '    ', '    298-009', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KATZ', '    ', '    ,Moritz', '    ', '', '     SCHWARTZ', '    ', '    ,Lina', '   ', '', '    Herman/Rebeka(WEISZ)', '    ', '    Emanuel/Rozalia(SPITZER)', '   ', '', '    23', '    ', '    18', '   ', '', '    30-May-1882', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nyir Mada / Bride born in: Nanas / Groom's year of wed: 1859 / Bride's year of wed: 1864", '   ', '', '    LDS 642810', '    ', '    300-002', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Ignatz', '    ', '', '     LICHTMAN', '    ', '    ,Zali', '   ', '', '    Gershon/Fani(SCHWARTZ)', '    ', '    Jonasz/Luzi(WEISZ)', '   ', '', '    24', '    ', '    19', '   ', '', '    08-May-1883', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Nanas / Bride born in: Nanas / Groom's weddate: '14-Feb-1857 / Bride's year of wed: 1864", '   ', '', '    LDS 642810', '    ', '    301-003', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KLEIN', '    ', '    ,Hersch Arje', '    ', '', '     GOLDBERGER', '    ', '    ,Betti', '   ', '', '    Zindel/Leni(WEISZ)', '    ', '    Izsak/Mindel(KUPFERSTEIN)', '   ', '', '    23', '    ', '    19', '   ', '', '    12-Feb-1884', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: M. Szighet / Bride born in: Nanas / Groom's year of wed: 1861 / Bride's weddate: '03-Nov-1864", '   ', '', '    LDS 642810', '    ', '    302-001', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     KELEMEN', '    ', '    ,Aron', '    ', '', '     HAMMER', '    ', '    ,Mari / Golde', '   ', '', '    Jozsef/Sara / Serel(WEISZ)', '    ', '    Samuel / Shmuel Dov/Sara(FELDMAN)', '   ', '', '    29', '    ', '    23', '   ', '', '    16-Mar-1886', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Hajdu Dorog / Bride born in: Nanas / Groom's year of wed: 1857 / Bride's weddate: '02-Jan-1861", '   ', '', '    LDS 642810', '    ', '    303-002', '    ', '', '']
['', '', '', '', ''],
['', '', '', '     SILBER', '    ', '    ,Samuel / Shmuel', '    ', '', '     LUSZTIG', '    ', '    ,Mari / Mattel', '   ', '', '    Gabriel/Sara(KLEIN)', '    ', '    Jozsef/Hani(WEISZ)', '   ', '', '    86', '    ', '    35', '   ', '', '    11-Apr-1886', '    ', '    Hajdunanas', '    ', '    Hajdunanas', '    ', "    Local Gov't.", '    ', '    Hajdú', '   ', '', "    Groom born in: Jozefof Germany / Bride born in: T. Lok / Groom's year of wed: 1800 / Bride's year of wed: 1851", '   ', '', '    LDS 642810', '    ', '    303-003', '    ', '', '']

