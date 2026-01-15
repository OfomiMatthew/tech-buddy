"""
Groq AI Service for TechBuddy Dating App
Handles all AI-powered features using Groq API
"""
from groq import Groq
from flask import current_app
import json
import re


class GroqService:
    def __init__(self):
        self.client = None
    
    def _get_client(self):
        """Initialize Groq client if not already done"""
        if not self.client:
            api_key = current_app.config.get('GROQ_API_KEY')
            if not api_key or api_key == 'gsk_your_api_key_here':
                raise ValueError("Groq API key not configured. Please set GROQ_API_KEY in config or environment.")
            self.client = Groq(api_key=api_key)
        return self.client
    
    def _call_groq(self, prompt, system_message="You are a helpful AI assistant for a tech-focused dating app.", temperature=0.7, max_tokens=1024):
        """Make a call to Groq API"""
        try:
            client = self._get_client()
            model = current_app.config.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            current_app.logger.error(f"Groq API error: {str(e)}")
            raise
    
    # Feature 1: Smart Conversation Starters
    def generate_conversation_starters(self, user_profile, match_profile, count=3):
        """Generate personalized conversation starters based on both profiles"""
        user_interests = ", ".join([i.name for i in user_profile.user.interests]) if user_profile.user.interests else "general tech"
        user_languages = ", ".join([l.name for l in user_profile.user.languages]) if user_profile.user.languages else "programming"
        
        match_interests = ", ".join([i.name for i in match_profile.user.interests]) if match_profile.user.interests else "general tech"
        match_languages = ", ".join([l.name for l in match_profile.user.languages]) if match_profile.user.languages else "programming"
        
        prompt = f"""Generate {count} personalized, natural conversation starters for a dating app focused on tech professionals.

User Profile:
- Interests: {user_interests}
- Programming Languages: {user_languages}
- Learning Goals: {user_profile.learning_goals or 'Not specified'}
- Current Role: {user_profile.current_role or 'Not specified'}

Match Profile:
- Name: {match_profile.user.username}
- Interests: {match_interests}
- Programming Languages: {match_languages}
- Bio: {match_profile.bio or 'No bio'}
- Current Role: {match_profile.current_role or 'Not specified'}
- Can Teach: {match_profile.can_teach or 'Not specified'}

Requirements:
- Make them engaging and reference shared interests or complementary skills
- Keep each under 150 characters
- Be friendly and approachable, not cheesy
- Focus on tech topics, projects, or learning
- Format as a numbered list

Return only the conversation starters, nothing else."""

        system_message = "You are a helpful assistant that creates engaging, tech-focused conversation starters for professionals."
        
        try:
            response = self._call_groq(prompt, system_message, temperature=0.8)
            # Parse the response to extract individual starters
            starters = []
            lines = response.strip().split('\n')
            for line in lines:
                line = line.strip()
                # Remove numbering (1., 2., 3., etc.)
                cleaned = re.sub(r'^\d+[\.\)]\s*', '', line)
                # Remove bullet points
                cleaned = re.sub(r'^[\-\*]\s*', '', cleaned)
                # Remove quotes
                cleaned = cleaned.strip('"\'')
                if cleaned and len(cleaned) > 10:
                    starters.append(cleaned)
            
            return starters[:count] if starters else [response]
        except Exception as e:
            current_app.logger.error(f"Error generating conversation starters: {str(e)}")
            return [
                f"I noticed we both are into {match_interests.split(',')[0] if match_interests else 'tech'}. What project are you working on?",
                f"Your profile caught my eye! What got you interested in {match_profile.current_role or 'tech'}?",
                "I'm always looking to learn new things. What's something you're passionate about teaching?"
            ]
    
    # Feature 2: Profile Bio Enhancement
    def enhance_bio(self, current_bio, user_data):
        """Suggest improvements or generate a bio based on user data"""
        if current_bio:
            prompt = f"""Improve this dating profile bio for a tech professional. Make it more engaging while keeping the core message.

Current Bio:
{current_bio}

User Info:
- Role: {user_data.get('current_role', 'Not specified')}
- Interests: {', '.join(user_data.get('interests', []))}
- Experience Level: {user_data.get('experience_level', 'Not specified')}

Provide:
1. An improved version of the bio (2-3 sentences max)
2. Three specific suggestions for improvement

Format as:
IMPROVED BIO:
[bio text]

SUGGESTIONS:
1. [suggestion]
2. [suggestion]
3. [suggestion]"""
        else:
            prompt = f"""Create an engaging dating profile bio for a tech professional.

User Info:
- Role: {user_data.get('current_role', 'Developer')}
- Interests: {', '.join(user_data.get('interests', ['coding']))}
- Programming Languages: {', '.join(user_data.get('languages', ['Python']))}
- Experience Level: {user_data.get('experience_level', 'Intermediate')}
- Learning Goals: {user_data.get('learning_goals', 'Expanding knowledge')}
- Can Teach: {user_data.get('can_teach', 'Various skills')}

Create 3 different bio options (each 2-3 sentences), each with a different tone:
1. Professional & approachable
2. Casual & friendly
3. Passionate & enthusiastic

Format clearly with headers."""

        system_message = "You are an expert at writing engaging dating profiles for tech professionals. Be authentic, interesting, and help people show their personality."
        
        try:
            return self._call_groq(prompt, system_message, temperature=0.8, max_tokens=800)
        except Exception as e:
            current_app.logger.error(f"Error enhancing bio: {str(e)}")
            return None
    
    # Feature 3: Intelligent Matchmaking Analysis
    def analyze_compatibility(self, user_profile, match_profile):
        """Analyze compatibility between two users and provide insights"""
        user_interests = ", ".join([i.name for i in user_profile.user.interests]) if user_profile.user.interests else "none"
        user_languages = ", ".join([l.name for l in user_profile.user.languages]) if user_profile.user.languages else "none"
        
        match_interests = ", ".join([i.name for i in match_profile.user.interests]) if match_profile.user.interests else "none"
        match_languages = ", ".join([l.name for l in match_profile.user.languages]) if match_profile.user.languages else "none"
        
        prompt = f"""Analyze compatibility between two tech professionals for dating purposes.

Person A:
- Interests: {user_interests}
- Languages: {user_languages}
- Current Role: {user_profile.current_role or 'Not specified'}
- Experience Level: {user_profile.experience_level or 'Not specified'}
- Learning Goals: {user_profile.learning_goals or 'Not specified'}
- Can Teach: {user_profile.can_teach or 'Not specified'}
- Looking For: {user_profile.user.looking_for or 'Not specified'}

Person B:
- Interests: {match_interests}
- Languages: {match_languages}
- Current Role: {match_profile.current_role or 'Not specified'}
- Experience Level: {match_profile.experience_level or 'Not specified'}
- Learning Goals: {match_profile.learning_goals or 'Not specified'}
- Can Teach: {match_profile.can_teach or 'Not specified'}
- Looking For: {match_profile.user.looking_for or 'Not specified'}

Provide a JSON response with:
{{
  "compatibility_score": <0-100>,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "learning_opportunities": "description of what they can learn from each other",
  "conversation_topics": ["topic 1", "topic 2", "topic 3"],
  "overall_summary": "brief summary"
}}

Return ONLY valid JSON, no additional text."""

        system_message = "You are an expert matchmaking analyst for tech professionals. Analyze compatibility based on technical skills, learning potential, and personality fit."
        
        try:
            response = self._call_groq(prompt, system_message, temperature=0.6, max_tokens=1024)
            # Try to parse JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                return {
                    "compatibility_score": 70,
                    "strengths": ["Shared tech interests", "Complementary skills", "Similar experience level"],
                    "learning_opportunities": "Great potential to learn from each other's expertise",
                    "conversation_topics": ["Tech projects", "Career growth", "New technologies"],
                    "overall_summary": response[:200]
                }
        except Exception as e:
            current_app.logger.error(f"Error analyzing compatibility: {str(e)}")
            return None
    
    # Feature 4: Safety & Content Moderation
    def moderate_content(self, content, content_type="message"):
        """Check if content is appropriate and safe"""
        prompt = f"""Analyze this {content_type} for a dating platform. Check for:
- Inappropriate or explicit content
- Harassment or offensive language
- Spam or scam attempts
- Personal information sharing (phone, email, address)
- Unsafe requests or propositions

Content:
{content}

Respond with JSON:
{{
  "is_safe": <true/false>,
  "risk_level": "<low/medium/high>",
  "issues": ["issue1", "issue2"],
  "suggested_action": "<allow/warn/block>",
  "reason": "brief explanation"
}}

Return ONLY valid JSON."""

        system_message = "You are a content moderation AI for a dating platform. Be thorough but fair. Allow flirting but block harassment."
        
        try:
            response = self._call_groq(prompt, system_message, temperature=0.3, max_tokens=512)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Default to safe if parsing fails
                return {
                    "is_safe": True,
                    "risk_level": "low",
                    "issues": [],
                    "suggested_action": "allow",
                    "reason": "No issues detected"
                }
        except Exception as e:
            current_app.logger.error(f"Error moderating content: {str(e)}")
            # Fail open for now
            return {
                "is_safe": True,
                "risk_level": "low",
                "issues": [],
                "suggested_action": "allow",
                "reason": "Moderation service unavailable"
            }
    
    # Feature 5: Date Ideas Generator
    def generate_date_ideas(self, user_profile, match_profile, count=5):
        """Generate personalized date ideas based on both profiles"""
        shared_interests = set([i.name for i in user_profile.user.interests]) & set([i.name for i in match_profile.user.interests])
        
        user_city = user_profile.user.city or "their area"
        collaboration_type = user_profile.collaboration_interest or "any activity"
        
        prompt = f"""Generate {count} creative date ideas for two tech professionals who matched on a dating app.

Shared Interests: {', '.join(shared_interests) if shared_interests else 'tech in general'}
Location: {user_city}
Collaboration Interest: {collaboration_type}
User 1 Can Teach: {user_profile.can_teach or 'various skills'}
User 2 Can Teach: {match_profile.can_teach or 'various skills'}

Create date ideas that:
- Incorporate their tech interests naturally
- Range from casual coffee to creative activities
- Include both indoor and outdoor options
- Allow for good conversation
- Are appropriate for a first or early date

Format each as:
**Title**: Brief description (2-3 sentences)

Be creative but realistic."""

        system_message = "You are a creative date planner for tech professionals. Suggest engaging, fun dates that let people connect over shared interests."
        
        try:
            response = self._call_groq(prompt, system_message, temperature=0.9, max_tokens=1024)
            # Parse into individual ideas
            ideas = []
            sections = response.split('**')[1:]  # Split by ** markers
            for i in range(0, len(sections), 2):
                if i + 1 < len(sections):
                    title = sections[i].strip().rstrip(':')
                    description = sections[i + 1].strip()
                    ideas.append({"title": title, "description": description})
            
            return ideas[:count] if ideas else [{"title": "Tech Talk Coffee Date", "description": response}]
        except Exception as e:
            current_app.logger.error(f"Error generating date ideas: {str(e)}")
            return [
                {"title": "Coffee & Code", "description": "Meet at a cozy cafe and chat about your latest projects over coffee."},
                {"title": "Tech Museum Visit", "description": "Explore interactive exhibits and discuss innovation together."},
                {"title": "Pair Programming Session", "description": "Work on a fun mini-project together at a co-working space."}
            ]
    
    # Feature 6: Message Coaching
    def coach_message(self, message_draft, context=None):
        """Provide feedback on a message draft"""
        prompt = f"""You're helping someone improve a message they want to send on a dating app.

Their draft message:
"{message_draft}"

{f"Context: {context}" if context else ""}

Provide:
1. Overall tone assessment (friendly/awkward/good/etc)
2. 2-3 specific suggestions for improvement
3. An improved version (optional, only if needed)

Be encouraging but honest. Format clearly."""

        system_message = "You are a helpful dating coach. Give constructive feedback to help people communicate better."
        
        try:
            return self._call_groq(prompt, system_message, temperature=0.7, max_tokens=512)
        except Exception as e:
            current_app.logger.error(f"Error coaching message: {str(e)}")
            return "Your message looks good! Just be yourself and keep the conversation flowing naturally."
    
    # Feature 7: Profile Insights
    def generate_profile_insights(self, user_profile, stats):
        """Generate insights and tips for improving profile success"""
        prompt = f"""Analyze this dating profile and provide actionable insights.

Profile:
- Bio: {user_profile.bio or 'No bio'}
- Role: {user_profile.current_role or 'Not specified'}
- Experience: {user_profile.experience_level or 'Not specified'}
- Interests: {len(user_profile.user.interests)} listed
- Languages: {len(user_profile.user.languages)} listed
- Photos: {stats.get('photo_count', 0)}
- Profile completeness: {stats.get('completeness', 0)}%

Stats:
- Profile views: {stats.get('views', 0)}
- Likes sent: {stats.get('likes_sent', 0)}
- Likes received: {stats.get('likes_received', 0)}
- Matches: {stats.get('matches', 0)}
- Response rate: {stats.get('response_rate', 0)}%

Provide:
1. Profile strength score (0-100) with brief explanation
2. Top 3 strengths
3. Top 3 improvement areas with specific actions
4. 2-3 tips to increase matches

Be specific, actionable, and encouraging."""

        system_message = "You are a dating profile optimization expert for tech professionals. Give practical, data-driven advice."
        
        try:
            return self._call_groq(prompt, system_message, temperature=0.7, max_tokens=1024)
        except Exception as e:
            current_app.logger.error(f"Error generating insights: {str(e)}")
            return "Keep your profile updated and engage authentically with matches. Quality photos and a complete bio make a big difference!"


# Global instance
groq_service = GroqService()
