import os
import exifread

# include trailing slash for directory.
# windows directories are easiest to read with forward slashes.
# like: 'C:/folder/subfolder/'

directory = 'IMAGE DIRECTORY HERE'
extension = '.ext'

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
