#coding: utf-8
import workflow
import ui
import editor
import dialogs
from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta

class Month:
	runningDate = date.today()
	
	def changeMonth(self, sender):
		if sender.name == 'next':
			self.runningDate = self.runningDate + relativedelta(months = 1)
		elif sender.name == 'previous':
			self.runningDate = self.runningDate - relativedelta(months = 1)
		elif sender.name == 'monthButton':
			self.runningDate = date.today()
		configure(self.runningDate)

class InsertionDelegate:
	def tableview_did_select(self, tableview, section, row):
  		cell = tableview.data_source.tableview_cell_for_row(tableview, section, row)
  		dateText = cell.content_view.subviews[0].text
  		editor.insert_text(dateText)
  		setInsertionVisible(False, True)
   	
class InsertionSource:
	selectedDate = date.today()
	
	formats = [
	('Short', '%x'),
	('Medium', '%a, %x'),
	('Long', '%A, %x'),
	('ISO', '%Y-%m-%d'),
	('One True Format', '%d/%m/%Y'),
	('Short Weekday', '%a'),
	('Weekday', '%A')
]
	
  	def tableview_number_of_rows(self, tableview, section):
  		return 7

 	def tableview_cell_for_row(self, tableview, section, row):
  		cell = ui.TableViewCell()
  		
  		dateText = ui.Label()
  		dateText.frame = cell.content_view.bounds
  		dateText.alignment = ui.ALIGN_RIGHT
  		cell.content_view.add_subview(dateText)
  		
  		def setText(name, format):
  			dateText.text = self.selectedDate.strftime(format)
  			cell.text_label.text = name
  		
  		setText(*self.formats[row])
  	 		
	   	return cell

 	def tableview_can_delete(self, tableview, section, row):
   		return False

	def tableview_can_move(self, tableview, section, row):
  		return False

v = ui.load_view()
d = v['daysView']
insertion = v['insertionView']
Date = Month()

def configure(curDate):
	v['monthButton'].title = curDate.strftime('%B %Y')
	if (curDate.month == date.today().month) and (curDate.year == date.today().year):
		today = curDate.day
	else:
		today = -1
	curRange = monthrange(curDate.year, curDate.month)
	prevMonth = curDate - relativedelta(months = 1)
	prevRange = monthrange(prevMonth.year, prevMonth.month)
	fill(prevRange[1] - curRange[0], today, curRange[0]+1, curRange[1])

def fill(firstSunday, today, firstDay, numDays):
	for i, b in enumerate(d.subviews[:firstDay]):
		b.title = str(firstSunday+i)
		b.tint_color = (0.7, 0.7, 0.9, 0.8)
	for day, index in enumerate(range(firstDay, firstDay+numDays)):
		btn = d.subviews[index]
		btn.title = str(day+1)
		btn.tint_color = 0
		if today == day+1:
			btn.tint_color = (0.1, 0.1, 1, 1)
			#btn.background_color = (149.0/255, 149.0/255, 227.0/255, 0.1)
		else:
			btn.background_color = 'transparent'
	for index, btn in enumerate(d.subviews[firstDay+numDays:]):
		btn.title = str(index+1)
		btn.tint_color = (0.7, 0.7, 0.9, 0.8)
		
def setInsertionVisible(visible = True, animated = True):
	insertion.reload()
	insertion.touch_enabled = visible
	def animation():
		insertion.alpha = 1 if visible else 0 # fade out
	ui.animate(animation, 0.3 if animated else 0)
	
	v['previous'].enabled = not visible
	v['next'].enabled = not visible
	v['monthButton'].enabled = not visible
	v['removeInsertion'].hidden = not visible
	
def setInsertionDate(sender):
	day = int(sender.title)
	before, days = monthrange(Date.runningDate.year, Date.runningDate.month)
	if d.subviews.index(sender) <= before:
		ndate = Date.runningDate - relativedelta(months = 1)
	elif d.subviews.index(sender) > before + days:
		ndate = Date.runningDate + relativedelta(months = 1)
	else:
		ndate = Date.runningDate
		
	ndate = date(ndate.year, ndate.month, day)
	insertion.data_source.selectedDate = ndate
	setInsertionVisible()

insertion.delegate = InsertionDelegate()
insertion.data_source = InsertionSource()
v['previous'].action = Date.changeMonth
v['next'].action = Date.changeMonth
v['monthButton'].action = Date.changeMonth
v['removeInsertion'].action = (lambda x: setInsertionVisible(False))

for i, btn in enumerate(d.subviews):
	btn.border_width = 0
	btn.corner_radius = 22
	btn.action = setInsertionDate
	#btn.touch_enabled = False

setInsertionVisible(False, False)
v.present('popover', hide_title_bar=True)
configure(Date.runningDate)