import requests

class VkUser:
	def __init__(
			self,
			access_token: str = None,
			api_version: str = "5.131",
			group_id: int = None,
			type: bool = True) -> None:
		self.api = "https://api.vk.com/method"
		self.session = requests.Session()
		self.session.headers = {
			"User-Agent": "VKAndroidApp/6.2-5091 (Android 9; SDK 28; samsungexynos7870; samsung j6lte; 720x1450)"
		}
		self.type = type
		self.group_id = group_id
		self.api_version = api_version
		if access_token:
			self.access_token = access_token
			self.user_id = self.get_profile_info()["response"]["id"]
		self.get_long_poll_server()

	def get_long_poll_server(self) -> dict:
		url = f"{self.api}/groups.getLongPollServer?access_token={self.access_token}&v={self.api_version}&group_id={self.group_id}"
		if self.type:
			url = f"{self.api}/messages.getLongPollServer?access_token={self.access_token}&v={self.api_version}&need_pts=1&lp_version=3"
		response = self.session.get(url).json()["response"]
		self.ts = response["ts"]
		self.key = response["key"]
		self.server = response["server"]
		return response

	def set_online_status(self) -> dict:
		return self.session.post(
			f"{self.api}/account.setOnline?access_token={self.access_token}&v={self.api_version}").json()

	def set_offline_status(self) -> dict:
		return self.session.post(
			f"{self.api}/account.setOffline?access_token={self.access_token}&v={self.api_version}").json()

	def get_profile_info(self) -> dict:
		return self.session.post(
			f"{self.api}/account.getProfileInfo?access_token={self.access_token}&v={self.api_version}").json()

	def get_user_info(self, user_id: int) -> dict:
		data = {
			"user_id": user_id
		}
		return self.session.post(
			f"{self.api}/account.getInfo?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def ban_user(self, owner_id: int) -> dict:
		data = {
			"owner_id": owner_id
		}
		return self.session.post(
			f"{self.api}/account.ban?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def unban_user(self, owner_id: int) -> dict:
		data = {
			"owner_id": owner_id
		}
		return self.session.post(
			f"{self.api}/account.unban?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_banned_users(
			self,
			offset: int = 0,
			count: int = 100) -> dict:
		data = {
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/account.getBanned?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_app_permissions(self) -> dict:
		return self.session.post(
			f"{self.api}/account.getAppPermissions?access_token={self.access_token}&v={self.api_version}").json()

	def get_user_gifts(self, user_id: int) -> dict:
		data = {
			"user_id": user_id
		}
		return self.session.post(
			f"{self.api}/gifts.get?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def like(
			self,
			type: str = "post",
			owner_id: int = 1,
			item_id: int = 1) -> dict:
		data = {
			"type": type,
			"owner_id": owner_id,
			"item_id": item_id
		}
		return self.session.post(
			f"{self.api}/likes.add?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def dislike(
			self,
			type: str = "post",
			owner_id: int = 1,
			item_id: int = 1) -> dict:
		data = {
			"type": type,
			"owner_id": owner_id,
			"item_id": item_id
		}
		return self.session.post(
			f"{self.api}/likes.delete?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_likes_list(
			self,
			type: str = "post",
			owner_id: int = 1,
			item_id: int = 1) -> dict:
		data = {
			"type": type,
			"owner_id": owner_id,
			"item_id": item_id
		}
		return self.session.post(
			f"{self.api}/likes.getList?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def close_post_comments(self, post_id: int) -> dict:
		data = {
			"post_id": post_id,
			"owner_id": self.user_id
		}
		return self.session.post(
			f"{self.api}/wall.closeComments?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def open_post_comments(self, post_id: int) -> dict:
		data = {
			"post_id": post_id,
			"owner_id": self.user_id
		}
		return self.session.post(
			f"{self.api}/wall.openComments?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def comment(
			self,
			message: str,
			post_id: int = 1,
			owner_id: int = 1) -> dict:
		data = {
			"message": message,
			"post_id": post_id,
			"owner_id": owner_id
		}
		return self.session.post(
			f"{self.api}/wall.createComment?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def delete_comment(
			self,
			comment_id: int = 1,
			owner_id: int = 1) -> dict:
		data = {
			"comment_id": comment_id,
			"owner_id": owner_id
		}
		return self.session.post(
			f"{self.api}/wall.deleteComment?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def delete_post_from_wall(self, post_id: int) -> dict:
		data = {
			"post_id": post_id,
			"owner_id": self.user_id
		}
		return self.session.post(
			f"{self.api}/wall.delete?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_user_wall(
			self,
			owner_id: int,
			offset: int = 0,
			count: int = 100) -> dict:
		data = {
			"owner_id": owner_id,
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/wall.get?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def pin_post_in_wall(self, post_id: int) -> dict:
		data = {
			"post_id": post_id,
			"owner_id": self.user_id
		}
		return self.session.post(
			f"{self.api}/wall.pin?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_post_comments(
			self,
			post_id: int = 1,
			owner_id: int = 1,
			offset: int = 0,
			count: int = 100) -> dict:
		data = {
			"post_id": post_id,
			"owner_id": owner_id,
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/wall.getComments?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_users_list(
			self,
			user_ids: str = "1, 2",
			fields: str = None) -> dict:
		data = {
			"user_ids": user_ids,
			"fields": fields
		}
		return self.session.post(
			f"{self.api}/users.get?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_user_followers(
			self,
			user_id: int,
			offset: int = 0,
			count: int = 100) -> dict:
		data = {
			"user_id": user_id,
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/users.getFollowers?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_user_subscriptions(
			self,
			user_id: int,
			offset: int = 0,
			count: int = 1000) -> dict:
		data = {
			"user_id": user_id,
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/users.getSubscriptions?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def report_user(
			self,
			user_id: int,
			type: str = "spam",
			comment: str = None) -> dict:
		data = {
			"user_id": user_id,
			"type": type,
			"comment": comment
		}
		return self.session.post(
			f"{self.api}/users.report?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_user_status(self, user_id: int) -> dict:
		data = {
			"user_id": user_id
		}
		return self.session.post(
			f"{self.api}/status.get?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def set_status(self, text: str) -> dict:
		data = {
			"text": text
		}
		return self.session.post(
			f"{self.api}/status.set?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_conversations(
			self,
			offset: int = 0,
			count: int = 10) -> dict:
		data = {
			"offset": offset,
			"count": count
		}
		return self.session.post(
			f"{self.api}/messages.getConversations?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def create_chat(
			self,
			title: str,
			user_ids: str = "1, 2, 3") -> dict:
		data = {
			"user_ids": user_ids,
			"title": title
		}
		return self.session.post(
			f"{self.api}/messages.createChat?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_message_history(self, peer_id: int) -> dict:
		data = {
			"peer_id": peer_id
		}
		return self.session.post(
			f"{self.api}/messages.getHistory?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_message_history_attachments(self, peer_id: int) -> dict:
		data = {
			"peer_id": peer_id
		}
		return self.session.post(
			f"{self.api}/messages.getHistoryAttachments?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_important_messages(self, count: int = 100) -> dict:
		data = {"count": count}
		return self.session.post(
			f"{self.api}/messages.getImportantMessages?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def send_typing(self, peer_id: int) -> dict:
		data = {
			"peer_id": peer_id
		}
		return self.session.post(
			f"{self.api}/messages.setActivity?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_user_last_activity(self, user_id: int) -> dict:
		data = {
			"user_id": user_id
		}
		return self.session.post(
			f"{self.api}/messages.getLastActivity?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def join_chat_by_invite_link(self, link: str) -> dict:
		data = {
			"link": link
		}
		return self.session.post(
			f"{self.api}/messages.joinChatByInviteLink?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_chat_info(self, chat_id: int) -> dict:
		data = {
			"chat_id": chat_id
		}
		return self.session.post(
			f"{self.api}/messages.getChat?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_conversation_members(self, peer_id: int) -> dict:
		data = {
			"peer_id": peer_id
		}
		return self.session.post(
			f"{self.api}/messages.getConversationMembers?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def edit_chat(
			self,
			chat_id: int,
			title: str = None) -> dict:
		data = {
			"chat_id": chat_id,
			"title": title
		}
		return self.session.post(
			f"{self.api}/messages.editChat?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_invite_link(
			self,
			peer_id: int,
			responseet: int = 0) -> dict:
		data = {
			"peer_id": peer_id,
			"responseet": responseet
		}
		return self.session.post(
			f"{self.api}/messages.getInviteLink?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def add_chat_user(
			self, 
			chat_id: int,
			user_id: int,
			visible_messages_count: int = 3) -> dict:
		data = {
			"chat_id": chat_id, 
			"user_id": user_id,
			"visible_messages_count": visible_messages_count
		}
		return self.session.post(
			f"{self.api}/messages.addChatUser?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def get_chat_preview(self, peer_id: int) -> dict:
		data = {
			"peer_id": peer_id
		}
		return self.session.post(
			f"{self.api}/messages.getChatPreview?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def delete_chat_photo(self, chat_id: int) -> dict:
		data = {
			"chat_id": chat_id
		}
		return self.session.post(
			f"{self.api}/messages.deleteChatPhoto?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def delete_message(
			self,
			message_ids: str = "1, 2",
			delete_for_all: int = 1) -> dict:
		data = {
			"message_id": message_ids,
			"delete_for_all": delete_for_all
		}
		return self.session.post(
			f"{self.api}/messages.delete?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def pin_message(
			self,
			peer_id: int,
			message_id: int) -> dict:
		data = {
			"peer_id": peer_id,
			"message_id": message_id
		}
		return self.session.post(
			f"{self.api}/messages.pin?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def send_message(
			self,
			peer_id: int,
			message: str) -> dict:
		data = {
			"message": message
		}
		if peer_id < 2000000000:
			data["user_id"] = peer_id
		else:
			data["peer_id"] = peer_id
		return self.session.post(
			f"{self.api}/messages.send?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def edit_message(
			self,
			peer_id: int,
			message: str,
			message_id: int) -> dict:
		data = {
			"peer_id": peer_id,
			"message": message,
			"message_id": message_id
		}
		return self.session.post(
			f"{self.api}/messages.edit?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def remove_chat_user(
			self,
			chat_id: int,
			user_id: int) -> dict:
		data = {
			"chat_id": chat_id,
			"user_id": user_id
		}
		return self.session.post(
			f"{self.api}/messages.removeChatUser?access_token={self.access_token}&v={self.api_version}",
			data=data).json()

	def listen(self) -> dict:
		url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
		if self.type:
			url = f"https://{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25&mode=2&version=3"
			response = self.session.get(url).json()
			self.ts = response["ts"]
			if len(response["updates"]) == 0:
				return {"type": "empty"}
			elif response["updates"][0][0] == 4:
				data = {
					"type": "message_new",
					"peer_id": response["updates"][0][3],
					"content": response["updates"][0][5],
					"from_id": response["updates"][0][6]["from"] if "from" in response["updates"][0][6] else None
				}
			else:
				data = {
					"type": "unknown",
					"c": response["updates"]
				}
		response = self.session.get(url).json()
		try:
			self.ts = response["ts"]
		except:
			return response
		if len(response["updates"]) == 0:
			return {"type": "empty"}
		else:
			data = response["updates"][0]
		return data
