from rest_framework import status
from rest_framework.exceptions import APIException


class UserNotActiveException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "User account is not verified"}
    default_code = "101"


class UserPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "status": "error",
        "message": "You do not have permission to perform this action.",
    }
    default_code = "403"


class MonitoringAndEvaluationPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "status": "error",
        "message": "You do not have permission to perform this action. Only Monitoring and Evaluation Officer",
    }
    default_code = "403"


class LoginRequiredException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status": "error",
        "message": "Login is required to access this view",
    }
    default_code = "102"


class AlreadyLoginUserException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"status": "error",
                      "message": "You are logged in already"}
    default_code = "403"


class UserSuspendedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "The user has been suspended"}
    default_code = "104"


class MissingAPIKeyException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        "status": "error",
        "message": "Auth denied. Missing required keys. API-KEY, REQUEST-TS and HASH-KEY",
    }
    default_code = "101"


class InvalidHashCodeException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "Auth denied. Invalid Hash Key"}
    default_code = "102"


class OtherAuthException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "Auth denied. Unknown Error"}
    default_code = "103"


class InvalidAPIKeyException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "Auth denied.  Invalid API Key"}
    default_code = "101"


class PasswordRestException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "The reset link is invalid"}
    default_code = "101"


class BlockedUserException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "Account Blocked"}
    default_code = "101"


class DeletedUserException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"status": "error", "message": "Account Deleted"}
    default_code = "101"


class UnverifiedUserException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "Account Not Verified"}
    default_code = "101"


class InactiveUserException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "Account Not active"}
    default_code = "101"


class NotMappedAsPastorException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "You are not a pastor yet"}
    default_code = "101"


class NotAllowedPastorException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "User Must Be an Assistance admin, Assembly, District or Area Pastor or Superintendent."}
    default_code = "101"


class NotComponent3Exception(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "User does not have access to this component."}
    default_code = "101"


class NotMonitoringAndEvaluationException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error",
                      "message": "User Must Be a Monitoring and Evaluation Officer"}
    default_code = "101"


class NotFoundUserException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "User Not Found"}
    default_code = "101"


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "Invalid token"}
    default_code = "101"


class InvalidSignatureException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"status": "error", "message": "Invalid signature"}
    default_code = "101"
