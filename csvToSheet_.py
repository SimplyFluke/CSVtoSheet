import os
import csv
import time
import gspread

from gspread_formatting import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))

for file in os.listdir(): #  Find csv file in folder
    if file.endswith(".csv"):
        csvfile = file
        fName = str(file.replace(".csv", ""))

with open(csvfile, 'r') as fp:
    length = len(fp.readlines())

fmt = CellFormat(
    backgroundColor=Color(1, 0, 0)
)

gc = gspread.service_account(filename=r'Json auth file')
sh = gc.create(fName) #  Set name of document
sh.share('email@email.email', perm_type='user', role='writer') #  Share doc to email
worksheet = sh.sheet1

with open(csvfile, 'r', encoding='utf-8-sig') as cFile:
    content = cFile.read()
    gc.import_csv(sh.id, data=content)

activeList = sh.sheet1.get_values(f'B2:B{length}')
cells = set() #  Set for storing 'false' cells

for item in activeList:
    strItem = str(item)
    if strItem == "['FALSE']":
        cells.add(activeList.index(item))
        activeList[activeList.index(item)] = "." #  Change value of item in list to avoid iteration hell

for item in cells: #  Mark 'dead' users in red
    format_cell_range(sh.sheet1, f"A{item+2}:E{item+2}", fmt)

set_column_widths(sh.sheet1,[('A', 60), ('B', 60), ('C', 230), ('D', 66), ('E', 122)]) #  Set width according to TIP-site
