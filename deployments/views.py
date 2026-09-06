
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Deployment
import json
import logging


logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse("CloudDeploy is running!")


@csrf_exempt
def deployments_list(request):

    if request.method == "GET":
        deployments = Deployment.objects.all()

        data = []

        for deployment in deployments:
            data.append({
                "id": deployment.id,
                "application": deployment.application,
                "version": deployment.version,
                "environment": deployment.environment,
                "status": deployment.status,
                "created_at": deployment.created_at,
            })

        return JsonResponse(data, safe=False)

    if request.method == "POST":

        try:
            body = json.loads(request.body)

        except json.JSONDecodeError:
            logger.warning("Received invalid JSON")

            return JsonResponse({
                "error": "Invalid JSON"
            }, status=400)

        required_fields = [
            "application",
            "version",
            "environment"
        ]

        for field in required_fields:

            if not body.get(field):
                logger.warning(
                    "Missing required field: %s",
                    field
                )

                return JsonResponse({
                    "error": f"{field} is required"
                }, status=400)

        deployment = Deployment.objects.create(
            application=body["application"],
            version=body["version"],
            environment=body["environment"],
            status="pending"
        )

        logger.info(
            "Deployment created: %s version %s",
            deployment.application,
            deployment.version
        )

        return JsonResponse({
            "id": deployment.id,
            "message": "Deployment created",
            "application": deployment.application,
            "version": deployment.version,
            "environment": deployment.environment,
            "status": deployment.status
        }, status=201)

    return JsonResponse({
        "error": "Method not allowed"
    }, status=405)

