import sys
import re

if len(sys.argv) is not 2:
  print "Invalid number of arguments. Usage: 'python part3_worldcup1.py worldcup.txt'"

file = open(sys.argv[1], 'r')

current_line = ""

for line in file:
  junk_match = re.match(r"^\|-|!|\|\d*\|\||\|\}", line)
  country_match = re.match(r"^.*\{\{fb\|([A-Z]*).*$", line)

  if not junk_match:
    if country_match:
      country = country_match.group(1)
      place = 0
    else:
      place += 1
      for result in line.split(','):
        year_match = re.match(r"^.*?\|(\d{4})\]\]", result)
        if year_match:
          print country + "," + year_match.group(1) + "," + str(place)