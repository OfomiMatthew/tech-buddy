from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Profile, Like, Match, Message, Notification, Report
from app.forms import MessageForm, SearchForm, ReportForm
from datetime import datetime
from sqlalchemy import and_, or_
from app.main import main
import os
from werkzeug.utils import secure_filename
from flask import current_app


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.discover'))
    return render_template('index.html')


@main.route('/conversations')
@login_required
def conversations():
    # Get all matches with their last messages
    matches = Match.query.filter(
        or_(Match.user1_id == current_user.id, Match.user2_id == current_user.id)
    ).order_by(Match.matched_at.desc()).all()
    
    conversations = []
    for match in matches:
        other_user = match.user2 if match.user1_id == current_user.id else match.user1
        
        # Get last message
        last_message = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_user.id),
                and_(Message.sender_id == other_user.id, Message.receiver_id == current_user.id)
            ),
            Message.is_deleted == False
        ).order_by(Message.sent_at.desc()).first()
        
        # Get unread count
        unread_count = Message.query.filter_by(
            sender_id=other_user.id,
            receiver_id=current_user.id,
            is_read=False,
            is_deleted=False
        ).count()
        
        conversations.append({
            'user': other_user,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    # Sort by last message timestamp
    conversations.sort(key=lambda x: x['last_message'].sent_at if x['last_message'] else datetime.min, reverse=True)
    
    from datetime import timedelta
    return render_template('main/conversations.html', conversations=conversations, datetime=datetime, timedelta=timedelta)


@main.route('/discover')
@login_required
def discover():
    # Get users that current user hasn't liked/passed and haven't blocked
    blocked_ids = [user.id for user in current_user.blocked.all()]
    blocked_by_ids = [user.id for user in current_user.blocked_by.all()]
    liked_ids = [like.liked_id for like in current_user.sent_likes.all()]
    
    exclude_ids = set([current_user.id] + blocked_ids + blocked_by_ids + liked_ids)
    
    # Get potential matches based on preferences
    query = User.query.filter(
        User.id.notin_(exclude_ids),
        User.is_active == True
    )
    
    # Filter by age range (example: ±10 years)
    if current_user.age:
        age_min = max(18, current_user.age - 10)
        age_max = current_user.age + 10
        # This is a simplified age filter - in production, you'd calculate birth year ranges
    
    users = query.limit(20).all()
    
    # Get match count
    matches_count = Match.query.filter(
        or_(Match.user1_id == current_user.id, Match.user2_id == current_user.id)
    ).count()
    
    return render_template('main/discover.html', users=users, matches_count=matches_count)


@main.route('/like/<int:user_id>', methods=['POST'])
@login_required
def like_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot like yourself'}), 400
    
    # Check if already liked
    if current_user.has_liked(user):
        return jsonify({'error': 'Already liked this user'}), 400
    
    # Create like
    like = Like(liker_id=current_user.id, liked_id=user_id)
    db.session.add(like)
    
    # Check if it's a match
    is_match = False
    if user.has_liked(current_user):
        # Create match
        match = Match(
            user1_id=min(current_user.id, user_id),
            user2_id=max(current_user.id, user_id)
        )
        db.session.add(match)
        is_match = True
        
        # Create notifications for both users
        notif1 = Notification(
            user_id=current_user.id,
            type='new_match',
            content=f'You matched with {user.username}!',
            related_user_id=user_id
        )
        notif2 = Notification(
            user_id=user_id,
            type='new_match',
            content=f'You matched with {current_user.username}!',
            related_user_id=current_user.id
        )
        db.session.add(notif1)
        db.session.add(notif2)
    else:
        # Create like notification for the other user
        notif = Notification(
            user_id=user_id,
            type='new_like',
            content=f'{current_user.username} liked your profile',
            related_user_id=current_user.id
        )
        db.session.add(notif)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_match': is_match,
        'message': "It's a match! 🎉" if is_match else "Like sent!"
    })


