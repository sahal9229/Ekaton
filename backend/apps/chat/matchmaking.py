from apps.chat.models import PrivateChatRoom
from apps.chat.services import create_private_chat_room
from apps.users.models import User
from core.redis import redis_client
from django.db.models import Q


def add_user_to_queue(user):
    """Add a user to the anonymous chat waiting queue."""
    redis_client.rpush("waiting_users", str(user.id))


def get_waiting_user():
    """Get the next waiting user from the queue."""
    user_id = redis_client.lpop("waiting_users")

    if not user_id:
        return None

    return User.objects.filter(id=user_id).first()


def get_active_chat_room(user):
    """Return the user's active chat room."""

    return (
        PrivateChatRoom.objects.filter(
            status=PrivateChatRoom.Status.ACTIVE,
        )
        .filter(Q(user_one=user) | Q(user_two=user))
        .first()
    )


def remove_user_from_queue(user):
    """Remove a user from the waiting queue."""

    redis_client.lrem("waiting_users", 0, str(user.id))


def is_user_waiting(user):
    """Check whether the user is already waiting."""

    waiting_users = redis_client.lrange(
        "waiting_users",
        0,
        -1,
    )

    return str(user.id) in waiting_users


def queue_size():
    """Return the number of users waiting."""

    return redis_client.llen("waiting_users")


def is_user_in_active_chat(user):
    """Check whether the user is already in an active private chat."""

    return (
        PrivateChatRoom.objects.filter(
            status=PrivateChatRoom.Status.ACTIVE,
        )
        .filter(Q(user_one=user) | Q(user_two=user))
        .exists()
    )


def start_chat(user):
    """Start anonymous chat matchmaking."""

    active_room = get_active_chat_room(user)

    if active_room:
        return {
            "status": "active",
            "message": "You are already in an active chat.",
            "room_id": str(active_room.id),
        }

    if is_user_waiting(user):
        return {
            "status": "waiting",
            "message": "You are already waiting for a match.",
        }

    waiting_user = get_waiting_user()

    if waiting_user is None:
        add_user_to_queue(user)

        return {
            "status": "waiting",
            "message": "Waiting for another user...",
        }

    if waiting_user.id == user.id:
        add_user_to_queue(user)

        return {
            "status": "waiting",
            "message": "Waiting for another user...",
        }

    room = create_private_chat_room(
        user_one=waiting_user,
        user_two=user,
    )

    return {
        "status": "matched",
        "message": "Match found.",
        "room_id": str(room.id),
    }
