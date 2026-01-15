from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, URL, Optional
from datetime import date
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    looking_for = SelectField('Looking For', choices=[
        ('Learning Partners', 'Learning Partners'),
        ('Mentors', 'Mentors'),
        ('Project Collaborators', 'Project Collaborators'),
        ('Friends', 'Friends'),
        ('All', 'All of the Above')
    ], validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Region', validators=[DataRequired(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    agree_terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')
    
    def validate_date_of_birth(self, date_of_birth):
        today = date.today()
        age = today.year - date_of_birth.data.year - ((today.month, today.day) < (date_of_birth.data.month, date_of_birth.data.day))
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        if age > 100:
            raise ValidationError('Please enter a valid date of birth.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ProfileSetupForm(FlaskForm):
    bio = TextAreaField('About Me', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    current_role = StringField('Current Role', validators=[Length(max=100)])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'Select Level'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
    ])
    learning_goals = TextAreaField('What I Want to Learn', validators=[
        Length(max=500, message='Learning goals must be less than 500 characters')
    ])
    can_teach = TextAreaField('What I Can Teach', validators=[
        Length(max=500, message='Teaching skills must be less than 500 characters')
    ])
    collaboration_interest = SelectField('Collaboration Interest', choices=[
        ('', 'Select Interest'),
        ('Open Source Projects', 'Open Source Projects'),
        ('Study Groups', 'Study Groups'),
        ('Pair Programming', 'Pair Programming'),
        ('Code Reviews', 'Code Reviews'),
        ('Hackathons', 'Hackathons'),
        ('All', 'All of the Above')
    ])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    portfolio_url = StringField('Portfolio URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Complete Profile')


class EditProfileForm(FlaskForm):
    bio = TextAreaField('About Me', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    current_role = StringField('Current Role', validators=[Length(max=100)])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'Select Level'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
    ])
    learning_goals = TextAreaField('What I Want to Learn', validators=[
        Length(max=500, message='Learning goals must be less than 500 characters')
    ])
    can_teach = TextAreaField('What I Can Teach', validators=[
        Length(max=500, message='Teaching skills must be less than 500 characters')
    ])
    collaboration_interest = SelectField('Collaboration Interest', choices=[
        ('', 'Select Interest'),
        ('Open Source Projects', 'Open Source Projects'),
        ('Study Groups', 'Study Groups'),
        ('Pair Programming', 'Pair Programming'),
        ('Code Reviews', 'Code Reviews'),
        ('Hackathons', 'Hackathons'),
        ('All', 'All of the Above')
    ])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    portfolio_url = StringField('Portfolio URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    
    # Location
    city = StringField('City', validators=[Length(max=100)])
    state = StringField('State/Region', validators=[Length(max=100)])
    country = StringField('Country', validators=[Length(max=100)])
    
    submit = SubmitField('Update Profile')


class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[
        Optional(),
        Length(max=5000, message='Message must be less than 5000 characters')
    ])
    message_type = HiddenField('Type', default='text')
    is_rich_text = HiddenField('RichText', default='false')
    attachment = FileField('Attachment', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'webm', 'mp3', 'wav', 'ogg', 'pdf', 'doc', 'docx', 'txt', 'zip'], 
                   'Invalid file type!')
    ])
    submit = SubmitField('Send')


class ReportForm(FlaskForm):
    reason = SelectField('Reason', choices=[
        ('fake_profile', 'Fake Profile'),
        ('harassment', 'Harassment'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('scam', 'Scam'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Additional Details', validators=[
        Length(max=500, message='Description must be less than 500 characters')
    ])
    submit = SubmitField('Submit Report')


class SearchForm(FlaskForm):
    username = StringField('Username', validators=[Optional()])
    age_min = SelectField('Min Age', choices=[('', 'Any')] + [(str(i), str(i)) for i in range(18, 101)], validators=[Optional()])
    age_max = SelectField('Max Age', choices=[('', 'Any')] + [(str(i), str(i)) for i in range(18, 101)], validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    current_role = StringField('Role/Title', validators=[Optional()])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'Any Level'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
    ])
    collaboration_interest = SelectField('Collaboration Interest', choices=[
        ('', 'Any'),
        ('Open Source Projects', 'Open Source Projects'),
        ('Study Groups', 'Study Groups'),
        ('Pair Programming', 'Pair Programming'),
        ('Code Reviews', 'Code Reviews'),
        ('Hackathons', 'Hackathons'),
        ('All', 'All of the Above')
    ])
    submit = SubmitField('Search')


class SettingsForm(FlaskForm):
    show_age = BooleanField('Show my age on profile')
    show_location = BooleanField('Show my location')
    show_online_status = BooleanField('Show when I\'m online')
    profile_visibility = SelectField('Profile Visibility', choices=[
        ('public', 'Public - Anyone can see'),
        ('private', 'Private - Only matches can see details')
    ])
    submit = SubmitField('Save Settings')
