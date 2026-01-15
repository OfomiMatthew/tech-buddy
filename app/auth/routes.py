from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User, Profile
from app.forms import RegistrationForm, LoginForm, ProfileSetupForm
from datetime import datetime
from app.auth import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            looking_for=form.looking_for.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Create empty profile
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        
        flash('Registration successful! Please complete your profile.', 'success')
        login_user(user)
        return redirect(url_for('auth.setup_profile'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=form.remember_me.data)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # Check if profile is complete
            if not user.profile.bio or not user.profile.profile_photo:
                return redirect(url_for('auth.setup_profile'))
            
            return redirect(url_for('main.discover'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/setup-profile', methods=['GET', 'POST'])
def setup_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    form = ProfileSetupForm()
    if form.validate_on_submit():
        profile = current_user.profile
        
        profile.bio = form.bio.data
        profile.current_role = form.current_role.data
        profile.experience_level = form.experience_level.data
        profile.learning_goals = form.learning_goals.data
        profile.can_teach = form.can_teach.data
        profile.collaboration_interest = form.collaboration_interest.data
        profile.github_url = form.github_url.data
        profile.portfolio_url = form.portfolio_url.data
        profile.linkedin_url = form.linkedin_url.data
        
        # Handle profile photo upload
        if form.profile_photo.data:
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            
            file = form.profile_photo.data
            filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}_{file.filename}")
            
            # Create upload directory if it doesn't exist
            upload_dir = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            profile.profile_photo = filename
        
        db.session.commit()
        flash('Profile setup complete! Start discovering tech buddies.', 'success')
        return redirect(url_for('main.discover'))
    
    return render_template('auth/setup_profile.html', form=form)
