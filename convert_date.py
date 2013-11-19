from datetime import datetime, timedelta

MIN = 5
FMT = "%H:%M:%S"

def convert_date(date):
	date = date.split(".")[0]
	date = datetime.strptime(date, FMT)
	delta = timedelta(minutes=MIN)
	return (date - delta).strftime(FMT)

if __name__ == "__main__":
	date = raw_input()
	print convert_date(date)