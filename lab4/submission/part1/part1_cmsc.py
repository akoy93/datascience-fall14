from wrangler import dw
import sys

if(len(sys.argv) < 3):
    sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on newline  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="\n",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max=0,
               positions=None,
               quote_character=None))

# Extract from data on 'CMSC any number '
w.add(dw.Extract(column=["data"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="CMSC\\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Cut from data on 'CMSC any number '
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="CMSC\\d+",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Fill extract  with values from above
w.add(dw.Fill(column=["extract"],
              table=0,
              status="active",
              drop=False,
              direction="down",
              method="copy",
              row=None))

# Delete  rows where data is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="data",
                value=None,
                op_str="is null")])))

# Extract from data on '{begin} any number {end}'
w.add(dw.Extract(column=["data"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="^\\d+$",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Fill extract1  with values from above
w.add(dw.Fill(column=["extract1"],
              table=0,
              status="active",
              drop=False,
              direction="down",
              method="copy",
              row=None))

# Cut from data on '{begin} any number {end}'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="^\\d+$",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Wrap  rows where data is null
w.add(dw.Wrap(column=[],
              table=0,
              status="active",
              drop=False,
              row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="data",
                value=None,
                op_str="is null")])))

# Drop wrap
w.add(dw.Drop(column=["wrap"],
              table=0,
              status="active",
              drop=True))

# Drop wrap13
w.add(dw.Drop(column=["wrap13"],
              table=0,
              status="active",
              drop=True))

# Drop wrap14
w.add(dw.Drop(column=["wrap14"],
              table=0,
              status="active",
              drop=True))

# Drop wrap11
w.add(dw.Drop(column=["wrap11"],
              table=0,
              status="active",
              drop=True))

# Drop wrap10
w.add(dw.Drop(column=["wrap10"],
              table=0,
              status="active",
              drop=True))

# Drop wrap8
w.add(dw.Drop(column=["wrap8"],
              table=0,
              status="active",
              drop=True))

# Drop wrap7
w.add(dw.Drop(column=["wrap7"],
              table=0,
              status="active",
              drop=True))

# Drop wrap5
w.add(dw.Drop(column=["wrap5"],
              table=0,
              status="active",
              drop=True))

# Drop wrap4
w.add(dw.Drop(column=["wrap4"],
              table=0,
              status="active",
              drop=True))

# Set  wrap1  name to  Section No.
w.add(dw.SetName(column=["wrap1"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Section No."],
                 header_row=None))

# Set  wrap2  name to  Course No.
w.add(dw.SetName(column=["wrap2"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Course No."],
                 header_row=None))

# Set  wrap3  name to  Instructor
w.add(dw.SetName(column=["wrap3"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Instructor"],
                 header_row=None))

# Extract from wrap6 on 'Total:  any number '
w.add(dw.Extract(column=["wrap6"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="Total: \\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Extract from wrap6 on 'Open:  any number '
w.add(dw.Extract(column=["wrap6"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="Open: \\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Extract from wrap6 on 'Waitlist:  any number '
w.add(dw.Extract(column=["wrap6"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="Waitlist: \\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop wrap6
w.add(dw.Drop(column=["wrap6"],
              table=0,
              status="active",
              drop=True))

# Extract from extract3 on ' any number '
w.add(dw.Extract(column=["extract3"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="\\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract3
w.add(dw.Drop(column=["extract3"],
              table=0,
              status="active",
              drop=True))

# Set  extract4  name to  Waitlist
w.add(dw.SetName(column=["extract4"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Waitlist"],
                 header_row=None))

# Extract from extract2 on ' any number '
w.add(dw.Extract(column=["extract2"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="\\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract2
w.add(dw.Drop(column=["extract2"],
              table=0,
              status="active",
              drop=True))

# Set  extract5  name to  Open
w.add(dw.SetName(column=["extract5"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Open"],
                 header_row=None))

# Extract from extract on ' any number '
w.add(dw.Extract(column=["extract"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="\\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Drop extract
w.add(dw.Drop(column=["extract"],
              table=0,
              status="active",
              drop=True))

# Set  extract6  name to  Seats
w.add(dw.SetName(column=["extract6"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Seats"],
                 header_row=None))

# Extract from wrap12 on ' any uppercase word '
w.add(dw.Extract(column=["wrap12"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[A-Z]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Extract from wrap12 on ' any number '
w.add(dw.Extract(column=["wrap12"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="\\d+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Set  extract7  name to  Room No.
w.add(dw.SetName(column=["extract7"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Room No."],
                 header_row=None))

# Set  extract  name to  Bldg.
w.add(dw.SetName(column=["extract"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Bldg."],
                 header_row=None))

# Drop wrap12
w.add(dw.Drop(column=["wrap12"],
              table=0,
              status="active",
              drop=True))

# Extract from wrap9 after ' any word  '
w.add(dw.Extract(column=["wrap9"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".*",
                 before=None,
                 after="[a-zA-Z]+ ",
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Extract from wrap9 on ' any word '
w.add(dw.Extract(column=["wrap9"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on="[a-zA-Z]+",
                 before=None,
                 after=None,
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Set  extract8  name to  Days
w.add(dw.SetName(column=["extract8"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Days"],
                 header_row=None))

# Set  extract  name to  Time
w.add(dw.SetName(column=["extract"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Time"],
                 header_row=None))

# Drop wrap9
w.add(dw.Drop(column=["wrap9"],
              table=0,
              status="active",
              drop=True))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])

