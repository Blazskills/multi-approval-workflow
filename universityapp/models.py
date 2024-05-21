# models.py
from django.db import models

from account.models import User
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # status = models.CharField(max_length=10, default='pending')
    approval_state = models.CharField(max_length=10, default='pending')
    created_by = models.ForeignKey(
        User, related_name="created_documents", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"


class Approver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveBigIntegerField(default=1)
    created_by = models.ForeignKey(
        User, related_name="created_approval", on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.user} {self.order} {self.created_by}"

    class Meta:
        ordering = ['order']
        unique_together = [['created_by', 'order'], ['created_by', 'user']]


class ApprovalWorkflow(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    workflow_action_type = models.ForeignKey(
        "universityapp.ActionType", on_delete=models.CASCADE, related_name="workflow_action_flow", null=True, blank=True)
    approvers = models.ManyToManyField(
        Approver, related_name='assigned_documents')
    current_approver = models.ForeignKey(
        Approver, related_name="documents_to_approve", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.document} {self.approvers} {self.current_approver}"

    def get_relevant_approvers(self):
        last_approed_order = self.approvers.filter(
            documents_to_approve__approval_state='approved').aggregate(models.Max('order'))['order__max'] or 0
        return self.approvers.filter(order__gt=last_approed_order)

    def get_user_approvers(self, user):
        return self.approvers.filter(created_by=user)

    # NOTE: This ensures that at least all the document action requirement are
    # NOTE: met, even if the approvers user types are more than the document
    # NOTE: requirements. But the requirement must first be met.
    def check_approval_requirements(self):
        # Get the set of required user types
        required_user_types = set(self.workflow_action_type.approval_required.values_list(
            'approval_requirement_name', flat=True))

        # Get the set of user types in the selected approvers
        selected_user_types = set(
            self.approvers.values_list('user__user_type', flat=True))

        print({"required_user_types": required_user_types})
        print({"selected_user_types": selected_user_types})

        # Check if all required user types are in the selected user types
        return required_user_types.issubset(selected_user_types)

    # NOTE: This ensures that all the required document action required type are met.
    # NOTE: For instance, if the document action type requires HOD AND DEAN,
    # NOTE: this is expected to be the same  in the selected approvers for the document. Can not be more and can not be less.

    def check_all_required_action_permission_in_selected_user_type_approval_requirements(self):
        # Get the set of required user types
        required_user_types = set(self.workflow_action_type.approval_required.values_list(
            'approval_requirement_name', flat=True))

        # Get the set of user types in the selected approvers
        selected_user_types = set(
            self.approvers.values_list('user__user_type', flat=True))
        # Check if all required user types are in the selected user types and vice versa
        return required_user_types.issubset(selected_user_types) and selected_user_types.issubset(required_user_types)

    def save(self, *args, **kwargs):
        print("here")
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if not self.current_approver:
            self.current_approver = self.approvers.order_by('order').first()
            super().save(update_fields=['current_approver'])


APPROVAL_ACTIVITY_STATUS = [
    ('waiting', _('Waiting')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
    # Add more options as needed
]


class ApprovalActivities(models.Model):
    approval_document_workflow = models.ForeignKey(
        ApprovalWorkflow, on_delete=models.CASCADE, related_name='approval_document_flow')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_assigned_documents', null=True, )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver_assigned_documents', null=True, )
    approval_activity_status = models.CharField(
        max_length=20,
        choices=APPROVAL_ACTIVITY_STATUS,
        default="waiting",
        help_text=_(
            "Approval Activity Status (e.g., Waiting, Approved and Rejected)"),
        verbose_name=_("Approval Activity Status"),
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # approvers = models.ManyToManyField(
    #     Approver, related_name='assigned_documents')
    # current_approver = models.ForeignKey(
    #     Approver, related_name="documents_to_approve", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.approval_document_workflow.document} sent from: {self.sender} to:{self.receiver} current status:{self.approval_activity_status}"


class ApprovalRequiredActionType(models.Model):
    approval_requirement_name = models.CharField(max_length=50, unique=True, )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.approval_requirement_name}"


class ActionType(models.Model):
    action_name = models.CharField(max_length=50, unique=True,)
    approval_required = models.ManyToManyField(
        ApprovalRequiredActionType,  related_name='approval_required_action_type')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.action_name}  {self.approval_required} {self.created}"
