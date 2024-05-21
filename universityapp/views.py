from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ApprovalActivities, Document, ApprovalWorkflow
from .serializers import DocumentSerializer, ApprovalWorkflowSerializer
from django.shortcuts import get_object_or_404


class ApproveDocumentView(APIView):
    def post(self, request, doc_id):
        document = get_object_or_404(Document, id=doc_id)
        workflow = get_object_or_404(ApprovalWorkflow, document=document)
        user = request.user
        print(user)
#         workflow = ApprovalWorkflow.objects.get(id=some_id)
# user_approvers = workflow.get_user_approvers(request.user)
        print(workflow.check_approval_requirements())
        if not workflow.check_approval_requirements():
            return Response({'error': 'Not all approval requirements are met. Ensure to check the required allotted operation permission.'}, status=403)

        if workflow.current_approver.user.pkid != user.pkid:
            return Response({'error': 'You are not authorized to approve this document.'}, status=403)

        if document.approval_state != 'pending':
            return Response({'error': 'Document is not awaiting approval.'}, status=400)

        # # Approve the document and update the current_approver
        next_approver = workflow.approvers.filter(
            order__gt=workflow.current_approver.order).first()
        if next_approver:
            workflow.current_approver = next_approver
            # print(next_approver.user.first_name)
            workflow.save()
            ApprovalActivities.objects.create(
                approval_document_workflow=workflow,
                sender=request.user,
                receiver=next_approver.user
            )
            update_receiver_status = ApprovalActivities.objects.filter(approval_document_workflow=workflow,
                                                                       receiver=request.user).first()
            if update_receiver_status:
                print(update_receiver_status.approval_activity_status)
                update_receiver_status.approval_activity_status = "approved"
                update_receiver_status.save()
            return Response({'message': 'Document approved. Awaiting next approval.'}, status=200)
        else:
            document.approval_state = 'approved'
            document.save()
            update_receiver_status = ApprovalActivities.objects.filter(approval_document_workflow=workflow,
                                                                       receiver=request.user).first()
            if update_receiver_status:
                update_receiver_status.approval_activity_status = "approved"
                update_receiver_status.save()
            return Response({'message': 'Document fully approved.'}, status=200)
