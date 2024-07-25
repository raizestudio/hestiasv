from rest_access_policy import AccessPolicy


class AssetAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list", "retrieve", "update", "partial_update", "create", "destroy"], "principal": "*", "effect": "allow"},
        # {"action": ["create", "destroy"], "principal": "*", "effect": "allow", "condition": "is_admin"},
    ]

    def is_admin(self, request, view, action) -> bool:
        return request.user.role.code == "RO-ADM" or request.user.role.code == "RO-MNG"
