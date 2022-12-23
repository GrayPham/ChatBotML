class InteractiveChatbox {
    constructor(a, b, c) {
      this.args = {
        button: a,
        chatbox: b,
      };
      this.icons = c;
      this.state = false;
    }
  
    display() {
      const { button, chatbox } = this.args;
  
      button.addEventListener("click", () => this.toggleState(chatbox));
    }
  
    toggleState(chatbox) {
      this.state = !this.state;
      this.showOrHideChatBox(chatbox, this.args.button);
    }
  
    showOrHideChatBox(chatbox, button) {
      if (this.state) {
        chatbox.classList.add("chatbox--active");
        this.toggleIcon(true, button);
      } else if (!this.state) {
        chatbox.classList.remove("chatbox--active");
        this.toggleIcon(false, button);
      }
    }
  
    toggleIcon(state, button) {
      const { isClicked, isNotClicked } = this.icons;
      let b = button.children[0].innerHTML;
  
      if (state) {
        button.children[0].innerHTML = isClicked;
      } else if (!state) {
        button.children[0].innerHTML = isNotClicked;
      }
    }
  }
  
  const chatButton = document.querySelector(".chatbox__button");
  const chatContent = document.querySelector(".chatbox__support");
  const icons = {
    isClicked:
      '<img src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/chatbox-icon.svg" />',
    isNotClicked:
      '<img src="https://cdn.jsdelivr.net/gh/thienan01/ChatCDNs/chatbox-icon.svg" />',
  };
  const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
  chatbox.display();
  chatbox.toggleIcon(false, chatButton);
  
  const handleSendMsg = () => {
    let senderHTML = `<div class="messages__item messages__item--operator">Content</div>`;
    let receiverHTML = `<div class="messages__item messages__item--visitor">Content</div>`;
    let msg = $("#inputMessage").val();
    senderHTML = senderHTML.replace("Content", msg);
    $(".chatbox__messages").prepend(senderHTML);
    $("#inputMessage").val("");
    let request = {
        securitykey: securitykey,
        botID: botID,
        userID: userID,
        message: msg,
        firstCheck : true,
    };
  
    $.ajax({
      url: "http://127.0.0.1:8000/api/mess/sentmessagesBuy",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(request),
      success: function (result) {
        console.log(JSON.stringify(result));
        if (result.status === true) {
            if (result.message != null && result.message.trim() != "") {
                firstCheck = result.First
              receiverHTML = result.message;
              console.log(receiverHTML);
              $(".chatbox__messages").prepend(receiverHTML);
            }

        }
        return result;
      },
      error: function (error) {
        console.log(error);
      },
    });
  };
  handleSendMsg();
