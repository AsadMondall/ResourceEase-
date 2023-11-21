$(document).ready(function() {
    $("#send-btn").on("click", function() {
        var userMessage = $("#user-input").val();
        if (userMessage.trim() !== "") {
            displayUserMessage(userMessage);
            fetchBotResponse(userMessage);
            $("#user-input").val("");
        }
    });

    function displayUserMessage(message) {
        var messageHTML = '<div class="message user-message">' + message + '</div>';
        $("#chat-messages").append(messageHTML);
    }

    function displayBotMessage(message) {
        var messageHTML = '<div class="message bot-message">' + message + '</div>';
        $("#chat-messages").append(messageHTML);
    }

    function fetchBotResponse(userMessage) {
        $.ajax({
            url: '/get_bot_response/',
            type: 'POST',
            data: {
                'message': userMessage,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                displayBotMessage(data.response);
            }
        });
    }
});
