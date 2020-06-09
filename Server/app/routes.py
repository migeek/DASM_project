from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, connections, files
from app.forms import LoginForm, RegistrationForm, BoxRegistrationForm, \
    BoxDeletionForm
from app.models import User, Box
from app.connections import update_contacts, sid_list
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    boxes = Box.query.filter_by(user_id=current_user.id)
    return render_template('index.html', boxes=boxes)


@app.route('/<uid>/box/<bid>')
@login_required
def box(uid, bid):
    bx = Box.query.get(bid)
    if int(current_user.id) != int(uid):
        flash('You are not authoized to configure this box')
        return redirect(url_for('index'))

    contacts = [boxes for boxes in Box.query.filter_by(user_id=current_user.id)
                if int(boxes.bid) != int(bid)]
    print(contacts)

    return render_template('box.html', contacts=contacts, box=bx)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/registerbox', methods=['GET', 'POST'])
@login_required
def registerbox():
    if len(list(Box.query.filter_by(user_id=current_user.id))) >= 5:
        flash('Only five devices can be registered to a family!')
        return redirect(url_for('index'))
    form = BoxRegistrationForm()
    if form.validate_on_submit():
        if Box.query.get(form.bid.data) is not None:
            flash("This box is already registered!")
            return redirect(url_for('index'))
        if int(form.bid.data) not in sid_list.keys():
            flash("This box is not on or does not exist!")
            return redirect(url_for('index'))
        bx = Box(bid=form.bid.data, owner=form.owner.data,
                 user_id=current_user.id)
        db.session.add(bx)
        db.session.commit()
        for b in Box.query.filter_by(user_id=bx.user_id):
            update_contacts(b, sid_list[b.bid])
        flash('Congratulations, you have now registered {}\'s device!'.format(
            form.owner.data))
        return redirect(url_for('index'))
    return render_template('registerbox.html', title='Register Box', form=form)


@app.route('/deletebox', methods=['GET', 'POST'])
@login_required
def deletebox():
    form = BoxDeletionForm()
    boxes = Box.query.filter_by(user_id=current_user.id).all()
    form.to_delete.choices = [(bx.bid, bx.owner) for bx in boxes]
    if form.validate_on_submit():
        bx = Box.query.filter_by(bid=form.to_delete.data).first()
        if bx is None:
            flash('Box does not exist!')
            return redirect(url_for('index'))
        db.session.delete(bx)
        db.session.commit()
        flash('{}\'s box has been removed'.format(bx.owner))
        for b in Box.query.filter_by(user_id=bx.user_id):
            update_contacts(b, sid_list[b.bid])
        return redirect(url_for('index'))
    return render_template('deletebox.html', title='Delete Box', form=form)


# HTTP stuff
@app.route('/api/audio', methods=['GET', 'POST'])
def get_audio():
    if request.method == 'POST':
        message = request.files['messageFile']
        name = message.filename
        data = request.form.to_dict()

        print(
            'received message name: {} from sender ID {} to destination {}'.format(
                name, data['sendID'],
                data['destID']))
        message.save('audio/{}'.format(message.filename))
        files[message.filename] = message
        print('audio file received')
        connections.send_audio(data)
    return 'OK'


@app.route('/api/audio-<send_id>-<file_num>.mp3', methods=['GET'])
def send_audio(send_id, file_num):
    print('sending audio to dest...')
    f_name = 'audio-' + str(send_id) + '-' + str(file_num) + '.mp3'
    file = open('audio/{}'.format(f_name), 'rb').read()
    return file
