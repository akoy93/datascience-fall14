cat worldcup.txt | grep -v '^|-\|!\||\d*||\||}' | sed 's/^.*{{fb|\([A-Z]*\).*/\1/' | awk '/^[A-Z]+$/ {country = $0; place = 0} !/^[A-Z]+$/ {place = place + 1} /\|[0-9]+\]\]/ {len = split($0,a,",");
                                                                                          for (i = 1; i <= len; i++) {
                                                                                            print country","a[i]","place}
                                                                                          }' | sed 's/^\([A-Z]*\).*|\([0-9]*\)\]\].*\([1-4]\)$/\1,\2,\3/'