from app import app

from flask import redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# app = Flask(__name__)
# app.secret_key = 'super secret keys'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jacquesdutoit/Developer/StockTrack/stocktrack.db'
# app.config['TRACK_MODIFICATIONS'] = False   
# app.permanent_session_lifetime = timedelta(minutes=60)

print(app.config)

db = SQLAlchemy(app)
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial = db.Column(db.String(100))
    problem = db.Column(db.String(100))
    date_booked = db.Column(db.String(100))
    etr = db.Column(db.String(100))
    at_repair_site = db.Column(db.Boolean())

    
    def __init__(self, client, brand, model, serial, problem, date_booked, etr, at_repair_site):
        self.client = client
        self.brand = brand
        self.model = model
        self.serial = serial
        self.problem = problem
        self.date_booked = date_booked
        self.etr = etr
        self.at_repair_site = at_repair_site

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    street = db.Column(db.String(100))
    suburb = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    contact_number = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, company, street, suburb, contact_person, contact_number, email):
        self.company = company
        self.street = street
        self.suburb = suburb
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.email = email

with app.app_context():
    db.create_all()


# this function will translate an object from the STOCK class into JSON format
def r_obj_to_dict(self):
    return {
        # "id": self.id,
        "client": self.client,  
        "brand": self.brand,
        "model": self.model,
        "serial": self.serial,
        "problem": self.problem,
        "date_booked": self.date_booked,
        "etr": self.etr,
        "at_repair_site": self.at_repair_site
    }
def c_obj_to_dict(self):
    return {
        # "id": self.id,
        "company": self.company,
        "street": self.street,
        "suburb": self.suburb,
        "contact_person": self.contact_person,
        "contact_number": self.contact_number,
        "email": self.email,  
    }

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.permanent = True
        if request.form['password'] == app.config['SECURE_PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('repair'))
        else:
            flash('Incorrect Password', category="error")
            return render_template('login.html', error=True)
    else:
        if 'logged_in' in session:
            return redirect(url_for('repair'))
        return render_template('login.html')

@app.route('/repair', methods=['GET', 'POST'])
def repair():
    if request.method == 'POST':
        if request.form['inlineRadioOptions'] == '1':
            x = True
        elif request.form['inlineRadioOptions'] == '0':
            x = False
        item = Item(request.form['client'], request.form['brand'], request.form['model'], request.form['serial'], request.form['problem'], request.form['date_booked'], request.form['etr'], x)
        db.session.add(item)
        db.session.commit()

        #this needs to display properly!!!!!!!!!!!!!!!!!!!
        flash('Record was successfully added!', category='success')
        
        return redirect(url_for('repair'))
    else:
        if 'logged_in' in session:
            # print(session['logged_in'])
            q = Client.query.all()
            # print(q)
            return render_template('repair.html' , q=q)
        else:
            return redirect(url_for('login'))
        
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        item = Client(request.form['company'], request.form['street'], request.form['suburb'], request.form['contact_person'], request.form['contact_number'], request.form['email'])
        db.session.add(item)
        db.session.commit()

        #this needs to display properly!!!!!!!!!!!!!!!!!!!
        flash('Record was successfully added!', category='success', )
        
        return redirect(url_for('client'))
    else:
        if 'logged_in' in session:
            # print(session['logged_in'])
            return render_template('client.html')
        else:
            return redirect(url_for('login'))
        
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         return "<h1>Search Results</h1>" 
#     else:
#         if 'logged_in' in session:
#             # print(session['logged_in'])
#             return render_template('search.html')
#         else:
#             return redirect(url_for('login'))
@app.route('/repair/search', methods=['GET', 'POST'])
def repair_search():
    if request.method == 'POST':
        return redirect(url_for('repair_view'))
    else:
        if 'logged_in' in session:
            # print(session['logged_in'])
            q = Item.query.all()
            return render_template('repair_search.html', q=q)
        else:
            return redirect(url_for('login'))
        
@app.route('/repair/view/<int:id>', methods=['GET', 'POST'])
def repair_view(id):
    if request.method == 'GET':
        if 'logged_in' in session:
            row = Item.query.get(id)
            q = Client.query.all()
            # print(row)
            return render_template('repair_view.html', row=row, q=q)
        else:
            return redirect(url_for('login'))
        
    if request.method == 'POST':
        if 'logged_in' in session:
            row = Item.query.filter_by(id=id).first()
            row.client = request.form['client']
            row.brand = request.form['brand']
            row.model = request.form['model']
            row.serial = request.form['serial']
            row.problem = request.form['problem']
            row.date_booked = request.form['date_booked']
            row.etr = request.form['etr']

            if request.form['inlineRadioOptions'] == '1':
                x = True
            elif request.form['inlineRadioOptions'] == '0':
                x = False
            row.at_repair_site = x
            
            db.session.commit()

            #this needs to display properly!!!!!!!!!!!!!!!!!!!
            flash('Record was successfully updated!', category='success')

            return render_template('repair_view.html', row=row)
@app.route('/client/search', methods=['GET', 'POST'])
def client_search():
    if request.method == 'POST':
        return redirect(url_for('client_view'))
    else:
        if 'logged_in' in session:
            # print(session['logged_in'])
             q = Client.query.all()
             return render_template('client_search.html', q=q)
        else:
            return redirect(url_for('login'))
        
@app.route('/client/view/<int:id>', methods=['GET', 'POST'])
def client_view(id):
    if request.method == 'GET':
        if 'logged_in' in session:
            row = Client.query.get(id)
            # print(row)
            return render_template('client_view.html', row=row)
        else:
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'logged_in' in session:
            row = Client.query.filter_by(id=id).first()
            row.company = request.form['company']
            row.street = request.form['street']
            row.suburb = request.form['suburb']
            row.contact_person = request.form['contact_person']
            row.contact_number = request.form['contact_number']
            row.email = request.form['email']
            
            db.session.commit()

            #this needs to display properly!!!!!!!!!!!!!!!!!!!
            flash('Record was successfully updated!', category='success', )

            return render_template('client_view.html', row=row)

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        flash('Logged out successfully!', category="info")
    session.pop('logged_in', None)
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run()