from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association table for tech interests
user_interests = db.Table('user_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('tech_interests.id'), primary_key=True)
)

# Association table for programming languages
user_languages = db.Table('user_languages',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('programming_languages.id'), primary_key=True)
)

# Association table for blocked users
blocked_users = db.Table('blocked_users',
    db.Column('blocker_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('blocked_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Account info
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Basic info
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)  # Male, Female, Non-binary, Other
    looking_for = db.Column(db.String(50))  # Friends, Mentors, Learning Partners, All
    
    # Location
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    sent_likes = db.relationship('Like', foreign_keys='Like.liker_id', backref='liker', lazy='dynamic', cascade='all, delete-orphan')
    received_likes = db.relationship('Like', foreign_keys='Like.liked_id', backref='liked', lazy='dynamic', cascade='all, delete-orphan')
    
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic', cascade='all, delete-orphan')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic', cascade='all, delete-orphan')
    
    reports_made = db.relationship('Report', foreign_keys='Report.reporter_id', backref='reporter', lazy='dynamic', cascade='all, delete-orphan')
    reports_received = db.relationship('Report', foreign_keys='Report.reported_id', backref='reported', lazy='dynamic', cascade='all, delete-orphan')
    
    notifications = db.relationship('Notification', foreign_keys='Notification.user_id', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Many-to-many relationships
    interests = db.relationship('TechInterest', secondary=user_interests, backref=db.backref('users', lazy='dynamic'))
    languages = db.relationship('ProgrammingLanguage', secondary=user_languages, backref=db.backref('users', lazy='dynamic'))
    
    blocked = db.relationship('User',
                             secondary=blocked_users,
                             primaryjoin=(blocked_users.c.blocker_id == id),
                             secondaryjoin=(blocked_users.c.blocked_id == id),
                             backref=db.backref('blocked_by', lazy='dynamic'),
                             lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.utcnow().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def has_liked(self, user):
        return self.sent_likes.filter_by(liked_id=user.id).first() is not None
    
    def has_matched(self, user):
        return (self.has_liked(user) and user.has_liked(self))
    
    def has_blocked(self, user):
        return self.blocked.filter(blocked_users.c.blocked_id == user.id).count() > 0
    
    def is_blocked_by(self, user):
        return user.has_blocked(self)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Profile info
    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(255))
    
    # Tech info
    current_role = db.Column(db.String(100))  # Developer, Designer, Data Scientist, etc.
    experience_level = db.Column(db.String(50))  # Beginner, Intermediate, Advanced, Expert
    github_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    
    # Learning & Growth
    learning_goals = db.Column(db.Text)  # What they want to learn
    can_teach = db.Column(db.Text)  # What they can teach others
    collaboration_interest = db.Column(db.String(100))  # Projects, Study Groups, Pair Programming, etc.
    
    # Preferences
    preferred_contact = db.Column(db.String(50))  # Chat, Video Call, In-Person
    availability = db.Column(db.String(50))  # Weekdays, Weekends, Flexible
    
    # Privacy settings
    show_age = db.Column(db.Boolean, default=True)
    show_location = db.Column(db.Boolean, default=True)
    show_online_status = db.Column(db.Boolean, default=True)
    profile_visibility = db.Column(db.String(20), default='public')  # public, private
    
    # Additional photos
    photos = db.relationship('Photo', backref='profile', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profile {self.user_id}>'


class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Photo {self.filename}>'


class TechInterest(db.Model):
    __tablename__ = 'tech_interests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50))  # Web Dev, Mobile, AI/ML, DevOps, etc.
    
    def __repr__(self):
        return f'<TechInterest {self.name}>'


class ProgrammingLanguage(db.Model):
    __tablename__ = 'programming_languages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<ProgrammingLanguage {self.name}>'


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liked_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_super_like = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('liker_id', 'liked_id', name='unique_like'),)
    
    def __repr__(self):
        return f'<Like {self.liker_id} -> {self.liked_id}>'


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    
    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name='unique_match'),)
    
    def get_other_user(self, current_user_id):
        return self.user1 if self.user2_id == current_user_id else self.user2
    
    def __repr__(self):
        return f'<Match {self.user1_id} <-> {self.user2_id}>'


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Nullable for media-only messages
    message_type = db.Column(db.String(20), default='text')  # text, voice, image, file
    file_url = db.Column(db.String(255), nullable=True)  # Path to uploaded file
    file_name = db.Column(db.String(255), nullable=True)  # Original filename
    file_size = db.Column(db.Integer, nullable=True)  # File size in bytes
    duration = db.Column(db.Integer, nullable=True)  # Duration in seconds for voice notes
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    reaction = db.Column(db.String(10), nullable=True)  # emoji reactions
    is_deleted = db.Column(db.Boolean, default=False)
    is_rich_text = db.Column(db.Boolean, default=False)  # Rich text formatting
    
    def __repr__(self):
        return f'<Message {self.sender_id} -> {self.receiver_id}>'


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # new_match, new_message, new_like, profile_view
    content = db.Column(db.String(255), nullable=False)
    related_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    related_user = db.relationship('User', foreign_keys=[related_user_id])
    
    def __repr__(self):
        return f'<Notification {self.type} for {self.user_id}>'


