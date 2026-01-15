# 🔧 Call Feature Debugging & Testing Guide

## ✅ Fixes Applied

### 1. Socket.IO Session Management

- **Problem**: Flask-Login sessions weren't working with Socket.IO
- **Fix**: Added `manage_session=False` to Socket.IO initialization
- **Location**: `app/__init__.py`

### 2. Enhanced Debugging

- **Added**: Comprehensive console logging for all call events
- **Backend Logs**: Shows user connections, call initiations, and message delivery
- **Frontend Logs**: Shows socket events, connection status, and call states

### 3. Authentication Verification

- **Added**: Session verification in socket handlers
- **Added**: User socket mapping with detailed logging

## 🧪 Testing Instructions

### Step 1: Open Browser Console

Open Developer Tools (F12) in your browser and go to the Console tab. You'll see debug messages.

### Step 2: Test Socket Connection

**In User 1's Browser:**

1. Open http://127.0.0.1:5000 and login
2. Go to Messages with User 2
3. Check console - should see:
   ```
   Socket connected: <socket-id>
   Current user ID: 1
   ```

**In User 2's Browser (Incognito/Different Browser):**

1. Open http://127.0.0.1:5000 and login as different user
2. Go to Messages with User 1
3. Check console - should see:
   ```
   Socket connected: <socket-id>
   Current user ID: 2
   ```

### Step 3: Check Server Logs

**In Terminal, you should see:**

```
✅ User 1 (Matthew) connected with socket <socket-id>
Active sockets: {1: '<socket-id>'}

✅ User 2 (Kimberly) connected with socket <socket-id>
Active sockets: {1: '<socket-id>', 2: '<socket-id>'}
```

### Step 4: Initiate Call

**From User 1's Browser:**

1. Click the phone icon (voice) or video icon
2. **Browser Console should show:**
   ```
   Starting voice call to user: 2
   Initiating call - isVideo: false
   Emitting initiate_call event: {receiver_id: 2, call_type: 'voice'}
   Call initiation event sent
   ```

**Server Terminal should show:**

```
📞 INITIATE CALL Event received:
   Data: {'receiver_id': 2, 'call_type': 'voice'}
   Authenticated: True
   Caller: User 1 (Matthew)
   Receiver: User 2
   Call Type: voice
   Active sockets: {1: '<id>', 2: '<id>'}
   Receiver in sockets: True
   ✅ Sending incoming_call to socket <socket-id>
   ✅ Call notification sent to User 2
```

**User 2's Browser Console should show:**

```
Incoming call received! {caller_id: 1, caller_username: 'Matthew', call_type: 'voice'}
Showing incoming call modal for: Matthew
```

**User 2's Screen should show:**

- 📞 Full-screen incoming call modal
- 🔊 Ringtone playing
- Caller name displayed
- Accept/Reject buttons

## 🐛 Troubleshooting

### Issue: "Socket not connected"

**Check:**

1. Is Flask server running? (`python run.py`)
2. Is Socket.IO script loaded? (Check Network tab for socket.io.min.js)
3. Any console errors?

**Solution:**

- Restart server
- Clear browser cache
- Check browser console for errors

### Issue: "User not authenticated" in server logs

**Check:**

1. Are both users logged in?
2. Is Flask session working?

**Solution:**

- Logout and login again
- Check if session cookies are enabled
- Try incognito mode for second user

### Issue: "Receiver not in sockets dict"

**Check Server Logs:**

```
Active sockets: {1: '<id>'}  ← Only one user connected!
```

**This means:**

- User 2 is not on the messages page
- User 2's socket didn't connect
- User 2 needs to navigate to messages page first

**Solution:**

- Ensure User 2 is on the messages page
- Check User 2's console for socket connection
- Reload User 2's page

### Issue: No incoming call modal appears

**Check User 2's Console:**

- Should see "Incoming call received!" message
- If not, socket event wasn't received

**Check:**

1. Server logs show "Call notification sent"?
2. User 2's socket ID matches the one in server's active sockets?
3. Both users on messages page?

