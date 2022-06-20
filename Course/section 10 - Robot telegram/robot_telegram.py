from config import api_id, api_hash, phone, username
import time
import asyncio

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError


class TelegramBot:
    def __init__(self):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.username = username
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        # self.connect()

    async def connect(self):
        await self.client.connect()
        if not self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            await self.client.sign_in(self.phone, input("Enter the code: "))
        return True

    async def get_my_groups(self):
        groups = []
        chats = await self.client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=200,
            hash=0)
        )

        for chat in chats.chats:
            print(chat)
            """
            Example chats return:
            Channel(id=1449813584, title='rCryptoCurrency', photo=ChatPhoto(photo_id=4958538356413803081, dc_id=1, 
            has_video=True, stripped_thumb=b'\\x01\\x08\\x08\\xd3\\xfd\\xe7\\x9d\\xdbe\\x14QL7?'), 
            date=datetime.datetime(2022, 6, 18, 9, 41, 21, tzinfo=datetime.timezone.utc), creator=False, left=False, 
            broadcast=False, verified=False, megagroup=True, restricted=False, signatures=False, min=False, scam=False, 
            has_link=True, has_geo=False, slowmode_enabled=False, call_active=False, call_not_empty=False, 
            fake=False, gigagroup=False, access_hash=5301131764771494573, username='rCryptoCurrencyOfficial', 
            restriction_reason=[], admin_rights=None, banned_rights=None, default_banned_rights=ChatBannedRights(
            until_date=datetime.datetime(2038, 1, 19, 3, 14, 7, tzinfo=datetime.timezone.utc), view_messages=False, 
            send_messages=False, send_media=False, send_stickers=False, send_gifs=False, send_games=False, 
            send_inline=False, embed_links=True, send_polls=True, change_info=True, invite_users=True, 
            pin_messages=True), participants_count=1364)"}
            """
            try:
                if chat.megagroup is True and chat.restricted is False:
                    groups.append(chat)
            except:
                continue

        print("Chose a group")
        i = 0
        # print(len(groups))
        for group in groups:
            print(f"{str(i)} - {group.title} - Participants: {group.participants_count}")
            i += 1

        chose = input("Enter a number: ")
        group_target = groups[int(chose)]
        return group_target

    async def get_members(self, target_group):
        users = []

        all_participantes = await self.client.get_participants(target_group, aggressive=True)
        print(dir(all_participantes))
        # print(len(all_participantes))

        for user in all_participantes:
            print(user)

        return all_participantes

    async def add_member_to_group(self, user, target_group):
        target_group_entity = await InputPeerChannel(target_group.id, target_group.access_hash)

        try:
            print(f"Adding user {user.id}")
            user_to_add = InputPeerUser(user.id, user.access_hash)

            await self.client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            time.sleep(2)

            return True

        except PeerFloodError:
            print("Error of Flood. Sleeping for 5minutes")
            time.sleep(300)
            return False

        except UserPrivacyRestrictedError:
            print("User don't permission adding in a group.")
            return False

        except Exception as e:
            print(e)
            return False

        # https://t.me/coinsnipernet
        with self.client:
            self.client.loop.run_until_complete(info_groups(phone))
