from typing import List

from django.contrib.auth.models import AnonymousUser
from rest_access_policy import AccessPolicy


class MenuAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list"], "principal": "*", "effect": "allow"},
        {"action": ["user_menu"], "principal": "*", "effect": "allow"},
        # {"action": ["destroy"], "principal": ["*"], "effect": "allow", "condition": "is_author"},
        # {"action": ["*"], "principal": ["*"], "effect": "deny", "condition": "is_happy_hour"},
    ]

    def is_admin(self, request, view, action) -> bool:
        if type(request.user) == AnonymousUser:
            return False

        return request.user.role.filter(code="RO-ADM").exists()

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.role.group.code == "GR-ADM" or request.user.role.group.code == "GR-STF":
            return queryset

        return queryset.filter(groups=request.user.role.group)
