import json


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message == "startcourse":
        return "Course started..."


def update_status(user_id, status):
    with open("users.json", encoding="utf-8") as file:
        users_list = json.load(file)['users']
        for user in users_list:
            if user["id"] == user_id:
                user["status"] = status

        json_data = {
            "users": users_list
        }

    with open("users.json", "w") as file:
        json.dump(json_data, file, indent=4)


# def save_name(name):
#     new_user = {
#         "name": name,
#         "email": None
#     }
#     message = f"Hy {name}, What is your email address?"
#     return f"Hy {name}, What is your email address?"

def save_user(user):
    with open("users.json",encoding="utf-8") as file:
        users_list = json.load(file)['users']

        users_list.append(user)

        json_data = {
            "users": users_list
        }

    with open("users.json", "w") as file:
        json.dump(json_data, file, indent=4)

help_message = """
I understand the following commands:

/start
/signup
/help
/start_course
"""