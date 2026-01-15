from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import EditProfileForm, SettingsForm
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.profile import profile


@profile.route('/my-profile')
@login_required
def my_profile():
    return render_template('profile/my_profile.html', user=current_user)


@profile.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        current_user.profile.bio = form.bio.data
        current_user.profile.current_role = form.current_role.data
        current_user.profile.experience_level = form.experience_level.data
        current_user.profile.learning_goals = form.learning_goals.data
        current_user.profile.can_teach = form.can_teach.data
        current_user.profile.collaboration_interest = form.collaboration_interest.data
        current_user.profile.github_url = form.github_url.data
        current_user.profile.portfolio_url = form.portfolio_url.data
        current_user.profile.linkedin_url = form.linkedin_url.data
        
        # Update location
        if form.city.data:
            current_user.city = form.city.data
        if form.state.data:
            current_user.state = form.state.data
        if form.country.data:
            current_user.country = form.country.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.my_profile'))
    
    # Pre-populate form
    form.bio.data = current_user.profile.bio
    form.current_role.data = current_user.profile.current_role
    form.experience_level.data = current_user.profile.experience_level
    form.learning_goals.data = current_user.profile.learning_goals
    form.can_teach.data = current_user.profile.can_teach
    form.collaboration_interest.data = current_user.profile.collaboration_interest
    form.github_url.data = current_user.profile.github_url
    form.portfolio_url.data = current_user.profile.portfolio_url
    form.linkedin_url.data = current_user.profile.linkedin_url
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.country.data = current_user.country
    
    return render_template('profile/edit_profile.html', form=form)


@profile.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    
    if form.validate_on_submit():
        current_user.profile.show_age = form.show_age.data
        current_user.profile.show_location = form.show_location.data
        current_user.profile.show_online_status = form.show_online_status.data
        current_user.profile.profile_visibility = form.profile_visibility.data
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('profile.settings'))
    
    # Pre-populate form
    form.show_age.data = current_user.profile.show_age
    form.show_location.data = current_user.profile.show_location
    form.show_online_status.data = current_user.profile.show_online_status
    form.profile_visibility.data = current_user.profile.profile_visibility
    
    return render_template('profile/settings.html', form=form)


@profile.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    from flask import current_app
    
    if 'photo' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('profile.my_profile'))
    
    file = request.files['photo']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('profile.my_profile'))
    
    if file:
        filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}_{file.filename}")
        
        # Create upload directory if it doesn't exist
        upload_dir = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        current_user.profile.profile_photo = filename
        db.session.commit()
        
        flash('Profile photo updated!', 'success')
    
    return redirect(url_for('profile.my_profile'))


@profile.route('/blocked-users')
@login_required
def blocked_users():
    blocked = current_user.blocked.all()
    return render_template('profile/blocked_users.html', blocked_users=blocked)


@profile.route('/unblock/<int:user_id>', methods=['POST'])
@login_required
def unblock_user(user_id):
    from app.models import User
    user = User.query.get_or_404(user_id)
    
    if current_user.has_blocked(user):
        current_user.blocked.remove(user)
        db.session.commit()
        flash(f'You have unblocked {user.username}.', 'success')
    
    return redirect(url_for('profile.blocked_users'))


@profile.route('/deactivate-account', methods=['POST'])
@login_required
def deactivate_account():
    current_user.is_active = False
    db.session.commit()
    
    from flask_login import logout_user
    logout_user()
    
    flash('Your account has been deactivated.', 'info')
    return redirect(url_for('main.index'))
