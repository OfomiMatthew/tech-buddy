from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config
from app.models import db, User
import os

login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*", manage_session=False)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, manage_session=False)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    
    from app.ai_routes import ai_bp
    app.register_blueprint(ai_bp, url_prefix='/ai')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize tech interests and programming languages if not exists
        from app.models import TechInterest, ProgrammingLanguage
        
        if TechInterest.query.count() == 0:
            interests = [
                TechInterest(name='Web Development', category='Web Dev'),
                TechInterest(name='Mobile Development', category='Mobile'),
                TechInterest(name='Machine Learning', category='AI/ML'),
                TechInterest(name='Data Science', category='Data'),
                TechInterest(name='DevOps', category='DevOps'),
                TechInterest(name='Cloud Computing', category='Cloud'),
                TechInterest(name='Blockchain', category='Blockchain'),
                TechInterest(name='Cybersecurity', category='Security'),
                TechInterest(name='Game Development', category='Gaming'),
                TechInterest(name='UI/UX Design', category='Design'),
            ]
            db.session.add_all(interests)
        
        if ProgrammingLanguage.query.count() == 0:
            languages = [
                ProgrammingLanguage(name='Python'),
                ProgrammingLanguage(name='JavaScript'),
                ProgrammingLanguage(name='TypeScript'),
                ProgrammingLanguage(name='Java'),
                ProgrammingLanguage(name='C++'),
                ProgrammingLanguage(name='C#'),
                ProgrammingLanguage(name='Go'),
                ProgrammingLanguage(name='Rust'),
                ProgrammingLanguage(name='PHP'),
                ProgrammingLanguage(name='Swift'),
                ProgrammingLanguage(name='Kotlin'),
                ProgrammingLanguage(name='Ruby'),
            ]
            db.session.add_all(languages)
        
        db.session.commit()
    
    # Import socket events after app is created
    with app.app_context():
        from app import call_events
    
    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
