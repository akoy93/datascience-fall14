cat cmsc.txt | grep -v '^$' | sed 's/^Seats (Total: \([0-9]*\), Open: \([0-9]*\), Waitlist: \([0-9]*\).*/\1,\2,\3/' | sed 's/^\([MWFTuh]*\) \(.*m\)/\1,\2/' | sed 's/\([A-Z]*\)  \([0-9]*\)/\1,\2/' | awk '/^CMSC[0-9]+$/ {print course; course = $0}
                                  /^[0-9]+$/ {print combined; combined = $0} 
                                  !/^[0-9]+$|^CMSC[0-9]+$/ {combined = combined","$0}
                                  END {print combined}' | grep -v '^$' | awk '/^CMSC[0-9]+$/ {course = $0} !/^CMSC[0-9]+$/ {print course","$0}'