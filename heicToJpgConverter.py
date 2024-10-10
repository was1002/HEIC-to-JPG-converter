from krita import *
import os
import time # TODO: you can delete it if you don't want to use the filtering based on date

# getting the Krita app
app = Krita.instance()

# setting the folder of the HEIC files
# TODO: place the path of the HEIC files here, escape backslashes, don't end the path with a backslash (e.g. "C:\\BadPictures")
folderPath = ""

# setting the target folder for the converted JPG images
# TODO: place the target path here, escape backslashes, DO end it with a backslash (because I was lazy) (e.g. "C:\\GoodPictures\\")
targetPath = ""

# ----------- DATE SECTION ----------- TODO: delete it if you don't want to use the filtering based on date

# getting the date of the last imported picture
# setting the path first
# TODO: place the path of the import date log file here, escape backslashes, don't end the path with a backslash (e.g. "C:\\BoringFiles")
datePath = ""
dateFileName = "importDateLog.txt" # give it a cooler name if you want
dateFileFullPath = datePath + "\\" + dateFileName
# used date format
dateFormat = r"%Y.%m.%d %H:%M:%S" # change the date format to a worse if you dare
# opening the file or creating if it doesn't exists
with open(dateFileFullPath, "a+") as dateFile:
    # moving back the pointer to the beginning of the file to read it entirely
    dateFile.seek(0)
    dateLog = dateFile.readlines()
# if the file isn't empty getting the last date, else setting it to 0
if len(dateLog) > 0:
    # getting and converting the last date to seconds (first making it a time struct by using the format on the last line and removing extra characters)
    lastImportDate = int(time.mktime(time.strptime(dateLog[-1][:-1], dateFormat)))
else:
    lastImportDate = 0
newLastImportDate = lastImportDate

# -------- END OF DATE SECTION --------

# cycling through every file in the folder
for fileName in os.listdir(folderPath):
    # getting the full path of the file
    fullPath = folderPath + "\\" + fileName
    # getting the creation date (not from exif so it's may not be the real, but it's easier) TODO: delete the next 3 lines if you don't want to use the filtering based on date
    CreationDate = int(os.path.getctime(fullPath))
    ModDate = int(os.path.getmtime(fullPath))
    fileCreationDate = CreationDate if CreationDate <= ModDate else ModDate
    # selecting the file if it's in HEIC format (lower makes sure it's not case sensitive)
    # and its creation date is later then the last import date
    if fileName.lower().endswith(".heic") and fileCreationDate > lastImportDate: # TODO: delete the second condition if you don't want to use the filtering based on date
        # changing the name of the target to end with JPG instead of HEIC
        targetName = fileName[:-4] + "jpg"
        #checking if file already exists in target folder
        if os.path.isfile(targetPath + targetName):
            print("Image already converted (" + targetName + ")")
        else:
            # opening the image
            image = app.openDocument(fullPath)
            # checking if it opened successfully
            if image:
                # setting the image as the active document
                app.setActiveDocument(image)
                print(f"Document {image.fileName()} opened successfully!")
            
                # setting the export parameters
                # TODO: change the parameters to match your demands
                jpgExportInfo = InfoObject()
                jpgExportInfo.setProperty("baseline", True)
                jpgExportInfo.setProperty("exif", True)
                jpgExportInfo.setProperty("filters", [False, False])
                jpgExportInfo.setProperty("forceSRGB", False)
                jpgExportInfo.setProperty("iptc", True)
                jpgExportInfo.setProperty("is_sRGB", True)
                jpgExportInfo.setProperty("optimize", True)
                jpgExportInfo.setProperty("progressive", False)
                jpgExportInfo.setProperty("quality", 100)
                jpgExportInfo.setProperty("saveProfile", True)
                jpgExportInfo.setProperty("smoothing", 0)
                jpgExportInfo.setProperty("subsampling", 0)
                jpgExportInfo.setProperty("transparencyFillcolor", [255,255,255])
                jpgExportInfo.setProperty("xmp", True)
            
                # setting batchmode on to avoid dialogs
                image.setBatchmode(True)
                # exporting the image
                exportSuccessful = image.exportImage(targetPath + targetName, jpgExportInfo)
                if exportSuccessful:
                    print(f"Image successfully exported: {targetPath + targetName}")
                    # check if the files creation date is the latest, if yes then store it
                    # TODO: delete this "if" if you don't want to use the filtering based on date
                    if fileCreationDate > newLastImportDate:
                        newLastImportDate = fileCreationDate
                else:
                    print("Export failed.")
            
                image.close()
            else:
                print("Failed to open the document.")

# ----------- DATE SECTION 2 ----------- TODO: delete it if you don't want to use the filtering based on date

# updating the import date log, if necessary
if lastImportDate <= newLastImportDate:
    formattedDate = time.strftime(dateFormat, time.localtime(newLastImportDate))
    with open(dateFileFullPath, "a") as dateFile:
        dateFile.write(formattedDate + "\n")

# -------- END OF DATE SECTION 2 --------

print("Finished converting.")
