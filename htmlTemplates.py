css = '''
<style>
.chat-message {
    padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 0.5rem; display: flex
}
.chat-message.user {
    background-color: #B1B1B1
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .message {
  width: 80%;
  padding: 0.5rem;
  color: #ffff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">    
    <div class="message">{{MSG}}</div>
</div>
'''
