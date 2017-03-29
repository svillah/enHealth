from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def intro():
    return render_template('index.html')


@app.route('/drug')
def getDrugInfo():
    drugName = request.args.get('keyword')
    return render_template('drugInfo.html', drugName = drugName)



