from django.contrib import admin

from universityapp.models import ActionType, ApprovalActivities, ApprovalRequiredActionType, ApprovalWorkflow, Approver, Document

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "title",
        "content",
        # "status",
        "approval_state",

    ]
    list_display = (
        "id",
        "title",
        "content",
        # "status",
        "approval_state",
        "created_by",
    )


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "document",
    ]
    list_display = (
        "id",
        "document",
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.current_approver = instance.approvers.order_by(
            'order').first()
        instance.save()


@admin.register(Approver)
class ApproverAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "user",
        "order",
        "created_by",

    ]
    list_display = (
        "id",
        "user",
        "order",
        "created_by",
    )


@admin.register(ApprovalActivities)
class ApprovalActivitiesAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "approval_document_workflow",
        "sender",
        "receiver",

    ]
    list_display = (
        "id",
        "approval_document_workflow",
        "sender",
        "receiver",
        "approval_activity_status",
        "created",
        "updated",
    )


@admin.register(ApprovalRequiredActionType)
class ApprovalRequiredActionTypeAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "approval_requirement_name",
        "created",
        "updated",

    ]
    list_display = (
        "id",
        "approval_requirement_name",
        "created",
        "updated",
    )


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display_links = [
        "id",
        "action_name",
        "display_approval_required",
        "created",
        "updated",

    ]
    list_display = (
        "id",
        "action_name",
        "display_approval_required",
        "created",
        "updated",
    )

    def display_approval_required(self, obj):
        return ", ".join([approval_requirement.approval_requirement_name for approval_requirement in obj.approval_required.all()])

    display_approval_required.short_description = 'Approval Required'
