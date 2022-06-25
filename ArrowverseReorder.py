import sys
import os
import json
import requests
import pandas as pd
import glob
import filetype
import shutil

if len(sys.argv) > 2:
	print("Usage: python ArrowverseReorder.py [folder]")
	sys.exit(1)

folder= os.getcwd()
if len(sys.argv) > 1:
	folder= sys.argv[1]

nameDestFolder="reordered"
destFolder= os.path.join(folder,nameDestFolder)
if not os.path.exists(destFolder):
	os.makedirs(destFolder)

url= "https://arrowverse.info"
df= pd.read_html(requests.get(url).content)[-1]

del df["Original Air Date"]
del df["Source"]

# from	Series - SXXEXX -Title.*
# to	000 - Series - SXXEXX -Title.*
"""
get all filenames
move them to all directory
rename them by prepending "#" column to old filename getting it from the line Series and Title
"""


# for each file in directory, move to new directory
for file in glob.glob(os.path.join(folder,"*[!"+nameDestFolder+"]","*"), recursive=True):
	# if file is a video
	if (filetype.is_video(file) and len(os.path.basename(file).split(" - "))==3):	# if file is a video and its name is in the format Series - SXXEXX -Title.*
		series= os.path.basename(file).split(" - ")[0]
		episode= os.path.basename(file).split(" - ")[1]
		end= os.path.basename(file).split(" - ")[2]
		
		rowDf= df.loc[(df['Series'] == series) & (df['Episode'] == episode)]
		row= json.loads(rowDf.to_json(orient="records"))[0]
		number= str(row['#']).zfill(3)

		shutil.move(file, os.path.join(destFolder, number+" - "+series+" - "+episode+" - "+end))