## 📊 Debug Checklist

### Before Testing

- [ ] Server running (`python run.py`)
- [ ] No errors in server startup
- [ ] Both users have accounts and are matched

### User 1 (Caller)

- [ ] Logged in successfully
- [ ] On messages page with User 2
- [ ] Console shows "Socket connected"
- [ ] Console shows correct user ID
- [ ] No errors in console

### User 2 (Receiver)

- [ ] Logged in successfully (different browser/incognito)
- [ ] On messages page with User 1
- [ ] Console shows "Socket connected"
- [ ] Console shows correct user ID
- [ ] No errors in console

### Server

- [ ] Shows both users connected
- [ ] Active sockets contains both user IDs
- [ ] No authentication errors

### Initiate Call

- [ ] User 1 clicks phone/video icon
- [ ] User 1 console shows call initiation
- [ ] Server shows "INITIATE CALL Event received"
- [ ] Server shows "Call notification sent"
- [ ] User 2 console shows "Incoming call received"
- [ ] User 2 sees modal
- [ ] User 2 hears ringtone

## 🎯 Expected Behavior

### Successful Call Flow

**1. Connection Phase:**

```
User 1 Opens Page → Socket Connects → Server Logs Connection
User 2 Opens Page → Socket Connects → Server Logs Connection
Server: Active sockets: {1: '<id>', 2: '<id>'}
```

**2. Call Initiation:**

```
User 1 Clicks Call → Browser Requests Media → Socket Emits Event
Server Receives Event → Validates Authentication → Finds Receiver Socket
Server Emits to Receiver → User 2 Receives Event
```

**3. Incoming Call:**

```
User 2 Browser: Modal Appears → Ringtone Plays → Waiting for Action
User 2 Can: Accept (green button) or Reject (red button)
```

**4. Call Connection:**

```
User 2 Accepts → WebRTC Negotiation Starts
Offer/Answer Exchange → ICE Candidates Exchange → Connection Established
Both Users: Audio/Video Streaming → Call Controls Active
```

## 📝 What To Look For

### Good Signs ✅

- "✅ User X connected" in server logs
- "Socket connected" in browser console
- "Incoming call received!" in receiver's console
- Modal appears immediately
- Ringtone plays automatically

### Bad Signs ❌

- "⚠️ Unauthenticated connection" in server
- "❌ User not authenticated" when calling
- "❌ Receiver not connected" in server
- No console messages in receiver browser
- Modal doesn't appear

## 🔍 Live Debugging

### Watch These Logs In Real-Time:

**Terminal (Server):**

```bash
# Watch for these messages:
✅ User connected       ← Good!
Active sockets: {1:..., 2:...}  ← Both users present!
📞 INITIATE CALL Event  ← Call started
✅ Call notification sent  ← Event delivered
```

**Browser Console (User 1):**

```javascript
Socket connected: xyz123
Starting voice call to user: 2
Emitting initiate_call event
```

**Browser Console (User 2):**

```javascript
Socket connected: abc456
Incoming call received!
Showing incoming call modal
```

## 🚀 Success Indicators

When everything works correctly:

1. ✅ Both users connect (see in server logs)
2. ✅ User 1 clicks call button
3. ✅ User 1 sees "Calling..." status
4. ✅ User 2 immediately sees incoming call modal
5. ✅ Ringtone starts playing on User 2's end
6. ✅ User 2 can accept/reject
7. ✅ Accepting connects the call
8. ✅ Both users can communicate

## 💡 Pro Tips

1. **Keep browser consoles open** - Critical for debugging
2. **Watch server terminal** - Shows all socket events
3. **Test in incognito** - Avoids cookie/session conflicts
4. **One step at a time** - Verify each step before proceeding
5. **Check active sockets** - Must show both users before calling

## 🎉 Ready to Test!

1. Start server: `python run.py`
2. Open two browser windows
3. Login as different users
4. Navigate both to messages
5. Check console logs (both browsers)
6. Check server logs (terminal)
7. Click call button
8. Watch the magic happen! 🎊
