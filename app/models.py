from bson import ObjectId

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullName": user["fullName"],
        "email": user["email"]
    }
