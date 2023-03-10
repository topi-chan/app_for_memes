from enum import Enum


class MemeStatusEnum(str, Enum):
    approved = "approved"
    unapproved = "unapproved"


class RoleEnum(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"
