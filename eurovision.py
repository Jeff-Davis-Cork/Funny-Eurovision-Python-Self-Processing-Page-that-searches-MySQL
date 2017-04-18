#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage, escape
import pymysql as db
            
print('Content-Type: text/html')
print()

form_data = FieldStorage()
country = ''
points = ''
performer=''
song = ''
year = ''
result = ''
dropdown = ''

if points =='':
    if country =='':
        result = '<p class="OutlineText">Go ahead, try it!</p>'

try:
    connection = db.connect(# Login)
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""SELECT DISTINCT country FROM winners""")
    dropdown='<select id="country" name="country">'
    #for row in cursor.fetchall():
        #if country not in row['country']:
            #result = '<p class="OutlineText">Use the dropdown menu for countries!!</p>'
    #else:
    
    for row in cursor.fetchall():
        dropdown+='<option class="OutlineText" value=%s>%s  </option>' % (row['country'],row['country'])
    dropdown +='</select>'

except db.Error: 
    result = '<p class="OutlineText">Sorry! We are experiencing problems at the moment. Please call back later.</p>'
            
if len(form_data) != 0:
    try:         
        country = escape(form_data.getfirst('country',''))
        if country =="United":
            country='United Kingdom'
        points = escape(form_data.getfirst('points', ''))
        connection = db.connect('cs1.ucc.ie', 'jd23', 'airaivou', 'csdipact2017_jd23')

        cursor = connection.cursor(db.cursors.DictCursor)

        # cursor.execute("SELECT country FROM winners")
        
        if country != '': 
            if points =='':
                cursor.execute("""SELECT performer, country, song, year, points FROM winners WHERE country = %s """ , (country))
                if cursor.rowcount==0:
                    result = '<p class="OutlineText">No country by that name. Use the dropdown menu for countries!!</p>'
                else:
                    result = """<h1 class="OutlineText" >Your Search is completed !</h1>
                    <p class="OutlineText">
                        Based on your input, your details are as follows:
                   </p>
                   <table class="table" border="1" style="background-color:#3F51B5;">
                       <tr>
                          <th class="OutlineText" colspan="5">Your Eurovision Data:</th>
                      </tr>
                      <tr class="OutlineText">
                        <th>Performer:</th>
                        <th>Country:</th>
                        <th>Song:</th>
                        <th>Year:</th>
                        <th>Points:</th>
                      </tr>"""
                for row in cursor.fetchall():
                    result+='<tr class="OutlineText"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row['performer'], row['country'],row['song'],row['year'],row['points'])
                result +='</table>'
            else:
                cursor.execute("""SELECT performer, country, song, year, points FROM winners WHERE country=%s AND points>=%s """ , (country,points))
                if cursor.rowcount==0:
                    result = '<p class="OutlineText">No country by that name. Use the dropdown menu for countries!!</p>'
                else:
                    result = """<h1 class="OutlineText">Your Search is completed !</h1>
                    <p class="OutlineText">
                        Based on your input, your details are as follows:
                   </p>
                   <table class="table" border="1" style="background-color:#3F51B5;">
                       <tr>
                          <th class="OutlineText" colspan="5">Your Eurovision Data:</th>
                      </tr>
                      <tr class="OutlineText">
                        <th>Performer:</th>
                        <th>Country:</th>
                        <th>Song:</th>
                        <th>Year:</th>
                        <th>Points:</th>
                      </tr>"""
                for row in cursor.fetchall():
                    result+='<tr class="OutlineText"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row['performer'], row['country'],row['song'],row['year'],row['points'])
                result +='</table>'
        elif points != '':
            try:
                int(points)
                if country =='' :
                    cursor.execute("""SELECT performer, country, song, year, points FROM winners WHERE points>=%s """ , (points))
                    result = """<h1 class="OutlineText">Your Search is completed !</h1>
                        <p class="OutlineText">
                            Based on your input, your details are as follows:
                       </p>
                       <table class="table" border="1" style="background-color:#3F51B5;">
                           <tr>
                              <th style="text-align:center;" class="OutlineText" colspan="5">Your Eurovision Data:</th>
                          </tr>
                          <tr style="text-align:center;" class="OutlineText">
                            <th>Performer:</th>
                            <th>Country:</th>
                            <th>Song:</th>
                            <th>Year:</th>
                            <th>Points:</th>
                          </tr>"""
                    for row in cursor.fetchall():
                        result+='<tr class="OutlineText"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row['performer'], row['country'],row['song'],row['year'],row['points'])
                    result +='</table>'
                else:
                    cursor.execute("""SELECT performer, country, song, year, points FROM winners WHERE country=%s AND points>=%s """ , (country,points))
                    result = """<h1 class="OutlineText">Your Search is completed !</h1>
                        <p class="OutlineText">
                            Based on your input, your details are as follows:
                       </p>
                       <table class="table" border="1" style="background-color:#3F51B5;">
                           <tr>
                              <th class="OutlineText" colspan="5">Your Eurovision Data:</th>
                          </tr>
                          <tr class="OutlineText">
                            <th>Performer:</th>
                            <th>Country:</th>
                            <th>Song:</th>
                            <th>Year:</th>
                            <th>Points:</th>
                          </tr>"""
                    for row in cursor.fetchall():
                        result+='<tr class="OutlineText"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row['performer'], row['country'],row['song'],row['year'],row['points'])
                    result +='</table>'
            except ValueError:
               result = '<p class="OutlineText">Sorry! Your value for points was not a number.</p>' 
        else:
            result = '<p class="OutlineText">Sorry! What you entered for either country or points was not a valid value</p>'
        cursor.close()  
        connection.close()
    except db.Error:
        result = '<p class="OutlineText">Sorry! We are experiencing problems at the moment. Please call back later.</p>' 
      
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Eurovision !</title>
        </head>
    <body style="background: url('https://upload.wikimedia.org/wikipedia/commons/6/68/ESC2014_-_Austria_17_(crop).jpg') no-repeat right top fixed;
                background-color:#3F51B5;
                background-size: 50em;">
        <main>
            <style type="text/css">
		.OutlineText {
		font: Tahoma, Geneva, sans-serif;
		text-align:left;
		margin-left:1em;
		font-size: 24px;
		color: #C5CAE9;
		text-shadow:
		/* Outline */
		-.5px -.5px 0 #303F9F,
		.5px -.5px 0 #303F9F,
		-.5px .5px 0 #303F9F,
		.5px .5px 0 #303F9F,  
		-1px 0 0 #303F9F,
		1px 0 0 #303F9F,
		0 1px 0 #303F9F,
		0 -1px 0 #303F9F; 
		}
	    </style>
	    <style type="text/css">
               .table
               {
              position:relative;
              left: 2em;

               }
            </style>
				
            <h1 class="OutlineText"> Welcome to my Eurovision Page !</h1>
                <p class="OutlineText">You can enter in the name of a country, <br></br>or a minimum amount of points to search my database of winners!</p>
            <form class="OutlineText" action="eurovision.py" method="get">
                <p>
                <label class="OutlineText" for="country">Country:
                %s  
                </label>
                </p>
                <p>
                <label class="OutlineText" for="points">Points: </label>
                <input type="point" name="points" value="%s" id="points" />
                </p>
                <p>
                <input type="submit" value="Go Eurovision!" />
                </p>
            </form>
            %s
            
        </body>
    </html>""" % (dropdown, points, result))
