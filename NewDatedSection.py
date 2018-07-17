#coding: utf-8
import workflow
import editor
from datetime import datetime, timedelta, date

# get and format date
runningDate = date.today()
format = '%x'
dateText = runningDate.strftime(format)

# position cursor
editor.set_selection(0) # move to beginning

# insert text
editor.insert_text('# ')
editor.insert_text(dateText)
editor.insert_text('\n\n\n')

# move back two characters
currentSpot = editor.get_selection()
editor.set_selection(currentSpot[0] - 2)