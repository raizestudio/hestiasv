from rest_access_policy import AccessPolicy


class ServiceAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list", "update", "partial_update"], "principal": "*", "effect": "allow"},
        {"action": ["create", "destroy"], "principal": "*", "effect": "allow", "condition": "is_admin"},
        # {"action": ["publish", "unpublish"], "principal": ["group:editor"], "effect": "allow"},
        # {"action": ["destroy"], "principal": ["*"], "effect": "allow", "condition": "is_author"},
        # {"action": ["*"], "principal": ["*"], "effect": "deny", "condition": "is_happy_hour"},
    ]

    def is_admin(self, request, view, action) -> bool:
        return request.user.role.code == "RO-ADM" or request.user.role.code == "RO-MNG"
