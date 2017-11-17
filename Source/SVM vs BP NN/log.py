from datetime import datetime

now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
file_name = "log_{}.txt".format()
header_str = file_name