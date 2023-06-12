from flask import render_template, redirect, url_for
from ..models import Results
import json

def index():
    return render_template('main/index.html')

def prediction():
    return render_template('main/predict.html')

def details(id):
    res = Results.query.filter_by(id=id).first()
    if res:
        res = res.to_dict()
        resultjs = json.loads(res['result'])
        result = {
            'matchWUP': json.loads(resultjs['result']['datamatchWUP']),
            'scoreWUP' :  resultjs['result']['WUP'],
            'matchPATH': json.loads(resultjs['result']['datamatchPATH']),
            'scorePATH' :  resultjs['result']['PATH']
        }
        return render_template(
            'main/results.html', 
            id=id,
            resultScrab=json.loads(resultjs['scrapdata']),
            processData=json.loads(resultjs['process']),
            result = result
        )
    return redirect(url_for('web.prediction'))

def detailSrap(id):
    res = Results.query.filter_by(id=id).first()
    if res:
        res = res.to_dict()
        resultjs = json.loads(res['result'])
        result = {
            'matchWUP': json.loads(resultjs['result']['datamatchWUP']),
            'scoreWUP' :  resultjs['result']['WUP'],
            'matchPATH': json.loads(resultjs['result']['datamatchPATH']),
            'scorePATH' :  resultjs['result']['PATH']
        }
        return render_template(
            'main/resultdetail.html', 
            id=id,
            resultScrab=json.loads(resultjs['scrapdata']),
            processData=json.loads(resultjs['process']),
            result = result
        )
    return redirect(url_for('web.prediction'))