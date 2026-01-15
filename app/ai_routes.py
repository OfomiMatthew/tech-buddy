"""
AI Features Blueprint
Handles all AI-powered endpoints using Groq
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, User, CompatibilityAnalysis, AIConversationStarter, DateIdea, ProfileInsight
from app.groq_service import groq_service
import json
from sqlalchemy import or_, and_

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/conversation-starters/<int:match_id>')
@login_required
def conversation_starters(match_id):
    """Generate AI conversation starters for a match"""
    match_user = User.query.get_or_404(match_id)
    
    # Check if they're matched
    if not current_user.has_matched(match_user):
        return jsonify({'error': 'You must match with this user first'}), 403
    
    try:
        # Check if we have recent starters cached
        cached = AIConversationStarter.query.filter_by(
            user_id=current_user.id,
            match_id=match_id
        ).order_by(AIConversationStarter.created_at.desc()).first()
        
        if cached and (datetime.utcnow() - cached.created_at).days < 7:
            starters = json.loads(cached.starters)
        else:
            # Generate new starters
            starters = groq_service.generate_conversation_starters(
                current_user.profile,
                match_user.profile
            )
            
            # Cache them
            new_starters = AIConversationStarter(
                user_id=current_user.id,
                match_id=match_id,
                starters=json.dumps(starters)
            )
            db.session.add(new_starters)
            db.session.commit()
        
        return jsonify({'success': True, 'starters': starters})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/enhance-bio', methods=['POST'])
@login_required
def enhance_bio():
    """Get AI suggestions for bio improvement"""
    data = request.get_json()
    current_bio = data.get('bio', '')
    
    user_data = {
        'current_role': current_user.profile.current_role if current_user.profile else None,
        'interests': [i.name for i in current_user.interests],
        'languages': [l.name for l in current_user.languages],
        'experience_level': current_user.profile.experience_level if current_user.profile else None,
        'learning_goals': current_user.profile.learning_goals if current_user.profile else None,
        'can_teach': current_user.profile.can_teach if current_user.profile else None
    }
    
    try:
        suggestions = groq_service.enhance_bio(current_bio, user_data)
        return jsonify({'success': True, 'suggestions': suggestions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/compatibility/<int:match_id>')
@login_required
def compatibility_analysis(match_id):
    """Get AI compatibility analysis with a match"""
    match_user = User.query.get_or_404(match_id)
    
    # Check if they're matched
    if not current_user.has_matched(match_user):
        return jsonify({'error': 'You must match with this user first'}), 403
    
    try:
        # Check cache
        cached = CompatibilityAnalysis.query.filter(
            or_(
                and_(CompatibilityAnalysis.user1_id == current_user.id, CompatibilityAnalysis.user2_id == match_id),
                and_(CompatibilityAnalysis.user1_id == match_id, CompatibilityAnalysis.user2_id == current_user.id)
            )
        ).order_by(CompatibilityAnalysis.created_at.desc()).first()
        
        if cached and (datetime.utcnow() - cached.created_at).days < 30:
            result = {
                'compatibility_score': cached.compatibility_score,
                'strengths': json.loads(cached.strengths) if cached.strengths else [],
                'learning_opportunities': cached.learning_opportunities,
                'conversation_topics': json.loads(cached.conversation_topics) if cached.conversation_topics else [],
                'overall_summary': cached.overall_summary
            }
        else:
            # Generate new analysis
            result = groq_service.analyze_compatibility(
                current_user.profile,
                match_user.profile
            )
            
            if result:
                # Cache it
                analysis = CompatibilityAnalysis(
                    user1_id=current_user.id,
                    user2_id=match_id,
                    compatibility_score=result.get('compatibility_score'),
                    strengths=json.dumps(result.get('strengths', [])),
                    learning_opportunities=result.get('learning_opportunities'),
                    conversation_topics=json.dumps(result.get('conversation_topics', [])),
                    overall_summary=result.get('overall_summary')
                )
                db.session.add(analysis)
                db.session.commit()
        
        return jsonify({'success': True, 'analysis': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/date-ideas/<int:match_id>')
@login_required
def date_ideas(match_id):
    """Generate AI date ideas for a match"""
    match_user = User.query.get_or_404(match_id)
    
    # Check if they're matched
    if not current_user.has_matched(match_user):
        return jsonify({'error': 'You must match with this user first'}), 403
    
    try:
        # Check cache
        cached = DateIdea.query.filter(
            or_(
                and_(DateIdea.user1_id == current_user.id, DateIdea.user2_id == match_id),
                and_(DateIdea.user1_id == match_id, DateIdea.user2_id == current_user.id)
            )
        ).order_by(DateIdea.created_at.desc()).first()
        
        if cached and (datetime.utcnow() - cached.created_at).days < 14:
            ideas = json.loads(cached.ideas)
        else:
            # Generate new ideas
            ideas = groq_service.generate_date_ideas(
                current_user.profile,
                match_user.profile
            )
            
            # Cache them
            new_ideas = DateIdea(
                user1_id=current_user.id,
                user2_id=match_id,
                ideas=json.dumps(ideas)
            )
            db.session.add(new_ideas)
            db.session.commit()
        
        return jsonify({'success': True, 'ideas': ideas})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/message-coach', methods=['POST'])
@login_required
def message_coach():
    """Get AI coaching on a message draft"""
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context', None)
    
    if not message or len(message) < 5:
        return jsonify({'success': False, 'error': 'Message too short'}), 400
    
    try:
        coaching = groq_service.coach_message(message, context)
        return jsonify({'success': True, 'coaching': coaching})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/profile-insights')
@login_required
def profile_insights():
    """Get AI insights about profile"""
    try:
        # Calculate stats
        likes_sent = current_user.sent_likes.count()
        likes_received = current_user.received_likes.count()
        
        # Count matches
        matches = 0
        for like in current_user.sent_likes:
            if like.liked.has_liked(current_user):
                matches += 1
        
        # Profile completeness
        completeness = 0
        if current_user.profile:
            fields = [
                current_user.profile.bio,
                current_user.profile.profile_photo,
                current_user.profile.current_role,
                current_user.profile.learning_goals,
                current_user.profile.can_teach,
                len(current_user.interests) > 0,
                len(current_user.languages) > 0
            ]
            completeness = int((sum(1 for f in fields if f) / len(fields)) * 100)
        
        stats = {
            'photo_count': 1 if current_user.profile and current_user.profile.profile_photo else 0,
            'completeness': completeness,
            'views': 0,  # Would need view tracking
            'likes_sent': likes_sent,
            'likes_received': likes_received,
            'matches': matches,
            'response_rate': 0  # Would need message tracking
        }
        
        # Check cache
        cached = ProfileInsight.query.filter_by(
            user_id=current_user.id
        ).order_by(ProfileInsight.created_at.desc()).first()
        
        if cached and (datetime.utcnow() - cached.created_at).days < 7:
            insights = cached.insights
        else:
            # Generate new insights
            insights = groq_service.generate_profile_insights(
                current_user.profile if current_user.profile else None,
                stats
            )
            
            # Cache them
            new_insight = ProfileInsight(
                user_id=current_user.id,
                insights=insights,
                profile_score=stats['completeness']
            )
            db.session.add(new_insight)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'insights': insights,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@ai_bp.route('/moderate', methods=['POST'])
@login_required
def moderate():
    """Moderate content using AI (internal use)"""
    # This would typically be called internally, not by users
    data = request.get_json()
    content = data.get('content', '')
    content_type = data.get('type', 'message')
    
    if not content:
        return jsonify({'success': False, 'error': 'No content provided'}), 400
    
    try:
        result = groq_service.moderate_content(content, content_type)
        return jsonify({'success': True, 'moderation': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


from datetime import datetime
