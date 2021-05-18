import json
from django.core.paginator import Paginator
from django.core.serializers.python import Serializer
from channels.db import async_to_sync
from django.utils import timezone
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("chatConsumer connection: " + str(self.scope["user"]))
        await self.accept()
        self.room_id = None

    async def disconnect(self, close_code):
        print("chatConsumer disconnection")
        if self.room_id != None:
            await self.leave_room(self.room_id)

    async def receive(self, text_data):
        command = content.get("command", None)
        print("chatConsumer recieve: " + str(command))
        try:
            if command == "send":
                if len(content["message"].lstrip()) != 0:
                    await self.send_room(content["room_id"], content["message"])
                elif command == "join":
                    await self.join_room(content["room"])
                elif command == "leave":
                    await self.leave_room(content["room"])
                elif command == "get_room_chat_messages":
                    room = await get_room_or_error(content['room_id'])
                    payload = await get_room_chat_messages(room, content['page_number'])
                    if payload != None:
                        payload = json.loads(payload)
                        await self.send_messages_payload(payload['messages'], payload['new_page_number'])

    async def send_room(self, room_id, message):
		print("chatConsumer: send_room")
		if self.room_id != None:
			if str(room_id) != str(self.room_id):
				raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
		if not is_authenticated(self.scope["user"]):
            raise ClientError("AUTH_ERROR", "You must be authenticated to chat.")
		else:
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
		
		room = await get_room_or_error(room_id)
		await createRoomChatMessage(room, self.scope["user"], message)

		await self.channel_layer.group_send(
			room.group_name,
			{
			#	"type": "chat.message",
				"username": self.scope["user"].username,
				"user_id": self.scope["user"].id,
				"message": message,
			}
		)

	async def chat_message(self, event):
		print("chatConsumer: chat_message from user #" + str(event["user_id"]))
		timestamp = calculate_timestamp(timezone.now())
		await self.send_json(
			{
				"username": event["username"],
				"user_id": event["user_id"],
				"message": event["message"],
				"natural_timestamp": timestamp,
			},
		)

	async def join_room(self, room_id):
		print("chatConsumer: join_room")
		is_auth = is_authenticated(self.scope["user"])
		try:
			room = await get_room_or_error(room_id)
		except ClientError as e:
			await self.handle_client_error(e)

		if is_auth:
			await connect_user(room, self.scope["user"])

		self.room_id = room.id
		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name,
		)
		await self.send_json({
			"join": str(room.id)
		})


	async def leave_room(self, room_id):
		print("chatConsumer: leave_room")
		is_auth = is_authenticated(self.scope["user"])
		room = await get_room_or_error(room_id)

		if is_auth:
			await disconnect_user(room, self.scope["user"])

		self.room_id = None
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name,
		)

	async def handle_client_error(self, e):
		errorData = {}
		errorData['error'] = e.code
		if e.message:
			errorData['message'] = e.message
			await self.send_json(errorData)
		return

	async def send_messages_payload(self, messages, new_page_number):
		print("chatConsumer: send_messages_payload. ")

		await self.send_json(
			{
				"messages_payload": "messages_payload",
				"messages": messages,
				"new_page_number": new_page_number,
			},
		)

def is_authenticated(user):
	if user.is_authenticated:
		return True
	return False

@database_sync_to_async
def createRoomChatMessage(room, user, message):
    return chatMessage.objects.create(user=user, room=room, body=message)

@database_sync_to_async
def connect_user(room, user):
    return room.connect_user(user)

@database_sync_to_async
def disconnect_user(room, user):
    return room.disconnect_user(user)

@database_sync_to_async
def get_room_or_error(room_id):
	try:
		room = chatRoom.objects.get(pk=room_id)
	except chatRoom.DoesNotExist:
		raise ClientError("ROOM_INVALID", "Invalid room.")
	return room


@database_sync_to_async
def get_room_chat_messages(room, page_number):
	try:
		qs = chatMessage.objects.by_room(room)
		p = Paginator(qs, 20)

		payload = {}
		messages_data = None
		new_page_number = int(page_number)  
		if new_page_number <= p.num_pages:
			new_page_number = new_page_number + 1
			s = LazyRoomChatMessageEncoder()
			payload['messages'] = s.serialize(p.page(page_number).object_list)
		else:
			payload['messages'] = "None"
		payload['new_page_number'] = new_page_number
		return json.dumps(payload)
	except Exception as e:
		print("EXCEPTION: " + str(e))
		return None

class LazyRoomChatMessageEncoder(Serializer):
	def get_dump_object(self, obj):
		dump_object = {}
		dump_object.update({'user_id': str(obj.user.id)})
		dump_object.update({'username': str(obj.user.username)})
		dump_object.update({'message': str(obj.body)}
		dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
		return dump_object
    

    pass
