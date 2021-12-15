from datetime import datetime
datenow = datetime.now()
date = datenow.date()
p = datenow.strftime("%p")
day = str(date)+p
print(datenow.time())