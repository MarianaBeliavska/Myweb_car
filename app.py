from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, make, model, color, year, price):
        self.make = make
        self.model = model
        self.color = color
        self.year= year
        self.price = price

    def __str__(self):
        return f"{self.make} {self.model} {self.color} {self.year} {self.price}"

# darbas su sql db failu
with app.app_context():
    db.create_all()

    # Patikriname, ar lentelė jau turi įrašų
    if Cars.query.count() == 0:
        # Sukuriame keletą automobilių
        car1 = Cars("Toyota", "Corolla", "Raudona", 2015, 8500)
        car2 = Cars("BMW", "320", "Juoda", 2018, 14500)
        car3 = Cars("Audi", "A4", "Balta", 2020, 17500)
        car4 = Cars("Honda", "Civic", "Mėlyna", 2017, 9200)

        # Pridedame juos prie sesijos
        db.session.add_all([car1, car2, car3, car4])

        # Įrašome į duomenų bazę
        db.session.commit()

@app.route('/')
def home():
    search_text = request.args.get('paieskoslaukelis')
    if search_text:
       all_rows = Cars.query.filter(Cars.make.ilike(search_text + '%')).all()
    else:
        all_rows = Cars.query.all()
    return render_template('index.html', all_rows=all_rows)
@app.route('/automobiliai/<int:car_id>')
def one_car(car_id):
    one_row = Cars.query.get(car_id)
    return render_template('one_car.html', one_row=one_row)

# C - CREATE
@app.route('/automobiliai/naujas', methods=['GET', 'POST'])
def new_employee():
    if request.method == 'GET':
        return render_template('new_car.html')
    elif request.method == 'POST':
        make = request.form.get('makeinputas')
        model = request.form.get('modelinputas')
        color = request.form.get('colorinputas')
        year = request.form.get('yearinputas')
        price = request.form.get('priceinputas')
        if make and model and price:
            new_row = Cars(make, model, color, int(year), int(price))

            db.session.add(new_row)
            db.session.commit()
    return redirect('/')

#D - DELETE

@app.route('/automobiliai/trinti/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    row = Cars.query.get(car_id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('home'))

#U - update
@app.route('/automobiliai/redaguoti/<int:car_id>', methods=['POST', 'GET'])
def update_car(car_id):
    row = Cars.query.get(car_id)
    if not row:
        return "Nuoroda ne egzistuoja"
    if request.method == 'GET':
        return render_template('update_car.html', row=row)

    elif request.method == 'POST':
        make = request.form.get('makeinputas')
        model = request.form.get('modelinputas')
        color = request.form.get('colorinputas')
        year = request.form.get('yearinputas')
        price = request.form.get('priceinputas')
    if make and model and price:
        row.make = make
        row.model = model
        row.color = color
        row.year = int(year)
        row.price = int(price)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()