#coding: utf-8
import workflow
import editor
from datetime import datetime, timedelta, date

runningDate = date.today()
format = '%x'
dateText = runningDate.strftime(format)
editor.insert_text(dateText)
