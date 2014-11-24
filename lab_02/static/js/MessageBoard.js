var MessageBoard = {

    messages: [],
    textField: null,
    messageArea: null,

    init: function (e) {

        MessageBoard.textField = document.getElementById("inputText");
        MessageBoard.nameField = document.getElementById("inputName");
        MessageBoard.messageArea = document.getElementById("messagearea");
        MessageBoard.csrfToken = document.getElementById("csrf_token");

        // Add eventhandlers
        document.getElementById("inputText").onfocus = function (e) {
            this.className = "focus";
        }
        document.getElementById("inputText").onblur = function (e) {
            this.className = "blur"
        }
        document.getElementById("buttonSend").onclick = function (e) {
            MessageBoard.sendMessage();
            return false;
        }

        MessageBoard.textField.onkeypress = function (e) {
            if (!e) var e = window.event;

            if (e.keyCode == 13 && !e.shiftKey) {
                MessageBoard.sendMessage();

                return false;
            }
        }
        if ("WebSocket" in window) {
            MessageBoard.WebSocket = new WebSocket('ws://localhost:8080');
        }
        MessageBoard.websocket();
    },
    websocket: function() {
        MessageBoard.WebSocket.onopen = function(e) {
            console.log("Connection to websocket established!");
        };

        MessageBoard.WebSocket.onmessage = function(e) {
            MessageBoard.getMessages();
        };
    },
    getMessages: function (timestamp) {
        var self = this;
        var url, obj, queryString;

        url = "index.php?get_messages";

        queryString = {'timestamp' : timestamp};

        $.ajax({
            type: 'GET',
            url: url,
            data: queryString,
            success: function(data){
                obj = jQuery.parseJSON(data);
                MessageBoard.renderMessages(obj.messages);
                if (!"WebSocket" in window) {
                    setTimeout(function() {
                        MessageBoard.getMessages(obj.timestamp);
                    }, 1000);
                }
            }
        });
    },
    sendMessage: function () {
        var self = this;
        var params, jqxhr;

        if (self.textField.value == "") return;

        url = "index.php?add_message";

        params = {
            mess: self.textField.value,
            csrf_token: self.csrfToken.value
        };

        jqxhr = $.post(url, params, function(data) {
            data = $.parseJSON(data);
            if ("WebSocket" in window) {
              MessageBoard.WebSocket.send(MessageBoard.textField.value);
            };
            self.getMessages();
        }).fail(function() {
            console.log("FAILURE SENDING");
        });

    },
    renderMessages: function (data) {
        var self = this;
        var mess, obj, text, mess,
            div, textTag, i;

        // Remove all messages
        MessageBoard.messageArea.innerHTML = "";

        div = document.createElement("div");
        div.className = "message";

        textTag = document.createElement("p");

        i = 0;
        for (mess in data) {
            obj = data[mess];
            text = obj.name + " said:\n" + obj.message;
            mess = new Message(text, new Date(obj.date *1000));
            messageID = self.messages.push(mess) - 1;
            self.renderMessage(messageID);
            i++;
        };

        document.getElementById("nrOfMessages").innerHTML = i;
    },
    renderMessage: function (messageID) {
        // Message div
        var div = document.createElement("div");
        div.className = "message";

        // Clock button
        aTag = document.createElement("a");
        aTag.href = "#";
        aTag.onclick = function () {
            MessageBoard.showTime(messageID);
            return false;
        }

        var imgClock = document.createElement("img");
        imgClock.src = "static/pic/clock.png";
        imgClock.alt = "Show creation time";

        aTag.appendChild(imgClock);
        div.appendChild(aTag);

        // Message text
        var text = document.createElement("p");
        text.innerHTML = MessageBoard.messages[messageID].getHTMLText();
        div.appendChild(text);

        // Time - Should fix on server!
        var spanDate = document.createElement("span");
        spanDate.appendChild(document.createTextNode(MessageBoard.messages[messageID].getDateText()))

        div.appendChild(spanDate);

        var spanClear = document.createElement("span");
        spanClear.className = "clear";

        div.appendChild(spanClear);

        MessageBoard.messageArea.appendChild(div);
    },
    removeMessage: function (messageID) {
        if (window.confirm("Vill du verkligen radera meddelandet?")) {

            MessageBoard.messages.splice(messageID, 1); // Removes the message from the array.

            MessageBoard.renderMessages();
        }
    },
    showTime: function (messageID) {

        var time = MessageBoard.messages[messageID].getDate();

        var showTime = "Created " + time.toLocaleDateString() + " at " + time.toLocaleTimeString();

        alert(showTime);
    }
}

window.onload = MessageBoard.init;