from rest_access_policy import AccessPolicy


class BaseUserAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list"], "principal": "*", "effect": "allow", "condition": "is_admin"},
        {"action": ["retrieve_dashboard"], "principal": "*", "effect": "allow", "condition": "is_admin"},
        # {"action": ["publish", "unpublish"], "principal": ["group:editor"], "effect": "allow"},
        # {"action": ["destroy"], "principal": ["*"], "effect": "allow", "condition": "is_author"},
        # {"action": ["*"], "principal": ["*"], "effect": "deny", "condition": "is_happy_hour"},
    ]

    def is_admin(self, request, view, action) -> bool:
        if request.user.is_anonymous:
            return False
        return request.user.role.code == "RO-ADM" or request.user.role.code == "RO-MNG"

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
