import pytest
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from core.models import BikeModel, BikeInstance, Reservation
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone


@pytest.mark.django_db
def test_bike_model_creation():
    bike = BikeModel.objects.create(
        brand="Kross",
        model="Level 2.0",
        type="mountain",
        price_per_day=100.00,
    )

    created_bike = BikeModel.objects.get(id=bike.id)

    assert created_bike.brand == "Kross"
    assert str(created_bike) == "Kross - Level 2.0"



@pytest.mark.django_db
def test_bike_model_unique_together_constraint():
    BikeModel.objects.create(
        brand="Kross",
        model="Level 2.0",
        type="mountain",
        price_per_day=100.00,
    )

    with pytest.raises(IntegrityError):
        BikeModel.objects.create(
            brand="Kross",
            model="Level 2.0",
            type="mountain",
            price_per_day=119.00,
        )

@pytest.mark.django_db
def test_bike_instance_creation():
    model = BikeModel.objects.create(
        brand="Kross",
        model="Level 2.0",
        type="mountain",
        price_per_day=119.00,
    )

    instance = BikeInstance.objects.create(
        bike_model=model,
        serial_number="KRS1111",
        status="available",
    )

    created_bike_instance = BikeInstance.objects.get(id=instance.id)
    assert created_bike_instance.bike_model == model



@pytest.mark.django_db
def test_bike_instance_related_name():
    model = BikeModel.objects.create(
        brand="Kross",
        model="Level 2.0",
        type="mountain",
        price_per_day=119.00,
    )

    BikeInstance.objects.create(
        bike_model=model,
        serial_number="KRS1111",
        status="available",
    )
    BikeInstance.objects.create(
        bike_model=model,
        serial_number="KRS1112",
        status="available",
    )

    instances = model.instances.count()

    assert instances == 2

@pytest.mark.django_db
def test_reservation_calculation():
    user = User.objects.create_user(username="testuser", password="password")

    bike_model = BikeModel.objects.create(
        brand="Kross",
        model="Level 2.0",
        type="mountain",
        price_per_day=Decimal("100.05"),
    )

    bike_instance = BikeInstance.objects.create(
        bike_model=bike_model,
        serial_number="KRS1112",
        size="M",
    )

    reservation = Reservation.objects.create(
        user=user,
        bike_instance=bike_instance,
        start_time=timezone.make_aware(datetime(2025, 8, 21, 10, 0, 0)),
        end_time=timezone.make_aware(datetime(2025, 8, 21, 18, 0, 0)),
        is_confirmed=True,
    )

    reservation.save()
    assert reservation.total_cost == Decimal("100.05")

    reservation2 = Reservation.objects.create(
        user=user,
        bike_instance=bike_instance,
        start_time=timezone.make_aware(datetime(2025, 8, 21, 10, 0, 0)),
        end_time=timezone.make_aware(datetime(2025, 8, 22, 18, 0, 0)),
        is_confirmed=True,
    )

    reservation2.save()
    assert reservation2.total_cost == Decimal("200.10")