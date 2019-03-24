from flask import Flask, render_template, request, redirect, url_for, flash
from assesbot import Assess

app = Flask(__name__)
app.secret_key = "kqeyu3jbkl3ygl73b7b383f2ih732kj.n328p'0;32p"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assess', methods = ['GET','POST'])
def submit_details():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        studentid = request.form.get('studentid')
        r = Assess(username,password,studentid)
        data = r.auto_assesment()
        if data == []:
            flash('There are no outstanding lecturers to be assessed.')
            return redirect(url_for('home'))
        print(data)
        flash('Great! Your fucking Lecturers have been assessed')
        return redirect(url_for('success'))
    return redirect(url_for('home'))

@app.route('/success')
def success():
   return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)