from django.shortcuts import render
from django.http import JsonResponse
from g4f.client import Client

client = Client()

def chat_view(request):
    return render(request, 'chat/chat.html')

def get_response(request):
    user_message = request.GET.get('message')
    changed_page_response = ""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": r"""answer using html markup but without html, head, and other tags, just a piece of code and without ``` |
                    dont say anything unless answer the question below use js apis if  you should provide the weather, random cat/dog image, the price of crypto 
                   and other currency with coingecko api and so on 
                   use js and beautify it all 
                   DONT FUCKING EVER WRITE ``` just answer with the code without anything that shows it's a code always put js code in script tag
                   use apis without keys with js api provide detailed info and ask the questions that might also help in a way of buttons under each message you answer with the questions that might help the user 
                   and if the user presses them, then the message with the text to get this info is sent to you again in chat, for this I send you the html page where you are showing everything, always style everything including buttons and so  you are allowed to change everything on the page with js depending on what user says or when you think it is ok to change for the user to better get the info:
                   page :
                   ```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat with GPT</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        #chat-box {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            height: 400px;
            overflow-y: auto;
            background-color: #fff;
            margin-bottom: 10px;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 5px;
        }
        .user {
            background-color: #d1e7dd;
            text-align: right;
        }
        .gpt {
            background-color: #f8d7da;
            text-align: left;
        }
        #user-input {
            width: calc(100% - 90px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        #send-button {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        #send-button:hover {
            background-color: #0056b3;
        }
        @media (max-width: 600px) {
            #user-input {
                width: calc(100% - 70px);
            }
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>Chat with GPT</h1>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Type your message here...">
    <button id="send-button"><i class="fas fa-paper-plane"></i> Send</button>

    <script>
        $(document).ready(function() {
            function appendMessage(role, message) {
                const messageClass = role === 'user' ? 'user' : 'gpt';
                $('#chat-box').append(`<div class="message ${messageClass}">${role.charAt(0).toUpperCase() + role.slice(1)}: ${message}</div>`);
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight); // Scroll to the bottom
            }

            $('#send-button').click(function() {
                sendMessage();
            });

            $('#user-input').keypress(function(event) {
                if (event.which === 13) { // Enter key
                    sendMessage();
                    event.preventDefault(); // Prevent form submission
                }
            });

            function sendMessage() {
                const userMessage = $('#user-input').val();
                if (userMessage.trim() === '') return; // Prevent sending empty messages
                appendMessage('user', userMessage);
                $('#user-input').val('');

                $.get('/chat/get_response/', { message: userMessage }, function(data) {
                    appendMessage('gpt', data.response);
                });
            }
        });
    </script>
</body>
</html>

                   ```""" + f"""
                   here is the page after change by you:
                   ```
                   {changed_page_response}
                   ```
                    HERE is the user message: \n""" + user_message}],
        web_search=False
    )
    return JsonResponse({'response': response.choices[0].message.content})
