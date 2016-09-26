import os ,sys

def merge_execute(path):
	path_AllOutput = path+"\\RebotAllFileOutput"
	os.system("del /S /Q "+path_AllOutput)
	os.system("mkdir "+path_AllOutput)
	dirs = os.listdir( path )
	#print dirs
	for file in dirs:
		Menu = file.split("Output")
		print Menu
		if Menu[0] == "" :
			print Menu[0]
			print Menu[1]
			path_file_each_output = path+"\\"+file+"\\output"+Menu[1]+"*.xml"
			#print path_file_each_output
			command = "copy " + path_file_each_output + " " + path_AllOutput
			os.system(command)
			#rename = "rename " + path_AllOutput + "\\output.xml output" + file + ".xml"
			#print rename
			#os.system(rename)
	rebot = "rebot --outputdir " + path + "\RebotAllFileOutput -N AllOutput -o outputAll.xml " + path + "\RebotAllFileOutput\output*.xml"
	os.system(rebot)
	
if __name__ == "__main__":
	print "[0] => " + sys.argv[0]
	print "[1] => " + sys.argv[1]
	merge_execute(sys.argv[1])