# Voice & Video Call Feature - Implementation Guide

## 🎉 Features Implemented

### Real-Time Communication

- ✅ Socket.IO integration for real-time signaling
- ✅ WebRTC peer-to-peer connection for audio/video
- ✅ Automatic connection establishment between users
- ✅ ICE candidate exchange for NAT traversal

### Voice Calls

- ✅ Initiate voice calls with click of a button
- ✅ Incoming call notification with ringtone
- ✅ Accept/Reject incoming calls
- ✅ Mute/Unmute microphone
- ✅ End call functionality

### Video Calls

- ✅ Initiate video calls
- ✅ Side-by-side video display (local and remote)
- ✅ Toggle video on/off
- ✅ Mute/Unmute audio during video call
- ✅ Full-screen call modal interface

## 🔧 Technical Implementation

### Backend (Flask + Socket.IO)

**Files Modified:**

- `app/__init__.py` - Added Socket.IO initialization
- `app/call_events.py` - NEW: Socket.IO event handlers for calls
- `run.py` - Updated to use socketio.run()
- `requirements.txt` - Added Flask-SocketIO and python-socketio

**Socket Events:**

- `initiate_call` - Sent when user starts a call
- `accept_call` - Sent when user accepts incoming call
- `reject_call` - Sent when user rejects incoming call
- `end_call` - Sent when user ends active call
- `webrtc_offer` - WebRTC offer exchange
- `webrtc_answer` - WebRTC answer exchange
- `webrtc_ice_candidate` - ICE candidate exchange for connection

### Frontend (WebRTC + Socket.IO)

**Files Modified:**

- `app/templates/base.html` - Added Socket.IO CDN script
- `app/templates/main/messages.html` - Complete WebRTC implementation

**Key Features:**

- Real-time socket connection per user
- WebRTC PeerConnection with STUN servers
- Local and remote media stream handling
- Incoming call modal with ringtone
- Call controls (mute, video toggle, end call)

## 🚀 How It Works

### Making a Call

1. User clicks phone/video icon in chat
2. System requests media permissions (camera/mic)
3. Socket.IO emits `initiate_call` to receiver
4. WebRTC offer created and sent via socket
5. Receiver gets incoming call notification with ringtone

### Receiving a Call

1. Incoming call modal appears with caller info
2. Ringtone plays automatically
3. User can Accept or Reject
4. If accepted: WebRTC answer sent, connection established
5. If rejected: Caller notified, call cancelled

### During Call

1. **Mute/Unmute**: Toggle audio track on/off
2. **Video Toggle**: Enable/disable video track (video calls only)
3. **End Call**: Stops all tracks, closes connection, notifies other user

## 📋 User Flow

### Caller's Perspective

```
Click Call Button → Media Permission → "Calling..." Status →
→ Wait for Answer → Connection Established → Call Controls Active
```

### Receiver's Perspective

```
Receive Socket Event → Incoming Call Modal + Ringtone →
→ Accept/Reject → Media Permission (if accept) →
→ Connection Established → Call Controls Active
```

## 🎨 UI Components

### Call Buttons (In Chat Header)

- Green phone icon for voice calls
- Blue video icon for video calls
- Hover effects and tooltips

### Incoming Call Modal

- Full-screen dark overlay
- Animated pulsing phone icon
- Caller name and call type
- Large Accept (green) and Reject (red) buttons
- Automatic ringtone playback

### Active Call Modal

- Full-screen interface with dark theme
- Call type and status display
- Video grid (2 columns for video calls)
- Call controls at bottom:
  - Mute/Unmute button (microphone icon)
  - Video toggle button (camera icon, video calls only)
  - End call button (red phone icon)

## 🔒 Security & Permissions

### Browser Permissions Required

- Microphone access (all calls)
- Camera access (video calls only)
- Permissions requested only when call initiated/accepted

### Network Configuration

- Uses Google's STUN servers for NAT traversal
- Peer-to-peer connection (no media goes through server)
- Signaling through secure Socket.IO connection

## 🐛 Troubleshooting

### "Could not access camera/microphone"

