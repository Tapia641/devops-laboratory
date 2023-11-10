def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "name": user["name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "department": user["department"],
        "salary": user["salary"]
    }


def users_schema_list(users) -> list:
    return [user_schema(user) for user in users]
