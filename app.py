from flask import Flask, render_template, redirect, request, make_response, send_from_directory
from login import LoginForm
from contactme import ContactMeForm
import json
import glob
import os
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'

with open('./data/data.json') as json_file:
    data = json.load(json_file)

@app.route('/')
def base():
    return render_template('home.html', username=request.cookies.get('username'))

@app.route('/admin')
def admin():
    if not request.cookies.get('username') == "jasmine":
        return redirect('/')
    else:
        return render_template('admin.html', username=request.cookies.get('username'))

@app.route("/logout")
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/before_leaving')
def before():
    return render_template('before_leaving.html', username=request.cookies.get('username'))


@app.route('/week_<id>')
def week(id):
    return render_template('week.html', username=request.cookies.get('username'), week_number=int(id), trip=data['trips'][int(id)-1])


@app.route('/contact')
def contact():
    form = ContactMeForm()
    return render_template('contact.html', username=request.cookies.get('username'), form=form)

def get_images(query):
    matches = []
    file_names = [os.path.basename(x) for x in glob.glob('./images/*.*')]

    for query_tag in query.lower().split(" "):
        matches.append(set())
        for file_name in file_names:
            for file_tag in file_name.split(".")[0].replace("_", " ").replace("-", " ").split():
                if query_tag in file_tag:
                    matches[-1].add(file_name)
                    break

    f_set = matches[0]

    for s in matches[1:]:
        f_set = f_set.intersection(s)

    return ["/images/" + x for x in list(f_set)] if f_set else []


@app.route('/search/<query>')
def search(query):
    return render_template('search.html', username=request.cookies.get('username'), query=query, search=get_images(query))

@app.route('/images/<image>')
def images(image):
    return send_from_directory('./images', image)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ""

    if form.is_submitted():
        result = request.form

        if result['email'] == 'jasmine.lebel@live.com' and result['password'] == 'soccer':
            resp = make_response(redirect('/'))
            resp.set_cookie('username', 'jasmine')
            return resp
        else:
            message = "Login Fail"

    return render_template('login.html', form=form, message=message, username=request.cookies.get('username'))

if __name__ == '__main__':
    #app.jinga_env.auto_reload = True
    app.run(debug=True)
