#!/usr/bin/env python3
"""
This file handles the main functionalities for
the authenticated users
"""


from flask import request, render_template, redirect
from flask import url_for, flash
from flask_login import login_required, current_user
from . import main
from app.models import Athlete, Scout, Message, Notification, User
from app.forms import EditProfileForm
from app.extensions import db
from app.__init__ import media
from app.models import Media


@main.route('/')
def homepage():
    """
    This is the homepage route
    """
    return render_template('homepage.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """
    This is the dashboard route only accessible to users
    who are authenticated.
    It fetches releveant user data, including messages, notifications
    and specific attributes based on the user's role (Athlete or Coach)
    """
    # Fetch user's messages and notifications
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    user = User.query.filter_by(id=current_user.id).first()

    # Check if the user is an Athlete or Coach, and fetch data accordingly
    user_data = {}
    if current_user.athlete:
        user_data = {
                "role": "Athlete",
                "country": current_user.country,
                "state": current_user.state,
                "height": current_user.height,
                "age": current_user.age,
                "position": current_user.athlete.position,
                "skills": current_user.athlete.skills,
                "achievements": current_user.athlete.achievements,
                "bio": current_user.athlete.bio
        }
    elif current_user.scout:
        user_data = {
                "role": "Scout",
                "country": current_user.country,
                "state": current_user.state,
                "height": current_user.height,
                "age": current_user.age,
                "experience_years": current_user.scout.experience_years,
                "credentials": current_user.scout.credentials,
                "bio": current_user.scout.bio
        }
    # Rendering the dashboard template with the fetched data
    return render_template('dashboard.html', user=current_user,
            messages=messages, notifications=notifications,
            user_data=user_data
    )


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    This route allows users to view and update their profile
    information 
    """
    form = EditProfileForm()
    if request.method == 'POST':
        # The user can choose to update their profile information
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.age = form.age.data
            current_user.height = form.height.data
            current_user.country = form.country.data
            current_user.state = form.state.data
            current_user.bio = form.bio.data

            # Update specific fields if user is a Coach or an Athlete
            if current_user.athlete:
                current_user.athlete.position = form.position.data
                current_user.athlete.skills = form.skills.data
                current_user.athlete.achievements = form.achievements.data

            if current_user.scout:
                current_user.scout.experience_years = form.experience_years.data
                current_user.scout.credentials = form.credentials.data

        # saving changes made in the user profile
        db.session.commit()
        flash("Changes in your profile has been update successfully! Taking you back to your dashboard.")
        return redirect(url_for('main.dashboard'))
    # on GET requests, it returns the profile page with the user's current information
    return render_template('edit_profile.html', user=current_user, form=form)


@main.route('/send_message/<int:recipient_id>', methods=['POST'])
@login_required
def send_message(recipient_id):
    # Fetch the receiver from the database
    recipient = User.query.get_or_404(recipient_id)
    content = request.form['message']

    # Create New message
    new_message = Message(
            sender_id=current_user.id,
            receiver_id=recipient.id,
            content=content,
            status=MessageStatus.UNREAD.value,
            timestamp=datetime.utcnow()
    )

    try:
        db.session.add(new_message)
        db.session.commit()
        flash(f"Message sent to {recipient.username}!")

        # Send notification to recipient
        socketio.emit('new_message', {
            'sender': current_user.username,
            'receiver': recipient.username,
            'content': content,
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, namespace='/messages', room=recipient.id)
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('main.profile', username=recipient.username))


@main.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


@main.route('/upload_media', methods=['GET', 'POST'])
@login_required
def upload_media():
    if request.method == 'POST':
        if 'media' not in request.files:
            flash('Please select a media file to upload')
            return redirect(request.url)

        file = request.files['media']
        if file and media.file_allowed(file, file.filename):
            try:
                filename = media.save(file)
                file_url = media.url(filename)

                if current_user.athlete:
                    athlete = current_user.athlete
                    new_media = Media(athlete_id=athlete.id,
                            media_url=file_url,
                            media_type=file.content_type,
                            uploaded_at=db.func.now()
                    )
                elif current_user.scout:
                    scout = current_user.scout
                    new_media = Media(scout_id=scout.id,
                            media_url=file_url,
                            media_type=file.content_type,
                            uploaded_at=db.func.now()
                    )

                db.session.add(new_media)
                db.session.commit()
                flash('Media uploaded successfully!')
                return redirect(url_for('main.profile'))

            except Exception as e:
                flash(f'An error occurred: {str(e)}')
                return redirect(request.url)

        flash('Invalid media file format')
        return redirect(request.url)
    return render_template('upload_media.html')


@main.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'media' not in request.files:
        flash('Please select a profile picture to upload')
        return redirect(url_for('main.profile', username=current_user.username))

    file = request.files['media']
    if file and media.file_allowed(file, file.filename):
        try:
            # Saving the file and get the URL
            filename = media.save(file)
            file_url = media.url(filename)

            # Check if current user is an athlete or scout and save profile picture accordingly
            if current_user.athlete:
                athlete = current_user.athlete
                new_media = Media(
                        athlete_id=athlete.id,
                        media_url=file_url,
                        media_type='profile_image',
                        uploaded_at=db.func.now()
                )
            elif current_user.scout:
                scout = current_user.scout
                new_media = Media(
                        scout_id=scout.id,
                        media_url=file_url,
                        media_type='profile_image',
                        uploaded_at=db.func.now()
                )

            db.session.add(new_media)
            db.session.commit()
            flash('Profile picture uploaded successfully!')
            return redirect(url_for('main.profile', username=current_user.username))

        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            app.logger.error(str(e))
            return redirect(request.url)

    flash('Invalid file format')
    return redirect(request.url)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Querying the Users table in the database and fetching the searched query
            results = db.session.query(User).join(Athlete, isouter=True).join(Scout, isouter=True).filter(
                    (User.username.contains(query)) | 
                    (User.role.contains(query)) | 
                    (User.sport.contains(query)) | 
                    (User.height.contains(query)) |
                    (User.country.contains(query)) | 
                    (User.state.contains(query)) | 
                    (User.age.contains(query)) | 
                    (Athlete.achievements.contains(query)) | 
                    (Athlete.position.contains(query)) | 
                    (Scout.experience_years.contains(query)) | 
                    (Scout.credentials.contains(query))
            ).all()

            if not results:
                flash('No results found matching your query.')
                return render_template('search.html', results=[])
            return render_template('search.html', results=results)

        flash('Please provide a valid search query.')
        return redirect(url_for('main.search'))
    return render_template('search.html', results=[])


@main.route('/profile')
@login_required
def profile():
    user = current_user
    profile_picture = None

    if user.athlete:
        profile_picture = Media.query.filter_by(athlete_id=user.athlete.id, media_type='profile_image').first()
    elif user.scout:
        profile_picture = Media.query.filter_by(scout_id=user.scout.id, media_type='profile_image').first()

    return render_template('profile.html', user=user, profile_picture=profile_picture)
