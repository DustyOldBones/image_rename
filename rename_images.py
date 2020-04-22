import os
import exifread

directory = 'IMAGE DIRECTORY HERE'
extension = '.ext'

def get_formatted_month(date_in):

    month = str

    if date_in[5:7] == "01":
        month = "JAN"
    elif date_in[5:7] == "02":
        month = "FEB"
    elif date_in[5:7] == "03":
        month = "MAR"
    elif date_in[5:7] == "04":
        month = "APR"
    elif date_in[5:7] == "05":
        month = "MAY"
    elif date_in[5:7] == "06":
        month = "JUN"
    elif date_in[5:7] == "07":
        month = "JUL"
    elif date_in[5:7] == "08":
        month = "AUG"
    elif date_in[5:7] == "09":
        month = "SEP"
    elif date_in[5:7] == "10":
        month = "OCT"
    elif date_in[5:7] == "11":
        month = "NOV"
    elif date_in[5:7] == "12":
        month = "DEC"
    
    return month

def get_year(date_in):
    return date_in[0:4]

def get_day(date_in):
    return date_in[8:10]

def get_formatted_time(time_in):
    hour_int = int(time_in[0:2])

    if hour_int < 12:
        return time_in + " AM"
    elif hour_int == 12:
        return time_in + " AM"
    elif hour_int > 12:
        return str(hour_int-12) + time_in[2:8] + " PM"


os.chdir(directory)

dupe_counter = 0
for file in os.listdir(directory):
    # print(file)
    if file.endswith(extension):
        img = open(file,"rb")

        # gets date/time, works
        exifdata = exifread.process_file(img,details=False)
        # format is YYYY:MM:DD HH:MM:SS - indexes 0:18
        #           0123456789 01234567 - split up as below
        date = str(exifdata['EXIF DateTimeOriginal'])[0:10]
        year = date[0:4]
        month_number = date[5:7]
        month_abbrev = get_formatted_month(date)
        day = date[8:10]

        time = str(exifdata['EXIF DateTimeOriginal'])[11:19]
        hour = time[0:2]
        minute = time[3:5]
        second = time[6:8]
        # millisecond
        ms = str(exifdata['EXIF SubSecTimeOriginal'])

        size_in_bytes = os.stat(directory+file).st_size
        size_in_mb = size_in_bytes / 1024 / 1024
        size_in_mb_rounded = round(size_in_mb,2)

        naming_scheme = f"{year}_{month_number}_{day}__{hour}-{minute}-{second}-{ms}__{size_in_bytes}{extension}"

        img.close()

        # renaming.  If all of these criteria are the same and the file already exists, mark it as a dupe and increment the dupe counter.
        # dupe counter quick and dirty way to keep it unique.
        # the odds of a picture taken at the exact same time down to the millisecond with the exact same byte count is likely atronomically low.
        try:
            os.rename(file,naming_scheme)
        except:
            os.rename(file,f"{naming_scheme}__POSSIBLEDUPE_{dupe_counter}.jpg")
            dupe_counter += 1
