from rest_access_policy import AccessPolicy


class EnterpriseAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list"], "principal": "*", "effect": "allow", "condition": "is_admin"},
        {"action": ["create"], "principal": "*", "effect": "allow"},
        {"action": ["retrieve", "update", "partial_update"], "principal": "*", "effect": "allow"},
        {"action": ["destroy"], "principal": "*", "effect": "allow"},
    ]

    def is_admin(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.role.code == "RO-ADM" or request.user.role.code == "RO-MNG"

        return False

    # def is_author(self, request, view, action) -> bool:
    #     user = view.get_object()
    #     return request.user == article.author

    # def is_happy_hour(self, request, view, action) -> bool:
    #     now = datetime.datetime.now()
    #     return now.hour >= 17 and now.hour <= 18:

    # @classmethod
    # def scope_queryset(cls, request, queryset):
    #     print(f"DEBUG: {request.user.groups.all()}")
    #     if request.user.groups.filter(code="GR-ADM").exists():
    #         return queryset
