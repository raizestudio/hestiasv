from rest_access_policy import AccessPolicy


class BaseUserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "create", "update", "partial_update"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["list_w_term"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_admin",
        },
        {
            "action": [
                "create_from_email",
                "confirm_email",
                "upload_user_avatar",
                "retrieve_dashboard",
            ],
            "principal": "*",
            "effect": "allow",
        },
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
