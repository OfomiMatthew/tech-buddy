# Quick Start Guide - AI Features Setup

## ⚡ Quick Setup (5 minutes)

### Step 1: Get Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up (it's FREE!)
3. Click "API Keys" in the sidebar
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

### Step 2: Configure the App

Open `config.py` and replace this line:

```python
GROQ_API_KEY = 'gsk_your_api_key_here'
```

with your actual key:

```python
GROQ_API_KEY = 'gsk_abc123...'  # Your real key here
```

### Step 3: Run Migration (If Not Done)

```bash
python migrate_ai_tables.py
```

### Step 4: Start the App

```bash
python run.py
```

### Step 5: Test AI Features

1. Login to your account
2. Go to any matched user's messages
3. Click the purple sparkle button (⚡)
4. Try "Conversation Starters"
5. Go to your profile page
6. Check "AI Profile Insights"

## ✨ That's it! All AI features are now active!

## 🎯 What Each Feature Does

### 1. **Conversation Starters** (In Messages)

- Generates 3 personalized icebreakers
- Based on both users' interests
- Click to use any starter

### 2. **Compatibility Analysis** (In Messages)

- Shows match % (0-100)
- Lists relationship strengths
- Suggests conversation topics
- Explains learning opportunities

### 3. **Date Ideas** (In Messages)

- 5 creative date suggestions
- Based on shared interests
- Tech-focused activities
- Location-aware

### 4. **Message Coach** (In Messages)

- Paste your message draft
- Get instant feedback
- Improve tone and clarity

### 5. **Bio Enhancer** (In Profile)

- Click "Enhance My Bio"
- AI suggests improvements
- Or generates new bio options

### 6. **Profile Insights** (In Profile)

- Shows profile completion %
- Lists strengths & improvements
- Provides actionable tips
- Updates weekly

### 7. **Content Moderation** (Automatic)

- Runs in background
- Screens for safety
- No setup needed

## 🔧 Troubleshooting

### "Groq API key not configured"

→ You forgot Step 2! Add your API key to config.py

### "Failed to generate..."

→ Check your internet connection
→ Verify API key is correct (no extra spaces)
→ Try again (Groq might be busy)

### Features not showing up

→ Restart the Flask server (Ctrl+C, then `python run.py`)
→ Clear browser cache (Ctrl+Shift+Delete)
→ Run migration: `python migrate_ai_tables.py`

## 💡 Tips for Best Results

1. **Complete Your Profile**: More info = better AI suggestions
2. **Be Specific**: Detailed bios get better enhancements
3. **Use Regularly**: AI learns from interactions
4. **Try Different Starters**: Mix AI suggestions with your personality
5. **Update Profile**: Refresh insights weekly for new tips

## 📊 Groq API Limits

**Free Tier**:

- 30 requests per minute
- Plenty for personal use
- App caches results to save API calls

**Caching**:

- Conversation starters: 7 days
- Compatibility: 30 days
- Date ideas: 14 days
- Profile insights: 7 days

## 🎉 Enjoy Your AI-Powered Dating App!

Questions? Check `AI_FEATURES.md` for detailed documentation.
