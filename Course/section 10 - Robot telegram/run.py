import asyncio
from robot_telegram import TelegramBot

if __name__ == '__main__':
    obj_telegram = TelegramBot()
    print("Starting the robot...")
    print("Chose the group target: ")
    target_group = obj_telegram.get_my_groups()
    members = obj_telegram.get_members(target_group)
    print(dir(members))
    print(f"MEMBERS: {members}")
    # print(f"{len(members)} members found in group")

    print("Chose group for add new members")
    my_group = obj_telegram.get_my_groups()

    for member in members:
        add_user = obj_telegram.add_member_to_group(member, my_group)
        if add_user:
            print(f"Member {member.id} added with success.")
            break
