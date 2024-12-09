"""
Helper function for creating multi-reddits.
Run script and paste the string it outputs into the accompanying Excel file.

Created on Sat Jun 11 09:02:09 2016

@author: wynand
"""

maxCell = int(input("What is the max Cell? "))
column = str(input("What is the column? "))
cellCount = [maxCell]

while maxCell > 0:
    maxCell = maxCell - 1
    cellCount.append(maxCell)

pasteString = "="

for i in cellCount:
    pasteString = pasteString + f'{column}{i}&"+"&'

print(pasteString)
