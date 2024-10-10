# HEIC-to-JPG-converter
This is a HEIC to JPG batch converter using Krita. You can control the quality and avoid online converters.

# What is this?

This is a python script that you can run in Krita to convert multiple HEIC images (all in a folder) to JPG.
It also has the possibility to filter based on creation date. That means, that it stores the latest creation
date from the import, and next time when you use it, it will only convert the ones that were created later.
If you don't want to use this, delete a part of the code, the TODO comments will help with that.

# How to use?

0. Download the script and edit it where you see a TODO then save it
1. Open Krita
2. In Krita open the Scripter (Tools -> Scripts -> Scripter)
3. Open the heicToJpgConverter.py in the Scripter
4. Run the file with the play button

# Additional info

The importDateLog.txt file contains the dates of the of the converted files that has the latest creation date
from each import. After an import it appends the current latest date at the end of the list.
(Note: creation date means here the creation or modification date of the file (which was earlier),
not the creation date of the photo from exif)
