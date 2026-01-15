# AI Features Documentation

## Overview

This dating app now includes 7 AI-powered features using Groq API to enhance user experience:

## 🚀 AI Features

### 1. **Smart Conversation Starters** ✨

- **Location**: Messages page (AI sparkle button)
- **Function**: Generates 3 personalized icebreakers based on both users' profiles
- **Benefits**: Helps users start meaningful conversations
- **Usage**: Click AI button → "Conversation Starters" → Click any starter to use it

### 2. **Profile Bio Enhancement** 📝

- **Location**: My Profile page
- **Function**: AI analyzes and suggests improvements to user bios or generates new ones
- **Benefits**: Creates more engaging profiles that attract better matches
- **Usage**: Click "Enhance My Bio with AI" button → Get AI suggestions

### 3. **Intelligent Matchmaking Analysis** 💕

- **Location**: Messages page (AI menu)
- **Function**: Provides compatibility score (0-100%) with detailed analysis
- **Analysis Includes**:
  - Compatibility percentage
  - Relationship strengths
  - Learning opportunities from each other
  - Great conversation topics
  - Overall summary
- **Usage**: Click AI button → "Compatibility Analysis"

### 4. **Safety & Content Moderation** 🛡️

- **Location**: Backend (automatic)
- **Function**: Automatically screens messages for inappropriate content
- **Checks For**:
  - Explicit or offensive language
  - Harassment
  - Spam/scam attempts
  - Personal information sharing
  - Unsafe propositions
- **Action**: Flags, warns, or blocks based on risk level

### 5. **Date Ideas Generator** 💡

- **Location**: Messages page (AI menu)
- **Function**: Creates 5 personalized date suggestions based on shared interests
- **Ideas Include**:
  - Tech-focused activities
  - Indoor and outdoor options
  - Casual to creative suggestions
  - Location-aware recommendations
- **Usage**: Click AI button → "Date Ideas"

### 6. **Message Coaching** 🎯

- **Location**: Messages page (AI menu)
- **Function**: Provides real-time feedback on message drafts
- **Feedback Includes**:
  - Tone assessment
  - Specific improvement suggestions
  - Improved version (if needed)
- **Usage**: Click AI button → "Message Coach" → Paste draft → Get feedback

### 7. **Profile Insights** 📊

- **Location**: My Profile page
- **Function**: AI analyzes profile and provides actionable insights
- **Provides**:
  - Profile strength score (0-100)
  - Top 3 strengths
  - Top 3 improvement areas
  - Tips to increase matches
  - Stats dashboard (completeness, matches, likes)
- **Usage**: Automatically loads on profile page, click "Refresh" to update

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### 3. Configure API Key

**Option A: Environment Variable (Recommended)**

```bash
# Windows
set GROQ_API_KEY=gsk_your_actual_api_key_here

# Linux/Mac
export GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Option B: Update config.py**

```python
# In config.py
GROQ_API_KEY = 'gsk_your_actual_api_key_here'
```

### 4. Run Database Migration

```bash
python migrate_ai_tables.py
```

### 5. Start the App

```bash
python run.py
```

## 🎨 User Interface

### AI Button Location

- **Messages Page**: Purple sparkle button (⚡) in chat header
- **Profile Page**: "AI Profile Insights" section with "Enhance My Bio" button

### Visual Design

- **Purple/Blue theme** for AI features (distinguishes from regular features)
- **Loading spinners** during AI generation
- **Modal windows** for immersive experience
- **Smooth animations** and transitions

## ⚙️ Technical Details

### API Model

- **Model**: `llama-3.3-70b-versatile`
- **Provider**: Groq (ultra-fast LLM inference)
- **Average Response Time**: 1-2 seconds
- **Temperature**: 0.6-0.9 (depending on feature)

### Caching Strategy

- **Conversation Starters**: 7 days cache
- **Compatibility Analysis**: 30 days cache
- **Date Ideas**: 14 days cache
- **Profile Insights**: 7 days cache
- **Bio Enhancement**: No cache (always fresh)
- **Message Coaching**: No cache (real-time)

### Database Tables

```sql
compatibility_analyses - Stores match compatibility data
ai_conversation_starters - Caches generated icebreakers
date_ideas - Stores personalized date suggestions
content_moderations - Logs moderation results
profile_insights - Stores profile analysis
```

### API Endpoints

```
GET  /ai/conversation-starters/<match_id>
POST /ai/enhance-bio
GET  /ai/compatibility/<match_id>
GET  /ai/date-ideas/<match_id>
POST /ai/message-coach
GET  /ai/profile-insights
POST /ai/moderate (internal)
```

## 🚨 Error Handling

### Fallback Mechanisms

1. **API Key Missing**: Shows error message with setup instructions
2. **API Timeout**: Displays retry button
3. **Rate Limit**: Uses cached results or fallback responses
4. **Parse Error**: Returns fallback content

### User-Friendly Messages

- Clear error descriptions
- Retry buttons where appropriate
- Fallback content when AI unavailable

## 📈 Performance Optimization

### Best Practices

1. **Caching**: Reduces API calls by storing results
2. **Async Loading**: UI remains responsive during AI processing
3. **Progressive Enhancement**: App works without AI, better with it
4. **Lazy Loading**: AI features load on-demand

### Rate Limiting

- Groq Free Tier: 30 requests/minute
- Cached results reduce API usage
- Consider upgrading for high-traffic apps

## 🔒 Privacy & Safety

### Content Moderation

- Automatic screening of all messages
- Risk levels: Low, Medium, High
- Actions: Allow, Warn, Block
- Protects users from harmful content

### Data Privacy

- AI analyses are cached locally (not sent to third parties)
- User profiles analyzed only with consent
- No personal data shared beyond what's needed for analysis

## 🎯 Best Practices for Users

### For Better AI Results

1. **Complete Your Profile**: More data = better suggestions
2. **Be Specific**: Detailed bios get better enhancement
3. **Update Regularly**: Refresh insights as profile evolves
4. **Use Starters Creatively**: Personalize AI suggestions
5. **Coach Before Sending**: Review important messages

## 🐛 Troubleshooting

### "Groq API key not configured"

- Set `GROQ_API_KEY` environment variable
- Or update `config.py` with your key

### "Failed to generate..."

- Check internet connection
- Verify API key is valid
- Check Groq API status
- Try again (may be temporary)

### Features Not Showing

- Run `python migrate_ai_tables.py`
- Clear browser cache
- Restart Flask server

## 📚 Resources

- [Groq Documentation](https://console.groq.com/docs)
- [Groq Models](https://console.groq.com/docs/models)
- [API Reference](https://console.groq.com/docs/api-reference)

## 🎉 Future Enhancements

Potential additions:

- Voice message transcription with AI summary
- Photo analysis and suggestions
- Behavioral pattern detection
- Personalized notification timing
- Multi-language support
- Advanced matching algorithms
- Sentiment analysis on conversations
- Automated date planning assistant

## 💬 Support

For issues or questions:

1. Check this documentation
2. Review error messages
3. Check Groq API status
4. Verify configuration
5. Restart server

---

**Note**: Groq API is required for AI features. The app will function normally without it, but AI features will show error messages.
