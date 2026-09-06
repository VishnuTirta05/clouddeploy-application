from django.test import TestCase
import pytest
from django.urls import reverse
from .models import Deployment


@pytest.mark.django_db
def test_create_deployment(client):
    deployment = Deployment.objects.create(
        application="CloudDeploy",
        version="1.0.0",
        environment="production",
        status="pending"
    )

    assert deployment.application == "CloudDeploy"
    assert deployment.version == "1.0.0"
    assert deployment.environment == "production"
    assert deployment.status == "pending"


@pytest.mark.django_db
def test_deployments_api(client):
    Deployment.objects.create(
        application="CloudDeploy",
        version="1.0.0",
        environment="production",
        status="pending"
    )

    response = client.get("/api/deployments/")

    assert response.status_code == 200
    assert len(response.json()) == 1
