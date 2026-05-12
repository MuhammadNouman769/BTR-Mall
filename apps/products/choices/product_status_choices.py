from django.db import models


class ProductStatus(models.TextChoices):

    # ================= CREATION FLOW =================
    DRAFT = "draft", "Draft"

    # ================= REVIEW FLOW =================
    PENDING = "pending", "Pending Approval"
    REJECTED = "rejected", "Rejected"

    # ================= LIVE PRODUCTS =================
    ACTIVE = "active", "Active"

    # ================= INVENTORY =================
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"

    # ================= BUSINESS STATES =================
    INACTIVE = "inactive", "Inactive"
    ARCHIVED = "archived", "Archived"

    # ================= DELETE FLOW =================
    DELETED = "deleted", "Deleted"