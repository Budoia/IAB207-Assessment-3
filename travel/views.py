from flask import Blueprint, request, session, render_template, url_for
from .models import Destination


#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = Destination.query.all()
    return render_template("index.html", destinations=destinations)

@mainbp.route('/search')
def saerch():
    if request.args['search']:
        dest = '%' + request.args['search'] + '%'
        destinations = Destination.query.filter(Destination.name.like(dest)).all()
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))