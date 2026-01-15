"""
Database migration script to add AI feature tables
"""
from app import create_app, db
from app.models import CompatibilityAnalysis, AIConversationStarter, DateIdea, ContentModeration, ProfileInsight

def migrate():
    app = create_app()
    with app.app_context():
        # Create all new tables
        db.create_all()
        print("✅ AI feature tables created successfully!")
        print("   - compatibility_analyses")
        print("   - ai_conversation_starters")
        print("   - date_ideas")
        print("   - content_moderations")
        print("   - profile_insights")

if __name__ == '__main__':
    migrate()
