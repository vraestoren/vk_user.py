# <img src="https://vk.com/images/icons/pwa/apple/default.png?15" width="28" style="vertical-align:middle;" /> vk_user.py

> VK API wrapper for [VKontakte](https://vk.com) — supports both user and group (bot) accounts with long poll event listening.

## Quick Start
```python
from vk_user import VkUser

# User account
vk = VkUser(access_token="your_access_token")

# Group/bot account
vk = VkUser(access_token="your_access_token", group_id=123456789, is_user=False)
```

---

## Constructor Options
```python
VkUser(
    access_token="your_token",  # required
    api_version="5.131",        # VK API version
    group_id=None,              # group ID for bot mode
    is_user=True                # True = user account, False = group/bot
)
```

---

## Long Poll

| Method | Description |
|--------|-------------|
| `get_long_poll_server()` | Initialize long poll session |
| `listen()` | Block and wait for the next update |
```python
while True:
    event = vk.listen()
    if event["type"] == "message_new":
        vk.send_message(event["peer_id"], "Hello!")
```

---

## Account

| Method | Description |
|--------|-------------|
| `get_profile_info()` | Get current user profile |
| `get_user_info(user_id)` | Get account info for a user |
| `get_app_permissions()` | Get app permission flags |
| `set_online_status()` | Set status to online |
| `set_offline_status()` | Set status to offline |
| `ban_user(owner_id)` | Ban a user |
| `unban_user(owner_id)` | Unban a user |
| `get_banned_users(offset, count)` | Get list of banned users |

---

## Users

| Method | Description |
|--------|-------------|
| `get_users_list(user_ids, fields)` | Get info for multiple users |
| `get_user_followers(user_id, offset, count)` | Get user's followers |
| `get_user_subscriptions(user_id, offset, count)` | Get user's subscriptions |
| `report_user(user_id, report_type, comment)` | Report a user |
| `get_user_gifts(user_id)` | Get user's gifts |
| `get_user_status(user_id)` | Get user's status text |
| `set_status(text)` | Set your status text |

---

## Likes

| Method | Description |
|--------|-------------|
| `like(like_type, owner_id, item_id)` | Like a post/photo/etc |
| `dislike(like_type, owner_id, item_id)` | Remove a like |
| `get_likes_list(like_type, owner_id, item_id)` | Get who liked an item |

**Like types:** `post`, `comment`, `photo`, `video`, `note`, `market`

---

## Wall

| Method | Description |
|--------|-------------|
| `get_user_wall(owner_id, offset, count)` | Get posts from a wall |
| `delete_post_from_wall(post_id)` | Delete a post |
| `pin_post_in_wall(post_id)` | Pin a post |
| `get_post_comments(post_id, owner_id, offset, count)` | Get post comments |
| `comment(message, post_id, owner_id)` | Post a comment |
| `delete_comment(comment_id, owner_id)` | Delete a comment |
| `close_post_comments(post_id)` | Disable comments on a post |
| `open_post_comments(post_id)` | Enable comments on a post |

---

## Messages

| Method | Description |
|--------|-------------|
| `get_conversations(offset, count)` | Get conversation list |
| `get_message_history(peer_id)` | Get message history |
| `get_message_history_attachments(peer_id)` | Get attachments from history |
| `get_important_messages(count)` | Get important messages |
| `get_user_last_activity(user_id)` | Get user's last activity time |
| `send_message(peer_id, message)` | Send a message |
| `edit_message(peer_id, message, message_id)` | Edit a sent message |
| `delete_message(message_ids, delete_for_all)` | Delete messages |
| `pin_message(peer_id, message_id)` | Pin a message |
| `send_typing(peer_id)` | Send typing indicator |

---

## Chats

| Method | Description |
|--------|-------------|
| `create_chat(title, user_ids)` | Create a group chat |
| `get_chat_info(chat_id)` | Get chat info |
| `get_chat_preview(peer_id)` | Get chat preview |
| `edit_chat(chat_id, title)` | Rename a chat |
| `delete_chat_photo(chat_id)` | Remove chat photo |
| `add_chat_user(chat_id, user_id, visible_messages_count)` | Add a user to chat |
| `remove_chat_user(chat_id, user_id)` | Remove a user from chat |
| `get_conversation_members(peer_id)` | Get all chat members |
| `get_invite_link(peer_id, reset)` | Get or reset chat invite link |
| `join_chat_by_invite_link(link)` | Join a chat via invite link |
