from random import randint
from typing import Optional
from requests import Session
    
class VkUser:
    def __init__(
            self,
            access_token: str,
            api_version: str = "5.131",
            group_id: Optional[int] = None,
            is_user: bool = True) -> None:
        self.api = "https://api.vk.com/method"
        self.is_user = is_user
        self.group_id = group_id
        self.session = Session()
        self.session.headers = {
            "User-Agent": "VKAndroidApp/6.2-5091 (Android 9; SDK 28; samsungexynos7870; samsung j6lte; 720x1450)"
        }
        self.session.params = {
            "access_token": access_token,
            "v": api_version,
        }
        self.user_id = self.get_profile_info()["response"]["id"]
        self.get_long_poll_server()

    def filter(self, data: dict) -> dict:
        return {key: value for key, value in data.items() if value is not None}

    def _post(self, method: str, **data) -> dict:
        data = self.filter(data)
        return self.session.post(f"{self.api}/{method}", data=data).json()

    def get_long_poll_server(self) -> dict:
        if self.is_user:
            response = self._post(
                "messages.getLongPollServer", need_pts=1, lp_version=3)["response"]
        else:
            response = self._post(
                "groups.getLongPollServer", group_id=self.group_id)["response"]
        self.ts = response["ts"]
        self.key = response["key"]
        self.server = response["server"]
        return response

    def listen(self) -> dict:
        if self.is_user:
            url = (
                f"https://{self.server}"
                f"?act=a_check&key={self.key}&ts={self.ts}&wait=25&mode=2&version=3"
            )
            response = self.session.get(url).json()
            self.ts = response["ts"]
            if not response["updates"]:
                return {"type": "empty"}

            update = response["updates"][0]
            if update[0] == 4:
                return {
                    "type": "message_new",
                    "peer_id": update[3],
                    "content": update[5],
                    "from_id": update[6].get("from"),
                }
            return {"type": "unknown", "c": response["updates"]}
        url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        response = self.session.get(url).json()
        try:
            self.ts = response["ts"]
        except KeyError:
            return response
        if not response["updates"]:
            return {"type": "empty"}
        return response["updates"][0]

    def get_profile_info(self) -> dict:
        return self._post("account.getProfileInfo")

    def get_user_info(self, user_id: int) -> dict:
        return self._post("account.getInfo", user_id=user_id)

    def get_app_permissions(self) -> dict:
        return self._post("account.getAppPermissions")

    def set_online_status(self) -> dict:
        return self._post("account.setOnline")

    def set_offline_status(self) -> dict:
        return self._post("account.setOffline")

    def ban_user(self, owner_id: int) -> dict:
        return self._post("account.ban", owner_id=owner_id)

    def unban_user(self, owner_id: int) -> dict:
        return self._post("account.unban", owner_id=owner_id)

    def get_banned_users(
            self, offset: int = 0, count: int = 100) -> dict:
        return self._post(
            "account.getBanned", offset=offset, count=count)

    def get_users_list(
            self,
            user_ids: str = "1, 2",
            fields: Optional[str] = None) -> dict:
        return self._post("users.get", user_ids=user_ids, fields=fields)

    def get_user_followers(
            self,
            user_id: int,
            offset: int = 0,
            count: int = 100) -> dict:
        return self._post(
            "users.getFollowers",
            user_id=user_id,
            offset=offset,
            count=count)

    def get_user_subscriptions(
            self,
            user_id: int,
            offset: int = 0,
            count: int = 1000,) -> dict:
        return self._post(
            "users.getSubscriptions",
            user_id=user_id,
            offset=offset,
            count=count)

    def report_user(
            self,
            user_id: int,
            report_type: str = "spam",
            comment: Optional[str] = None) -> dict:
        return self._post(
            "users.report",
            user_id=user_id,
            type=report_type,
            comment=comment)

    def get_user_gifts(self, user_id: int) -> dict:
        return self._post("gifts.get", user_id=user_id)

    def get_user_status(self, user_id: int) -> dict:
        return self._post("status.get", user_id=user_id)

    def set_status(self, text: str) -> dict:
        return self._post("status.set", text=text)

    def like(
            self,
            like_type: str = "post",
            owner_id: int = 1,
            item_id: int = 1) -> dict:
        return self._post(
            "likes.add",
            type=like_type,
            owner_id=owner_id, 
            item_id=item_id)

    def dislike(
            self,
            like_type: str = "post",
            owner_id: int = 1,
            item_id: int = 1) -> dict:
        return self._post(
            "likes.delete", 
            type=like_type,
            owner_id=owner_id, 
            item_id=item_id)

    def get_likes_list(
            self,
            like_type: str = "post",
            owner_id: int = 1,
            item_id: int = 1) -> dict:
        return self._post(
            "likes.getList",
            type=like_type,
            owner_id=owner_id,
            item_id=item_id)

    def get_user_wall(
            self,
            owner_id: int,
            offset: int = 0,
            count: int = 100) -> dict:
        return self._post(
            "wall.get",
            owner_id=owner_id,
            offset=offset,
            count=count)

    def delete_post_from_wall(self, post_id: int) -> dict:
        return self._post(
            "wall.delete", post_id=post_id, owner_id=self.user_id)

    def pin_post_in_wall(self, post_id: int) -> dict:
        return self._post(
            "wall.pin", post_id=post_id, owner_id=self.user_id)

    def get_post_comments(
            self,
            post_id: int = 1,
            owner_id: int = 1,
            offset: int = 0,
            count: int = 100) -> dict:
        return self._post(
            "wall.getComments",
            post_id=post_id,
            owner_id=owner_id,
            offset=offset,
            count=count)

    def comment(self, message: str, post_id: int = 1, owner_id: int = 1) -> dict:
        return self._post(
            "wall.createComment",
            message=message,
            post_id=post_id,
            owner_id=owner_id)

    def delete_comment(self, comment_id: int = 1, owner_id: int = 1) -> dict:
        return self._post(
            "wall.deleteComment",
            comment_id=comment_id,
            owner_id=owner_id)

    def close_post_comments(self, post_id: int) -> dict:
        return self._post(
            "wall.closeComments",
            post_id=post_id,
            owner_id=self.user_id)

    def open_post_comments(self, post_id: int) -> dict:
        return self._post(
            "wall.openComments",
            post_id=post_id,
            owner_id=self.user_id)

    def get_conversations(
            self,
            offset: int = 0,
            count: int = 10) -> dict:
        return self._post(
            "messages.getConversations", offset=offset, count=count)

    def get_message_history(self, peer_id: int) -> dict:
        return self._post("messages.getHistory", peer_id=peer_id)

    def get_message_history_attachments(self, peer_id: int) -> dict:
        return self._post(
            "messages.getHistoryAttachments", peer_id=peer_id)

    def get_important_messages(self, count: int = 100) -> dict:
        return self._post(
            "messages.getImportantMessages", count=count)

    def get_user_last_activity(self, user_id: int) -> dict:
        return self._post("messages.getLastActivity", user_id=user_id)

    def send_message(self, peer_id: int, message: str) -> dict:
        data = {
            "message": message,
            "random_id": randint(0, 2**31)
        }
        if peer_id < 2_000_000_000:
            data["user_id"] = peer_id
        else:
            data["peer_id"] = peer_id
        return self._post("messages.send", **data)

    def edit_message(
            self,
            peer_id: int,
            message: str,
            message_id: int) -> dict:
        return self._post(
            "messages.edit",
            peer_id=peer_id,
            message=message,
            message_id=message_id
        )

    def delete_message(
            self,
            message_ids: str = "1, 2",
            delete_for_all: int = 1) -> dict:
        return self._post(
            "messages.delete",
            message_id=message_ids,
            delete_for_all=delete_for_all)

    def pin_message(
            self, peer_id: int, message_id: int) -> dict:
        return self._post(
            "messages.pin", peer_id=peer_id, message_id=message_id)

    def send_typing(self, peer_id: int) -> dict:
        return self._post("messages.setActivity", peer_id=peer_id)

    def create_chat(self, title: str, user_ids: str = "1, 2, 3") -> dict:
        return self._post(
            "messages.createChat", user_ids=user_ids, title=title)

    def get_chat_info(self, chat_id: int) -> dict:
        return self._post("messages.getChat", chat_id=chat_id)

    def get_chat_preview(self, peer_id: int) -> dict:
        return self._post("messages.getChatPreview", peer_id=peer_id)

    def edit_chat(
            self, chat_id: int, title: str = None) -> dict:
        return self._post(
            "messages.editChat", chat_id=chat_id, title=title)

    def delete_chat_photo(self, chat_id: int) -> dict:
        return self._post("messages.deleteChatPhoto", chat_id=chat_id)

    def add_chat_user(
            self,
            chat_id: int,
            user_id: int,
            visible_messages_count: int = 3) -> dict:
        return self._post(
            "messages.addChatUser",
            chat_id=chat_id,
            user_id=user_id,
            visible_messages_count=visible_messages_count,
        )

    def remove_chat_user(
            self, chat_id: int, user_id: int) -> dict:
        return self._post(
            "messages.removeChatUser",
            chat_id=chat_id,
            user_id=user_id)

    def get_conversation_members(self, peer_id: int) -> dict:
        return self._post(
            "messages.getConversationMembers",
            peer_id=peer_id)

    def get_invite_link(
            self, peer_id: int, reset: int = 0) -> dict:
        return self._post(
            "messages.getInviteLink",
            peer_id=peer_id,
            reset=reset)

    def join_chat_by_invite_link(self, link: str) -> dict:
        return self._post("messages.joinChatByInviteLink", link=link)
