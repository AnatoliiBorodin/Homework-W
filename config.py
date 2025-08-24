default_confluence_group = "confluence-public"
default_admin_group = "org-admins"
default_account_lead = "557058:dc9ad4ec-abd5-4fe9-bf2c-1c02693fa1fb"

confluence_full_permissions = [
    ("read", "space"),
    ("administer", "space"),
    ("create", "page"),
    ("create", "blogpost"),
    ("create", "comment"),
    ("create", "attachment"),
    ("delete", "page"),
    ("delete", "blogpost"),
    ("delete", "comment"),
    ("delete", "attachment"),
    ("export", "space"),
    ("restrict_content", "space"),
]

confluence_default_permissions = [
    ("read", "space"),
    ("create", "page"),
    ("create", "blogpost"),
    ("create", "comment"),
    ("create", "attachment")
]
