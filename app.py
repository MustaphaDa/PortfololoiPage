from flask import Flask, render_template, redirect, url_for, flash,session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

app = Flask(__name__, template_folder='Templates', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        last_sent_time = session.get('last_sent_time')
        if last_sent_time:
            last_sent_time = datetime.strptime(last_sent_time, '%Y-%m-%d %H:%M:%S')
            if datetime.now() - last_sent_time < timedelta(minutes=30):
                flash('You need to wait 30 minutes before sending another message.', 'danger')
                return redirect(url_for('contact'))

        # Save the current time as the last sent time
        session['last_sent_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about_me')
def about_me():
    return render_template('About_me.html')

@app.route('/education')
def education():
    return render_template('Education.html')

@app.route('/projet')
def projet():
    return render_template('Projet.html')

if __name__ == '__main__':
    print(f"Current working directory: {os.getcwd()}")
    print(f"Template folder: {app.template_folder}")
    app.run(debug=True)