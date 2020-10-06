from flask import Blueprint, request, session, redirect, url_for, render_template
from flask_login import login_required, current_user
from .models import Destination,Comment
from .forms import DestinationForm, CommentForm
from . import db
from werkzeug.utils import secure_file



bp = Blueprint('destination', __name__, url_prefix='/destinations')

@bp.route('/<id>')
def show(id):
    destination = Destination.query.filter_by(id=id).first()
    cform = CommentForm()
    return render_template("destinations/show.html", destination=destination, form=cform)


def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)

  upload_path = os.path.join(
    BASE_PATH, 'static/images', secure_filename(filename))
    db_upload_path = 'static/images' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    print('Method type: ', request.method)
    form = DestinationForm()
    
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        destination = Destination(name=form.name.data,
                                description=form.description.data,
                                image=db_file_path,
                                currency=form.currency.data)
        db.session.add(destination)
        db.session.commit()  
        print('Successfully created new travel destination', 'success')
        return redirect(url_for('destination.create'))

    return render_template("destinations/create.html", form=form)

@bp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):  
  #here the form is created 
  form = CommentForm()
  destination_obj = Destination.query.filter_by(id=id).first()
  if form.validate_on_submit():
    comment = Comment(text=form.text.data,
    destination=destination_obj, user = current_user)
    db.session.add(comment)
    db.session.commit()
    print("Comment posted by the user:", form.text.data)
  
  return redirect(url_for('destination.show', id=id))


##def get_destination():
    
##    b_desc= """Brazil is considered an advanced emerging economy.
##    It has the ninth largest GDP in the world by nominal, and eight by PPP measures. 
##    It is one of the world\'s major breadbaskets, being the largest producer of coffee for the last 150 years."""
    # an image location
##    image_loc='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFyC8pBJI2AAHLpAVih41_yWx2xxLleTtdshAdk1HOZQd9ZM8-Ag'
##    destination = Destination('Brazil',b_desc,image_loc,'10 R$')
    # a comment
##    comment = Comment("User1", "Visited during the olympics, was great",'2019-11-12 11:00:00')
##    destination.set_comments(comment)
##    comment2 = Comment("User B", "Cool stuff",'2019-11-12 11:00:01')
##    destination.set_comments(comment2)
##    return destination