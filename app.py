from flask import Flask, render_template
from flask import jsonify

import utils

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/time')
def get_time():
    return utils.get_time()

@app.route('/c1')
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({'confirm': data[0], 'suspect': data[1], 'heal': data[2], 'dead': data[3]})

@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route('/le1')
def get_le1_data():
    data = utils.get_le1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({'day':day,'confirm':confirm,'suspect':suspect,'heal':heal,'dead':dead})

@app.route('/le2')
def get_le2_data():
    data = utils.get_le2_data()
    day,confirm_add,suspect_add = [],[],[]
    for a,b,c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({'day':day,'confirm_add':confirm_add,'suspect_add':suspect_add})

@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({'city': city, 'confirm': confirm})

@app.route('/r2')
def get_r2_data():
    from jieba.analyse import extract_tags
    import string
    data = utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)
        v = i[0][len(k):]
        ks = extract_tags(k)
        for j in ks:
            if not j.isdigit():
                d.append({'name':j,'value':v})
    return jsonify({'kws':d})

if __name__ == '__main__':
    app.run()
