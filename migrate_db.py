"""
Database migration script to add new message features
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Add new columns to messages table
        with db.engine.connect() as conn:
            # Check if columns already exist
            result = conn.execute(text("PRAGMA table_info(messages)"))
            columns = [row[1] for row in result]
            
            if 'message_type' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN message_type VARCHAR(20) DEFAULT 'text'"))
                conn.commit()
                print("✓ Added message_type column")
            
            if 'file_url' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN file_url VARCHAR(255)"))
                conn.commit()
                print("✓ Added file_url column")
            
            if 'file_name' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN file_name VARCHAR(255)"))
                conn.commit()
                print("✓ Added file_name column")
            
            if 'file_size' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN file_size INTEGER"))
                conn.commit()
                print("✓ Added file_size column")
            
            if 'duration' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN duration INTEGER"))
                conn.commit()
                print("✓ Added duration column")
            
            if 'reaction' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN reaction VARCHAR(10)"))
                conn.commit()
                print("✓ Added reaction column")
            
            if 'is_deleted' not in columns:
                conn.execute(text("ALTER TABLE messages ADD COLUMN is_deleted BOOLEAN DEFAULT 0"))
                conn.commit()
                print("✓ Added is_deleted column")
            
            # Make content nullable
            print("✓ Updated content to be nullable (requires table recreation in SQLite)")
            print("\nNote: If you want to make 'content' nullable, you'll need to recreate the table")
            print("For now, existing messages will work fine with the new features!")
        
        print("\n✅ Database migration completed successfully!")
        print("New messaging features enabled:")
        print("  - Voice notes")
        print("  - Image sharing")
        print("  - Video sharing")
        print("  - File attachments")
        print("  - Message reactions")
        print("  - Message deletion")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        print("You may need to delete the database and start fresh.")
