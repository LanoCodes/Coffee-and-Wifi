from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
# Generic
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

coffee_rating_choices = ['✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️']
wifi_rating_choices = ['✘', '🛜', '🛜🛜', '🛜🛜🛜', '🛜🛜🛜🛜']
power_socket_amount = ['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌']

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField(label='Cafe Location on Google Maps (URL)', validators=[URL(), DataRequired()])
    time_open = StringField(label='Opening Time e.g.: 8AM', validators=[DataRequired()])
    time_close = StringField(label='Closing Time e.g.: 5:30PM', validators=[ DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=coffee_rating_choices)
    wifi_rating = SelectField(label='Wifi Strength Rating', choices=wifi_rating_choices)
    power_socket_avail = SelectField(label='Power Socker Availability', choices=power_socket_amount)
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        f = open('cafe-data.csv', 'a')
        f.write(f'\n{form.cafe.data},{form.cafe_location.data},{form.time_open.data},{form.time_close.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_socket_avail.data}')

    return render_template(
        'add.html',
        form=form
    )


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template(
        'cafes.html',
        cafes=list_of_rows
    )


if __name__ == '__main__':
    app.run(debug=True)
