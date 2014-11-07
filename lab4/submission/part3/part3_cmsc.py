import sys
import re

if len(sys.argv) is not 2:
  print "Invalid number of arguments. Usage: 'python part3_cmsc.py cmsc.txt'"

file = open(sys.argv[1], 'r')

current_line = ""

for line in file:
  # current course
  course_match = re.match(r"^(CMSC\d+)$", line)
  section_match = re.match(r"(\d{4})$", line)
  instructor_match = re.match(r"^([a-zA-Z\s:]+)\n$", line)
  seats_match = re.match(r"^Seats.*?(\d+),.*?(\d+),.*?(\d+)", line)
  time_match = re.match(r"^([MWFTuh]+)\s+(.*)$", line)
  building_match = re.match(r"^([A-Z]+)\s+(\d+)$", line)

  if course_match:
    course = course_match.group(1)
  # current section
  elif section_match:
    current_line = course + "," + section_match.group(1) + "," 
  elif instructor_match:
    current_line += instructor_match.group(1).strip() + ","
  elif seats_match:
    current_line += seats_match.group(1) + "," + seats_match.group(2) + "," + seats_match.group(3) + ","
  elif time_match:
    current_line += time_match.group(1) + "," + time_match.group(2) + ","
  elif building_match:
    current_line += building_match.group(1) + "," + building_match.group(2)
    print current_line