@main.route('/pass/<int:user_id>', methods=['POST'])
@login_required
def pass_user(user_id):
    # For now, we'll just create a "pass" like with a flag
    # In a full implementation, you might want a separate Pass model
    return jsonify({'success': True, 'message': 'Passed'})


@main.route('/matches')
@login_required
def matches():
    # Get all matches
    user_matches = Match.query.filter(
        or_(Match.user1_id == current_user.id, Match.user2_id == current_user.id)
    ).order_by(Match.matched_at.desc()).all()
    
    match_users = []
    for match in user_matches:
        other_user = match.get_other_user(current_user.id)
        
        # Get last message
        last_message = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_user.id),
                and_(Message.sender_id == other_user.id, Message.receiver_id == current_user.id)
            )
        ).order_by(Message.sent_at.desc()).first()
        
        # Get unread count
        unread_count = Message.query.filter(
            Message.sender_id == other_user.id,
            Message.receiver_id == current_user.id,
            Message.is_read == False
        ).count()
        
        match_users.append({
            'user': other_user,
            'match': match,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    return render_template('main/matches.html', matches=match_users)


@main.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def messages(user_id):
    other_user = User.query.get_or_404(user_id)
    
    # Check if they're matched
    if not current_user.has_matched(other_user):
        flash('You can only message users you\'ve matched with.', 'warning')
        return redirect(url_for('main.matches'))
    
    form = MessageForm()
    
    if form.validate_on_submit():
        message_type = 'text'
        file_url = None
        file_name = None
        file_size = None
        content = form.content.data
        
        # Handle file upload
        if form.attachment.data:
            file = form.attachment.data
            filename = secure_filename(file.filename)
            
            # Generate unique filename
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            
            # Determine message type
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                message_type = 'image'
                folder = 'messages/images'
            elif ext in ['mp3', 'wav', 'ogg']:
                message_type = 'voice'
                folder = 'messages/voice'
            elif ext in ['mp4', 'webm']:
                message_type = 'video'
                folder = 'messages/videos'
            else:
                message_type = 'file'
                folder = 'messages/files'
            
            # Create directory if it doesn't exist
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
            os.makedirs(upload_path, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_path, unique_filename)
            file.save(file_path)
            
            file_url = os.path.join(folder, unique_filename).replace('\\', '/')
            file_name = filename
            file_size = os.path.getsize(file_path)
        
        # Create message (allow empty content if file is attached)
        if content or file_url:
            # Check if rich text
            is_rich_text = form.is_rich_text.data == 'true'
            
            message = Message(
                sender_id=current_user.id,
                receiver_id=user_id,
                content=content,
                message_type=message_type,
                file_url=file_url,
                file_name=file_name,
                file_size=file_size,
                is_rich_text=is_rich_text
            )
            db.session.add(message)
            
            # Create notification
            notif = Notification(
                user_id=user_id,
                type='new_message',
                content=f'New message from {current_user.username}',
                related_user_id=current_user.id
            )
            db.session.add(notif)
            
            db.session.commit()
        
        return redirect(url_for('main.messages', user_id=user_id))
    
    # Get all messages between users
    messages_list = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.sent_at.asc()).all()
    
    # Mark messages as read
    unread_messages = Message.query.filter(
        Message.sender_id == user_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).all()
    
    for msg in unread_messages:
        msg.is_read = True
        msg.read_at = datetime.utcnow()
    
    if unread_messages:
        db.session.commit()
    
    return render_template('main/messages.html', 
                         other_user=other_user, 
                         messages=messages_list, 
                         form=form)


@main.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if blocked
    if current_user.has_blocked(user) or user.has_blocked(current_user):
        flash('This profile is not available.', 'warning')
        return redirect(url_for('main.discover'))
    
    # Check if matched or if viewing own profile
    can_message = current_user.has_matched(user) if user.id != current_user.id else False
    has_liked = current_user.has_liked(user) if user.id != current_user.id else False
    
    return render_template('main/profile.html', 
                         user=user, 
                         can_message=can_message,
                         has_liked=has_liked)


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    users = []
    
    if request.method == 'POST' or request.args.get('submit'):
        # Get blocked users to exclude
        blocked_ids = [user.id for user in current_user.blocked.all()]
        blocked_by_ids = [user.id for user in current_user.blocked_by.all()]
        exclude_ids = set([current_user.id] + blocked_ids + blocked_by_ids)
        
        query = User.query.filter(
            User.id.notin_(exclude_ids),
            User.is_active == True
        )
        
        # Apply username filter
        if form.username.data:
            query = query.filter(User.username.ilike(f'%{form.username.data}%'))
        
        # Apply city filter
        if form.city.data:
            query = query.filter(User.city.ilike(f'%{form.city.data}%'))
        
        # Join with Profile for profile-specific filters
        needs_profile_join = (form.experience_level.data or 
                            form.current_role.data or 
                            form.collaboration_interest.data)
        
        if needs_profile_join:
            query = query.join(Profile)
        
        # Apply experience level filter
        if form.experience_level.data:
            query = query.filter(Profile.experience_level == form.experience_level.data)
        
        # Apply role filter
        if form.current_role.data:
            query = query.filter(Profile.current_role.ilike(f'%{form.current_role.data}%'))
        
        # Apply collaboration interest filter
        if form.collaboration_interest.data:
            query = query.filter(Profile.collaboration_interest == form.collaboration_interest.data)
        
        # Apply age filters
        if form.age_min.data:
            # Calculate max birth year
            from datetime import date
            today = date.today()
            max_birth_year = today.year - int(form.age_min.data)
            query = query.filter(User.date_of_birth <= date(max_birth_year, 12, 31))
        
        if form.age_max.data:
            # Calculate min birth year
            from datetime import date
            today = date.today()
            min_birth_year = today.year - int(form.age_max.data)
            query = query.filter(User.date_of_birth >= date(min_birth_year, 1, 1))
        
        users = query.limit(100).all()
    
    return render_template('main/search.html', form=form, users=users)


@main.route('/api/message/<int:message_id>/react', methods=['POST'])
@login_required
def react_to_message(message_id):
    """Add or update reaction to a message"""
    message = Message.query.get_or_404(message_id)
    
    # Check if user is part of the conversation
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    reaction = data.get('reaction')
    
    if reaction:
        message.reaction = reaction
    else:
        message.reaction = None
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'reaction': message.reaction
    })


