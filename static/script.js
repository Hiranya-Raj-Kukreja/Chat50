document.addEventListener("DOMContentLoaded", function() {
    function loadFriendRequests() {
        var container = document.getElementById("friendRequestsContainer");

        if (container) {
            fetch("/showRequests")
                .then(response => response.text())
                .then(data => {
                    container.innerHTML = data;

                    const acceptButtons = document.querySelectorAll('.acceptButton');
                    const rejectButtons = document.querySelectorAll('.rejectButton');

                    acceptButtons.forEach(function(button) {
                        button.addEventListener('click', function() {
                            updateStatus(button);
                        });
                    });

                    rejectButtons.forEach(function(button) {
                        button.addEventListener('click', function() {
                            updateStatus(button);
                        });
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        const messageForms = document.querySelectorAll('.message-form');

        messageForms.forEach(function(form) {
            form.addEventListener('click', function() {
                submitForm(form);
            });
        });

        function submitForm(form) {
            const friendIdInput = form.querySelector('input[name="friend_id"]');
            const friendId = friendIdInput.value;
            form.submit();
        }
    }

    setInterval(loadFriendRequests, 30000);
    loadFriendRequests();

    const acceptButtons = document.querySelectorAll('.acceptButton');
    const rejectButtons = document.querySelectorAll('.rejectButton');

    function updateStatus(button) {
        const friendRequestDiv = button.closest('.friendRequest');
        const buttons = friendRequestDiv.querySelectorAll('button');
    }

    acceptButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            updateStatus(button);
        });
    });

    rejectButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            updateStatus(button);
        });
    });

    const new_chat = document.querySelector('.new_chat');
    if (new_chat) {
        new_chat.addEventListener('click', function() {
            document.querySelector('.chat-input-tag').focus();
        });
    }

    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keydown', function(event) {
            if (event.keyCode === 13 && !event.shiftKey) {
                event.preventDefault();
                document.getElementById('chatForm').submit();
            }
        });
    }

    var chatsContainer = document.getElementById('chatsContainer');
    if (chatsContainer) {
        chatsContainer.scrollTop = chatsContainer.scrollHeight;
        chatsContainer.scrollTo({
            top: chatsContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    var chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', function() {
            chatsContainer.scrollTop = chatsContainer.scrollHeight;
        });
    }

    const submitMessageInput = document.getElementById('submitMessageInput');
    if (submitMessageInput) {
        document.getElementById('submitMessageInput').addEventListener('click', function(event) {
            document.getElementById('chatForm').submit();
        });
    }

    const friendListContainer = document.getElementById('friendListContainer');

    const originalContentMap = new Map();

    const friends = friendListContainer.getElementsByClassName('message-container');
    Array.from(friends).forEach(friend => {
        const friendNameElement = friend.querySelector('.contact-name');
        originalContentMap.set(friend, friendNameElement.innerText.trim().toLowerCase());
    });

    document.getElementById('searchInput').addEventListener('input', function(event) {
        const query = event.target.value.trim().toLowerCase();
        const friends = Array.from(friendListContainer.getElementsByClassName('message-container'));

        friends.sort((a, b) => {
            const nameA = originalContentMap.get(a);
            const nameB = originalContentMap.get(b);
            return nameA.localeCompare(nameB);
        });

        const visibleFriends = friends.filter(friend => {
            const friendNameElement = friend.querySelector('.contact-name');
            const originalContent = originalContentMap.get(friend);

            const nameMatch = originalContent.includes(query);

            const isVisible = query === '' || nameMatch;
            friend.classList.toggle('hide', !isVisible);

            if (isVisible) {
                highlightSearchResult(friendNameElement, query);
            }

            return isVisible;
        });

        visibleFriends.forEach(friend => {
            friendListContainer.prepend(friend);
        });
    });

    function highlightSearchResult(element, query) {
        const regex = new RegExp(`(${query})`, 'ig');
        element.innerHTML = element.textContent.replace(regex, '<span class="highlight">$1</span>');
    }
});
