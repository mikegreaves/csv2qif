#!/usr/bin/env python
import csv #csv reading
import argparse #Command line parsing
import sys


headerrows = 1

def date(value):
	if value:
		args.outfile.write('D'+str.strip(value)+'\n')


def security_desc(value):
	if value:
		args.outfile.write('M'+str.strip(value)+'\n')

def amount(value):
	if value:
		args.outfile.write('T'+str.strip(value)+'\n' )


fields = {0 : date,
		1: security_desc,
		10: amount,
}


#Parse input commands
#defines infile and outfile for reading and writing respectively

acct_choices =["Bank","Cash","CCard","Invst"]
parser = argparse.ArgumentParser(description = "Converts Fidelity .csv input files to Quicken .qif format")
parser.add_argument('infile', help = 'Input file name')
parser.add_argument('outfile', nargs='?', type = argparse.FileType('w'), default = sys.stdout)
#parser.add_argument('outfile', help = 'Output file name')
parser.add_argument('-t', required = True,nargs='?', choices=acct_choices, help='Type of account designator.  Valid inputs are: '+','.join(acct_choices))
args = parser.parse_args()

outfile = args.outfile
reader = csv.reader(open(args.infile,"rb"), delimiter=',', lineterminator='\r\n')

valid_rows = []

#Build a list of valid rows
for row in reader:
	if row: #skip empty rows
		valid_rows.append(row)

#Define the account type
args.outfile.write('!Type:'+ args.t+'\n')

#Parse the CSV	
for index,row in enumerate(valid_rows):
	if (index < headerrows):
		#print('header\t:',row)
		continue
	#Format a single row
	for recordindex,value in enumerate(row):
		try:
			fields[recordindex](value)
			
		except KeyError:
			continue #Ignore unused keys
		finally:
			pass
		
	#print the record separator between records
	args.outfile.write('^'+'\n')
 