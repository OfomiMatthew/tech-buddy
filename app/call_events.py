from flask import request, session
from flask_socketio import emit
from flask_login import current_user
from app import socketio

# Store user socket IDs
user_sockets = {}

@socketio.on('connect')
def handle_connect():
    print(f'Socket connection attempt - Session: {session}')
    if current_user.is_authenticated:
        user_sockets[current_user.id] = request.sid
        print(f'✅ User {current_user.id} ({current_user.username}) connected with socket {request.sid}')
        print(f'Active sockets: {user_sockets}')
    else:
        print('⚠️ Unauthenticated connection attempt')

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        if current_user.id in user_sockets:
            del user_sockets[current_user.id]
        print(f'❌ User {current_user.id} disconnected')
        print(f'Active sockets: {user_sockets}')

@socketio.on('initiate_call')
def handle_initiate_call(data):
    """Handle call initiation from one user to another"""
    print('\n📞 INITIATE CALL Event received:')
    print(f'   Data: {data}')
    print(f'   Authenticated: {current_user.is_authenticated}')
    
    if not current_user.is_authenticated:
        print('   ❌ User not authenticated')
        return
    
    receiver_id = data.get('receiver_id')
    call_type = data.get('call_type')  # 'voice' or 'video'
    
    print(f'   Caller: User {current_user.id} ({current_user.username})')
    print(f'   Receiver: User {receiver_id}')
    print(f'   Call Type: {call_type}')
    print(f'   Active sockets: {user_sockets}')
    print(f'   Receiver in sockets: {receiver_id in user_sockets}')
    
    if receiver_id in user_sockets:
        receiver_socket = user_sockets[receiver_id]
        print(f'   ✅ Sending incoming_call to socket {receiver_socket}')
        
        emit('incoming_call', {
            'caller_id': current_user.id,
            'caller_username': current_user.username,
            'caller_photo': current_user.profile.profile_photo if current_user.profile else None,
            'call_type': call_type
        }, room=receiver_socket)
        
        print(f'   ✅ Call notification sent to User {receiver_id}')
    else:
        print('   ❌ Receiver not connected (not in sockets dict)')

@socketio.on('accept_call')
def handle_accept_call(data):
    """Handle call acceptance"""
    if not current_user.is_authenticated:
        return
    
    caller_id = data.get('caller_id')
    
    if caller_id in user_sockets:
        emit('call_accepted', {
            'accepter_id': current_user.id,
            'accepter_username': current_user.username
        }, room=user_sockets[caller_id])
        
        print(f'Call accepted by {current_user.id} from {caller_id}')

@socketio.on('reject_call')
def handle_reject_call(data):
    """Handle call rejection"""
    if not current_user.is_authenticated:
        return
    
    caller_id = data.get('caller_id')
    
    if caller_id in user_sockets:
        emit('call_rejected', {
            'rejecter_id': current_user.id
        }, room=user_sockets[caller_id])
        
        print(f'Call rejected by {current_user.id} from {caller_id}')

@socketio.on('end_call')
def handle_end_call(data):
    """Handle call end"""
    if not current_user.is_authenticated:
        return
    
    other_user_id = data.get('other_user_id')
    
    if other_user_id in user_sockets:
        emit('call_ended', {
            'ended_by': current_user.id
        }, room=user_sockets[other_user_id])
        
        print(f'Call ended by {current_user.id}')

@socketio.on('webrtc_offer')
def handle_webrtc_offer(data):
    """Forward WebRTC offer to the other peer"""
    if not current_user.is_authenticated:
        return
    
    receiver_id = data.get('receiver_id')
    offer = data.get('offer')
    
    if receiver_id in user_sockets:
        emit('webrtc_offer', {
            'sender_id': current_user.id,
            'offer': offer
        }, room=user_sockets[receiver_id])

@socketio.on('webrtc_answer')
def handle_webrtc_answer(data):
    """Forward WebRTC answer to the other peer"""
    if not current_user.is_authenticated:
        return
    
    receiver_id = data.get('receiver_id')
    answer = data.get('answer')
    
    if receiver_id in user_sockets:
        emit('webrtc_answer', {
            'sender_id': current_user.id,
            'answer': answer
        }, room=user_sockets[receiver_id])

@socketio.on('webrtc_ice_candidate')
def handle_ice_candidate(data):
    """Forward ICE candidate to the other peer"""
    if not current_user.is_authenticated:
        return
    
    receiver_id = data.get('receiver_id')
    candidate = data.get('candidate')
    
    if receiver_id in user_sockets:
        emit('webrtc_ice_candidate', {
            'sender_id': current_user.id,
            'candidate': candidate
        }, room=user_sockets[receiver_id])