@main.route('/api/message/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Delete a message (soft delete)"""
    message = Message.query.get_or_404(message_id)
    
    # Only sender can delete
    if message.sender_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    message.is_deleted = True
    db.session.commit()
    
    return jsonify({'success': True})


@main.route('/api/typing/<int:user_id>', methods=['POST'])
@login_required
def typing_indicator(user_id):
    """Endpoint for typing indicator (can be expanded with WebSocket)"""
    return jsonify({'success': True, 'user_id': current_user.id})


@main.route('/notifications')
@login_required
def notifications():
    notifs = current_user.notifications.order_by(Notification.created_at.desc()).limit(50).all()
    
    # Mark all as read
    for notif in notifs:
        if not notif.is_read:
            notif.is_read = True
    
    if notifs:
        db.session.commit()
    
    return render_template('main/notifications.html', notifications=notifs)


@main.route('/block/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot block yourself'}), 400
    
    if not current_user.has_blocked(user):
        current_user.blocked.append(user)
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'User blocked'})


@main.route('/report/<int:user_id>', methods=['GET', 'POST'])
@login_required
def report_user(user_id):
    user = User.query.get_or_404(user_id)
    form = ReportForm()
    
    if form.validate_on_submit():
        report = Report(
            reporter_id=current_user.id,
            reported_id=user_id,
            reason=form.reason.data,
            description=form.description.data
        )
        db.session.add(report)
        db.session.commit()
        
        flash('Report submitted. Our team will review it shortly.', 'success')
        return redirect(url_for('main.discover'))
    
    return render_template('main/report.html', user=user, form=form)
