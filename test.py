#test.py
import calendar
from datetime import date

billingPeriod = (date.today(), date(2020,4,calendar.monthrange(2020, 2)[1]))

print(billingPeriod)
print(str(billingPeriod[0]) + "," + str(billingPeriod[1]))