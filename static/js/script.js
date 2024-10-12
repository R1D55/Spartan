$(document).ready(function () {
    function appendMessage(content, userType = 'bot') {
        let messageHtml = '';
        if (userType === 'user') {
            messageHtml = `<div class="message user-message">
                            <div class="bubble">${content}</div>
                           </div>`;
        } else {
            messageHtml = `<div class="message bot-message">
                            <div class="bubble">${content}</div>
                           </div>`;
        }
        $('#chat-box').append(messageHtml);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    }

    function appendFormattedBotMessage(content) {
        let markdownContent = marked.parse(content);
        let formattedMessage = `<div class="message bot-message">
                                    <div class="bubble">${markdownContent}</div>
                                </div>`;
        $('#chat-box').append(formattedMessage);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    }

    function setLoadingIndicator(isLoading) {
        if (isLoading) {
            $('#chat-box').append('<p class="loading-indicator" id="loading">Bot is typing...</p>');
        } else {
            $('#loading').remove();
        }
    }

    $('#send-button').on('click', function (e) {
        e.preventDefault();
        let userMessage = $('#message').val().trim();
        if (userMessage === '') return;

        appendMessage(userMessage, 'user');
        $('#message').val('');

        setLoadingIndicator(true);

        $.ajax({
            url: '/ask',
            type: 'POST',
            data: { message: userMessage },
            success: function (response) {
                setLoadingIndicator(false);
                appendFormattedBotMessage(response.response);
            },
            error: function () {
                setLoadingIndicator(false);
                appendMessage("Error occurred. Please try again.", 'bot');
            }
        });
    });

    $('#message').on('keypress', function (e) {
        if (e.which == 13) {
            $('#send-button').click();
        }
    });
});