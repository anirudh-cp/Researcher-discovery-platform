from flask import Flask, redirect, url_for, request, render_template

from legacy.main import main_process

app = Flask(__name__)


@app.route('/process/<term>')
def process(term):
    data = main_process(term)
    return render_template('output.html', table_data=data)


@app.route('/query', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        term = request.form['query']
        return redirect(url_for('process', term=term))
    else:
        term = request.args.get('query')
        return redirect(url_for('process', term=term))


@app.route('/')
def index():
    return render_template('home.html')


#if __name__ == '__main__':
#    app.run(debug=True)
