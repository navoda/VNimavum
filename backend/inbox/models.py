from django.db import models


class Conversation(models.Model):
    """A chat thread a customer starts on the website."""

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    customer = models.ForeignKey(
        "customers.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="conversations",
    )
    guest_name = models.CharField(max_length=200, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=30, blank=True)
    order = models.ForeignKey(
        "orders.Order", null=True, blank=True, on_delete=models.SET_NULL, related_name="conversations"
    )
    service_order = models.ForeignKey(
        "services.ServiceOrder",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="conversations",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-last_message_at"]

    def __str__(self):
        who = self.customer.name if self.customer else self.guest_name
        return f"Conversation with {who}"


class Message(models.Model):
    class Sender(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        OWNER = "owner", "Owner"

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=Sender.choices)
    body = models.TextField()
    attachment = models.ImageField(upload_to="inbox/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.get_sender_display()}: {self.body[:40]}"
