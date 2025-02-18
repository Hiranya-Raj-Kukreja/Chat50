# Chat50
## This is Chat50
### Made by Hiranya Raj Kukreja

#### Video name is - This is Chat50 (CS50 Final Project):
[Link to Video - This is Chat50 (CS50 Final Project)](https://www.youtube.com/watch?v=Z2Jqe0CbCmU)

#### Description:
Chat50 is a user-friendly text-messaging web app designed for seamless communication. It provides a simple and intuitive platform for connecting with friends, managing friend requests, and exploring new conversations.

### Features and Main Plot:

**User Registration and Login:**
Chat50 offers a straightforward user registration process. New users can easily create an account by providing essential details such as a username, password, and confirmation. For existing users, a quick login process ensures immediate access to the vibrant chatting experience.

**Home Page:**
Upon successful login, users are welcomed to Chat50's web app. The left division elegantly displays the user's profile picture, username, and a settings icon. Hovering over the settings icon reveals a dropdown menu with options like Home, Show Requests, Add Friend, and Log Out.

**Show Requests:**
Clicking on "Show Requests" unveils a list of friend requests, indicating their current status—whether they are sent, accepted, or rejected. For received requests, users can respond directly from this section, simplifying the friend request management process.

**Add Friends:**
The "Add Friends" feature enables users to search for friends by entering their username. If a match is found, a friend request is seamlessly sent. The system intelligently checks for existing requests or established friendships, ensuring a smooth and efficient user experience.

**Chat Interface:**
The heart of Chat50 lies in its main chatting interface. This section includes a search bar for quick contact lookup and a list of contacts displayed below. Contacts are presented with profile pictures, usernames, the time of the last conversation, and the last message sent. The interface dynamically adjusts with a scrollbar if the contact list surpasses the viewport height.

**Left Division:**
Consistency is maintained across various sections with the left division, containing the user's profile picture, a settings icon, and a search section for rapid contact discovery. The contacts list dynamically adjusts with a scrollbar if needed, ensuring a smooth user experience even with an extensive contact list.

**Right Division:**
The right division adapts based on the selected section. In the "Home" setting or by default, it features a pleasant background with the Chat50 logo and creator information. In the "Show Requests" section, it displays a list of friend requests. In the "Add Friends" section, it facilitates friend searches and requests.

### Detailed User Experience:

**Search Functionality:**
The search function allows users to find contacts swiftly. As letters are typed, matching contacts are displayed, with entered letters highlighted in the usernames for clarity.

**Contact List:**
Contacts are presented with profile pictures, usernames, last conversation timestamps, and the last message sent. Unread messages are indicated by a circle with a number, ensuring users do not overlook new messages. The scrollbar dynamically appears to guarantee a smooth experience for users with a long contact list.

**Timestamps:**
Timestamps for conversations are shown in Indian Standard Time (IST) and dynamically adjust based on the recency of the conversation.

**Messages and Unseen Indicators:**
The chat interface displays messages with indicators for sent, reached, and seen statuses. Unseen messages are flagged with a circle indicator, offering users a quick overview of their chat history.

### File Structure:

Chat50
|-- static
| |-- media
| | |-- icons # Folder containing icons
| | |-- profile_pictures # Folder containing profile pictures (DPs)
| | |-- script.js # JavaScript file
| | |-- styles.css # CSS styles file
|-- templates # Folder containing HTML files
|-- app.py # Main application file
|-- chat.db # Database file for Chat50
|-- sample.db # Sample database file
|-- schema.sql # SQL schema file
|-- README.md # readme file

### Design Choices:

- **Minimalistic Design:** The interface embraces a clean and minimalistic design for a clutter-free user experience, contributing to the overall aesthetic appeal of Chat50.
- **User-Friendly Navigation:** Features such as the settings dropdown and intuitive search enhance user navigation, promoting a seamless and enjoyable user experience.
- **Dynamic Timestamps:** The use of dynamic timestamps ensures relevance, displaying time, yesterday, this week's day, or the date based on the recency of the conversation.

### Usage:

To run the Chat50 web app, execute the following command in the terminal:

```bash
flask run
```
This command launches the Flask app, making Chat50 accessible on your local machine.
