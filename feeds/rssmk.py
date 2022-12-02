import xml.etree.ElementTree as ET
import  urllib.request
import sqlite3
import re

NUMBER_OF_PRINTED = 30
# Create a database in RAM
db = sqlite3.connect(':memory:')
# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('data.db')

# Get a cursor object
cursor = db.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS  data (id INTEGER PRIMARY KEY, pubDate TEXT UNIQUE,
    title TEXT, description TEXT, medialink  TEXT, link TEXT)
''')
db.commit()

startText= '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Sahand Podcast | پادکست سهند</title>
    <itunes:owner>
        <itunes:email>hasanbiabani@gmail.com</itunes:email>
    </itunes:owner>
    <itunes:author>Hasan</itunes:author>
    <description>سعی می‌کنم مطالبی رو که گوش می‌کنم یه جا جمع کنم، محتوا مال خودم نیست. در صورتی که صاحب اثر هستید و از انتشار اثر خود در اینجا ناراضی هستید لطفا اطلاع دهید.</description>
    <itunes:image href="https://bayanbox.ir/preview/5374116589477659827/sahand-logo.jpg"/>
    <language>fa-ir</language>
    <link>https://shemshad.blog.ir</link>
    '''

endText= '''
  </channel>
</rss>
'''

#Close database


url = "https://shemshad.blog.ir/rss/category/%D9%BE%D8%A7%D8%AF%DA%A9%D8%B3%D8%AA/%D8%B3%D9%87%D9%86%D8%AF"

urllib.request.urlretrieve(url, "rss.xml")

mytree = ET.parse('rss.xml')
myroot = mytree.getroot()
channel= myroot.find('channel')
for item in channel.findall('item'):
    description = item.find('description').text
    indexStart = description.find("<p>")
    indexEnd = description.find("</p>")
    newDescription= re.sub("<.*?>", " ", description[indexStart+3:indexEnd])
    indexStart = description.find("src")
    indexEnd = description.find(".mp3")
    medialink ="https:" + (description[indexStart+5:indexEnd]) + ".mp3"
    print (medialink)
    link = item.find('link').text
    title = item.find('title').text
    pubDate = item.find('pubDate').text
    cursor.execute('''INSERT OR REPLACE INTO data(pubDate, title,description, medialink, link)
                VALUES(?,?,?,?,?)''', (pubDate, title,newDescription, medialink, link))

db.commit()

f = open("sahand.rss", "w")
f.write(startText)

try:
    cursor.execute('''SELECT * FROM data''')
except:
	None
else:	
  	for row in cursor:
            newLine = "<item>"+ "\n"
            f.write(newLine)
            newLine = "<title>" + row[2] + "</title>"+ "\n"
            f.write(newLine)
            newLine = "<link>" + row[5] + "</link>"+ "\n"
            f.write(newLine)
            newLine= "<description>" +row[3] + "</description>"+ "\n"
            f.write(newLine)
            newLine = "<pubDate>" + row[1] + "</pubDate>"+ "\n"
            f.write(newLine)
            newLine= "<enclosure url=\"" +row[4] + "\" type=\"audio/mpeg\"/>"+ "\n"
            f.write(newLine)
            newLine = "</item>"+ "\n"
            f.write(newLine)   


f.write(endText)

db.close()
f.close()
