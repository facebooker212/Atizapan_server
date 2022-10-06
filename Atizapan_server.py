from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subnoti')
def subnoti():
    return render_template('noti_submit.html')

@app.route('/subnoti', methods=['POST'])
def postnoti():
    noti = request.form['notis']
    f = open("notis.txt", "w")
    f.write(noti)
    f.close()
    return "notificaciones actualizadas"

@app.route('/notis')
def readnotis():
    f = open("notis.txt", "r")
    n = f.read()
    return n

@app.route('/subcoord')
def subcoord():
    return render_template('coord_submit.html')

@app.route('/subcoord', methods=['POST'])
def postcoord():
    coords = request.form['coords']
    f = open("coords.txt", "r")
    c = f.read()
    f.close()
    if (len(checklen(c)) == 1):
        f = open("coords.txt", "w")
        f.write(coords)
    elif (len(checklen(c)) == 20):
        nc = checklen(c)
        del nc[0]
        del nc[0]
        sc = ", ".join(nc)
        f = open("coords.txt", "w")
        f.write(sc + ", " + coords)
    else:
        f = open("coords.txt", "w")
        f.write(c + ", " + coords)
    f.close()
    return "coordenadas actualizadas"

@app.route('/coords')
def readcoords():
    f = open("coords.txt", "r")
    c = f.read()
    return c

def checklen(s):
    l = s.split(",")
    print(l)
    print(len(l))
    return l

if __name__ == '__main__':
    from waitress import serve
    #app.run(use_reloader=True, port=5000, threaded=True)
    serve(app, host="0.0.0.0", port=5000, url_scheme='https')
