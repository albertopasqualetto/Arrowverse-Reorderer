import argparse
import sys
import os
from arrowverse_reorderer import reorder

def main() -> int:
	# parse arguments
	parser = argparse.ArgumentParser(description='Order Arrowverse episodes files in air time order.')
	parser.add_argument('-dm', '--dry-run-rename', action="store_true", default=False, help='does not really rename files, just prints them (and then exits, equivalent to "mnamer --test")')
	parser.add_argument('-dr', '--dry-run-reorder', action="store_true", default=False, help='does not really reorder files, just prints them')
	parser.add_argument('-dest', '--destination-path', nargs='?', default="", type=str, help='destination folder')
	parser.add_argument('folders', action="extend", nargs='*', default=[], type=str, metavar='FOLDERS', help='folders to process')
	args= parser.parse_args()

	# if no folders are given, use current directory
	folders= args.folders
	if folders==[]:
		folders.append= os.getcwd()

	# if no destination folder is given, use current directory
	name_dest_folder="reordered"
	if args.destination_path!="":
		name_dest_folder= os.path.basename(args.destination_path)

	# rename files with mnamer
	if not args.dry_run_rename :
		for folder in folders:
			os.system("mnamer -b -r --no-guess --episode-format=\"{series} - S{season:02}E{episode:02} - {title}{extension}\" --ignore=\"(\\\\"+name_dest_folder+"\\\\)|(\/"+name_dest_folder+"\/)\" --test "+folder)
			return 0
	else:
		for folder in folders:
			os.system("mnamer -b -r --no-guess --episode-format=\"{series} - S{season:02}E{episode:02} - {title}{extension}\" --ignore=\"(\\\\"+name_dest_folder+"\\\\)|(\/"+name_dest_folder+"\/)\" "+folder)

	# reorder files
	if destination_path=="":
		destination_path= os.path.join(os.getcwd(),name_dest_folder)
	reorder(folders, name_dest_folder, args.destination_path, args.dry_run_reorder)

	return 0

if __name__ == '__main__':
	sys.exit(main())