from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from pymongo import Connection

app = Flask(__name__)

connection = Connection()
collection = connection.paint.images

@app.route("/")
@app.route('/<imagename>', methods=['POST', 'GET'])
def mainpage(imagename=None):
    if request.method == 'GET':
        
        if imagename:
            imgname=(imagename,)
            rows = collection.find({'imgname': imagename})
            if rows:
                for row in rows:
                    imgdata = row["imgdata"]
                    #return Response(imgdata)
                    return render_template('paint.html', saved=imgdata)
            else:
                resp = Response("""<html> <script> alert("Image not found");document.location.href="/" </script> </html>""")
                return resp
        else:
            return render_template('paint.html')
	
	
    if request.method == 'POST':
        imgname=request.form['imagename']
        imgdata=request.form['string']
	    
        collection.insert({"imgname":imgname, "imgdata":imgdata})
        resp = Response("saved")
        return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
