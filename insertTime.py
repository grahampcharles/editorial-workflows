#coding: utf-8
import workflow
import editor
from datetime import datetime, timedelta, date

runningDate = datetime.now()
format = '%H:%M'
dateText = runningDate.strftime(format)
editor.insert_text(dateText)