- **Cause**: Browser permissions denied or device not available
- **Solution**: Grant permissions in browser settings, check device connections

### Call not connecting

- **Cause**: Network firewall blocking WebRTC
- **Solution**: May need TURN server for restrictive networks (not included in basic implementation)

### No incoming call notification

- **Cause**: Socket.IO not connected or user not online
- **Solution**: Check server logs, ensure both users are connected

### Ringtone not playing

- **Cause**: Browser autoplay policy
- **Solution**: User must interact with page before ringtone can play

## 🔮 Future Enhancements

### Potential Improvements

1. **TURN Server**: Add for networks that block peer-to-peer
2. **Call History**: Store call logs in database
3. **Screen Sharing**: Add option to share screen during video call
4. **Call Recording**: Record calls with user permission
5. **Group Calls**: Support for multiple participants
6. **Better Ringtones**: Custom ringtone files
7. **Call Quality Indicator**: Show connection strength
8. **Reconnection Logic**: Handle network disruptions
9. **Mobile Optimization**: Better UI for mobile devices
10. **Push Notifications**: Notify users when app is not open

## 📱 Testing Instructions

### Test Voice Call

1. Open two browser windows (or use incognito for second user)
2. Log in as different users in each window
3. Navigate to messages between the two users
4. Click green phone icon in one window
5. Accept call in other window
6. Test mute/unmute functionality
7. End call from either side

### Test Video Call

1. Follow same steps as voice call
2. Click blue video icon instead
3. Verify local video appears immediately
4. Verify remote video appears after acceptance
5. Test video toggle (camera on/off)
6. Test mute during video call
7. End call from either side

### Test Call Rejection

1. Initiate call from one window
2. Click reject in other window
3. Verify caller receives rejection notification

## 📊 System Requirements

### Server

- Python 3.7+
- Flask 3.0.0
- Flask-SocketIO 5.3.5+
- python-socketio 5.10.0+

### Client (Browser)

- Modern browser with WebRTC support:
  - Chrome 74+
  - Firefox 66+
  - Safari 12.1+
  - Edge 79+
- Stable internet connection
- Microphone and camera (for video)

## 🎓 Code Structure

### Socket Event Handlers (`app/call_events.py`)

```python
@socketio.on('initiate_call')  # Start call
@socketio.on('accept_call')    # Accept incoming
@socketio.on('reject_call')    # Reject incoming
@socketio.on('end_call')       # End active call
@socketio.on('webrtc_offer')   # Exchange offer
@socketio.on('webrtc_answer')  # Exchange answer
@socketio.on('webrtc_ice_candidate')  # Exchange ICE
```

### WebRTC Flow

```javascript
1. getUserMedia() → Get local stream
2. RTCPeerConnection() → Create connection
3. addTrack() → Add local tracks
4. createOffer() → Create SDP offer
5. setLocalDescription() → Set local SDP
6. Send offer via Socket.IO
7. Receive answer via Socket.IO
8. setRemoteDescription() → Set remote SDP
9. ontrack event → Receive remote stream
10. onicecandidate → Exchange ICE candidates
```

## ✨ Key Features Summary

✅ **Real-time signaling** - Socket.IO for instant communication
✅ **Peer-to-peer media** - WebRTC for efficient audio/video transfer
✅ **Incoming call notifications** - Modal with ringtone
✅ **Call controls** - Mute, video toggle, end call
✅ **Responsive UI** - Beautiful Tailwind CSS interface
✅ **Error handling** - Permission checks and fallbacks
✅ **Cross-browser support** - Works on all modern browsers
✅ **NAT traversal** - STUN servers for connection establishment

## 🎯 Production Considerations

Before deploying to production:

1. ✅ Add TURN server for better connectivity
2. ✅ Implement call duration tracking
3. ✅ Add call quality monitoring
4. ✅ Set up proper error logging
5. ✅ Add rate limiting for Socket.IO events
6. ✅ Implement reconnection strategies
7. ✅ Add bandwidth adaptation
8. ✅ Consider using a WebRTC gateway (like Janus)
9. ✅ Implement proper authentication for socket events
10. ✅ Add analytics for call metrics
