# TechBuddy - A Dating Platform for Tech Enthusiasts

A modern dating platform built with Flask, designed specifically for techies who want to connect, learn, and grow together.

## Features

✅ **User Authentication**

- Secure registration and login
- Email validation
- Age verification (18+)
- Password hashing with bcrypt

✅ **Profile Management**

- Detailed tech profiles
- Profile photos
- Tech interests and programming languages
- Learning goals and teaching skills
- GitHub, Portfolio, and LinkedIn integration

✅ **Discovery System**

- Smart user discovery
- Like/Pass functionality
- Match algorithm
- Profile filtering

✅ **Matching & Messaging**

- Match notifications
- Real-time messaging interface
- Rich text messaging with formatting
- Voice notes, images, videos, and file sharing
- Read receipts
- Conversation history

✅ **Real-time Communication**

- Voice calls with WebRTC
- Video calls with camera and microphone controls
- Call timer and status indicators
- Socket.IO powered real-time features

✅ **AI-Powered Features** 🤖 ✨

- **Smart Conversation Starters**: AI-generated personalized icebreakers
- **Profile Bio Enhancement**: Get AI suggestions to improve your bio
- **Compatibility Analysis**: AI analyzes match compatibility with detailed insights
- **Date Ideas Generator**: Personalized date suggestions based on interests
- **Message Coaching**: Real-time feedback on message drafts
- **Profile Insights**: AI analysis of profile strength with improvement tips
- **Content Moderation**: Automatic safety screening of messages

✅ **Safety Features**

- Block users
- Report system
- Privacy settings
- Profile visibility controls
- AI-powered content moderation

✅ **Notifications**

- New matches
- New messages
- Profile likes
- In-app notifications

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Real-time**: Flask-SocketIO, Socket.IO
- **WebRTC**: Peer-to-peer voice and video calls
- **AI**: Groq API (Llama 3.3 70B model)
- **Frontend**: Tailwind CSS, Alpine.js
- **Icons**: Font Awesome 6

## Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd flask_dating
   ```

2. **Virtual environment is already created and activated**
   The virtual environment has been set up in the `venv` folder.

3. **Dependencies are already installed**
   All required packages have been installed from `requirements.txt`.

4. **Set up environment variables**

   Copy `.env.example` to `.env` and update the values:

   ```bash
   cp .env.example .env
   ```

   Update the `.env` file:

   ```
   SECRET_KEY=your-secret-key-here
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

   **Get your Groq API key**:

   - Visit [Groq Console](https://console.groq.com/)
   - Sign up/Login
   - Navigate to API Keys
   - Create a new API key
   - Copy and paste into `.env` file

5. **Run database migrations**

   ```bash
   python migrate_ai_tables.py
   ```

6. **Run the application**

   ```bash
   python run.py
   ```

7. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
flask_dating/
├── app/
│   ├── __init__.py              # App initialization
│   ├── models.py                # Database models
│   ├── forms.py                 # WTForms
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/                    # Main app blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── profile/                 # Profile blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── main/
│   │   └── profile/
│   └── static/
│       └── uploads/             # User uploaded files
├── venv/                        # Virtual environment
├── config.py                    # App configuration
├── run.py                       # App entry point
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Database Models

- **User**: Core user account information
- **Profile**: Extended profile details
- **TechInterest**: Tech categories (Web Dev, AI/ML, etc.)
- **ProgrammingLanguage**: Programming languages
- **Like**: User likes/interests
- **Match**: Mutual matches between users
- **Message**: Chat messages
- **Notification**: User notifications
- **Report**: User reports for moderation
- **Photo**: Additional profile photos
- **blocked_users**: Blocked users table

## Key Features Explained

### Discovery Algorithm

- Filters out blocked users and users who have blocked you
- Excludes already liked/passed users
- Age-based filtering
- Location-based matching (can be extended)

### Matching System

- Automatic match creation when mutual likes occur
- Instant notifications for new matches
- Match history tracking

### Safety & Privacy

- Block users functionality
- Report system with multiple categories
- Privacy settings for age, location, and online status
- Profile visibility controls

### Tech-Focused Features

- Current role and experience level
- Learning goals tracking
- Teaching skills showcase
- Collaboration interest preferences
- Integration with GitHub, Portfolio, and LinkedIn

## Customization

### Adding More Tech Interests

Edit `app/__init__.py` and add more interests to the initialization:

```python
TechInterest(name='Your Category', category='Type')
```

### Adding More Programming Languages

Edit `app/__init__.py` and add more languages:

```python
ProgrammingLanguage(name='Your Language')
```

### Changing Theme Colors

The app uses Tailwind CSS. Colors are defined in `app/templates/base.html`:

- Primary: Blue (#3b82f6)
- Secondary: Purple (#8b5cf6)
- Accent: Cyan (#06b6d4)

## Future Enhancements

- Real-time messaging with WebSockets
- Advanced search with tech stacks
- Video call integration
- Event/meetup organization
- Skill endorsements
- Project collaboration features
- AI-powered match recommendations
- Email notifications
- Mobile app version

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `.env`
2. Set `FLASK_DEBUG=0` in production
3. Use PostgreSQL instead of SQLite
4. Add HTTPS/SSL certificates
5. Implement rate limiting
6. Add email verification
7. Set up proper file upload validation
8. Configure CORS if needed
9. Add CSRF protection for all forms
10. Implement proper session management

## Contributing

This is a complete starter template. Feel free to:

- Add more features
- Improve the UI/UX
- Enhance the matching algorithm
- Add real-time features
- Implement AI capabilities

## License

This project is open source and available for learning purposes.

## Support

For issues or questions, please refer to Flask documentation:

- Flask: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Flask-Login: https://flask-login.readthedocs.io/

---

**Built with ❤️ for the tech community**