class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.String(100), nullable=False)  # fake_profile, harassment, inappropriate_content, scam
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Report {self.reporter_id} -> {self.reported_id}>'

# AI-powered feature models

class CompatibilityAnalysis(db.Model):
    """Store AI-generated compatibility analysis between users"""
    __tablename__ = 'compatibility_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    compatibility_score = db.Column(db.Integer)  # 0-100
    strengths = db.Column(db.Text)  # JSON array of strengths
    learning_opportunities = db.Column(db.Text)
    conversation_topics = db.Column(db.Text)  # JSON array
    overall_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    
    def __repr__(self):
        return f'<CompatibilityAnalysis {self.user1_id} <-> {self.user2_id}: {self.compatibility_score}%>'


class AIConversationStarter(db.Model):
    """Store AI-generated conversation starters"""
    __tablename__ = 'ai_conversation_starters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    starters = db.Column(db.Text, nullable=False)  # JSON array of starters
    was_used = db.Column(db.Boolean, default=False)
    used_starter = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    match = db.relationship('User', foreign_keys=[match_id])
    
    def __repr__(self):
        return f'<AIConversationStarter for {self.user_id} -> {self.match_id}>'


class DateIdea(db.Model):
    """Store AI-generated date ideas for matched pairs"""
    __tablename__ = 'date_ideas'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ideas = db.Column(db.Text, nullable=False)  # JSON array of ideas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    
    def __repr__(self):
        return f'<DateIdea for {self.user1_id} & {self.user2_id}>'


class ContentModeration(db.Model):
    """Log AI content moderation results"""
    __tablename__ = 'content_moderations'
    
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(50), nullable=False)  # message, bio, profile
    content_id = db.Column(db.Integer)  # ID of the message or profile
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_safe = db.Column(db.Boolean, nullable=False)
    risk_level = db.Column(db.String(20))  # low, medium, high
    issues = db.Column(db.Text)  # JSON array of issues
    suggested_action = db.Column(db.String(50))  # allow, warn, block
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='content_moderations')
    
    def __repr__(self):
        return f'<ContentModeration {self.content_type} {self.risk_level}>'


class ProfileInsight(db.Model):
    """Store AI-generated profile insights and recommendations"""
    __tablename__ = 'profile_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_score = db.Column(db.Integer)  # 0-100
    insights = db.Column(db.Text, nullable=False)  # Full AI analysis
    strengths = db.Column(db.Text)  # JSON array
    improvements = db.Column(db.Text)  # JSON array
    tips = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='profile_insights')
    
    def __repr__(self):
        return f'<ProfileInsight for {self.user_id}: Score {self.profile_score}>'