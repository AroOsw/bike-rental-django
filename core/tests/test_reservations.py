import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import BikeModel, BikeInstance, Reservation
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def bike_image():
    """Create a temporary in-memory image file."""
    img = Image.new('RGB', (100, 100), color = (73, 109, 137))
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile("test_image.jpg", buffer.read(), content_type="image/jpeg")

@pytest.fixture
def bike_model():
    """Create a bike model for testing."""
    return BikeModel.objects.create(
        brand="Giant",
        model="Escape 3",
        type="road",
        price_per_day=Decimal("50.00"),
    )

@pytest.fixture
def bike_instance(bike_model, bike_image):
    """Create a bike instance associated with the given bike model."""
    return BikeInstance.objects.create(
        bike_model=bike_model,
        serial_number="GIANT123",
        size="M",
        bike_img=bike_image,
    )

@pytest.fixture
def reservation(bike_instance, bike_model, user):
    start_time = timezone.now() + timedelta(days=2)
    end_time = start_time + timedelta(days=5)

    return Reservation.objects.create(
        user=user,
        bike_instance=bike_instance,
        start_time=start_time,
        end_time=end_time,
    )

@pytest.mark.django_db
def test_user_can_create_reservation(user, bike_model, bike_instance):
    """Tests whether a user can create a bike reservation with valid data.
        Verifies that the reservation fields match the provided values."""

    start_time = timezone.now() + timedelta(days=10)
    end_time = start_time + timedelta(days=15)

    reservation1 = Reservation.objects.create(
        user=user,
        bike_instance=bike_instance,
        start_time=start_time,
        end_time=end_time,
    )

    assert reservation1.user == user
    assert reservation1.bike_instance == bike_instance
    assert reservation1.start_time == start_time
    assert reservation1.end_time == end_time


@pytest.mark.django_db
def test_user_cannot_create_reservation_with_end_before_start_date(client, user, bike_model, bike_instance):
    """Verifies that a reservation with an end date before the start date is rejected."""

    client.force_login(user)

    start_datetime = timezone.now() + timedelta(days=5)
    end_datetime = timezone.now() + timedelta(days=1)

    form_data_1 = {
        "start_time": start_datetime.strftime("%Y-%m-%d %H:%M"),
        "end_time": end_datetime.strftime("%Y-%m-%d %H:%M"),
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_1)

    assert response.status_code == 200
    assert Reservation.objects.count() == 0
    assert "Something went wrong. Please check the form for errors." in response.content.decode()


@pytest.mark.django_db
def test_user_cannot_create_reservation_in_past(client, user, bike_model, bike_instance):
    """Verifies that a reservation with a start date in the past is rejected."""

    client.force_login(user)

    day_now = timezone.now()
    start_time_past = day_now - timedelta(days=5)
    end_time_past = day_now - timedelta(days=1)

    start_time_str = start_time_past.strftime("%Y-%m-%d %H:%M")
    end_time_str = end_time_past.strftime("%Y-%m-%d %H:%M")

    form_data_2 = {
        "start_time": start_time_str,
        "end_time": end_time_str,
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_2)

    assert response.status_code == 200
    assert Reservation.objects.count() == 0
    assert "Something went wrong. Please check the form for errors." in response.content.decode()

@pytest.mark.django_db
def test_user_cannot_create_overlapping_reservations(client, user, bike_model, bike_instance, reservation):
    """Verifies that overlapping reservations for the same bike instance are rejected."""

    client.force_login(user)

    start_time =  reservation.start_time + timedelta(days=3)
    end_time = start_time + timedelta(days=4)

    start_time_2 = reservation.start_time + timedelta(days=1)
    end_time_2 = start_time_2 + timedelta(days=7)

    start_time_3 = reservation.start_time + timedelta(days=1)
    end_time_3 = start_time_3 + timedelta(days=4)

    start_time_4 = reservation.start_time + timedelta(days=3)
    end_time_4 = start_time_4 + timedelta(days=7)

    form_data_3_1 = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M"),
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_3_1)

    assert response.status_code == 200
    assert Reservation.objects.count() == 1
    assert "Something went wrong. Please check the form for errors." in response.content.decode()

    form_data_3_2 = {
        "start_time": start_time_2.strftime("%Y-%m-%d %H:%M"),
        "end_time": end_time_2.strftime("%Y-%m-%d %H:%M"),
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_3_2)

    assert response.status_code == 200
    assert Reservation.objects.count() == 1
    assert "Something went wrong. Please check the form for errors." in response.content.decode()

    form_data_3_3 = {
        "start_time": start_time_3.strftime("%Y-%m-%d %H:%M"),
        "end_time": end_time_3.strftime("%Y-%m-%d %H:%M"),
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_3_3)

    assert response.status_code == 200
    assert Reservation.objects.count() == 1
    assert "Something went wrong. Please check the form for errors." in response.content.decode()

    form_data_3_4 = {
        "start_time": start_time_4.strftime("%Y-%m-%d %H:%M"),
        "end_time": end_time_4.strftime("%Y-%m-%d %H:%M"),
        "bike_instance": bike_instance.id,
    }

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.post(url, data=form_data_3_4)

    assert response.status_code == 200
    assert Reservation.objects.count() == 1
    assert "Something went wrong. Please check the form for errors." in response.content.decode()


@pytest.mark.django_db
def test_bike_details_page_loads_successfully(client, user, bike_model, bike_instance):
    """Verifies that the bike details page returns a 200 OK status."""

    url = reverse("bike_details", kwargs={"slug": bike_model.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert bike_model.brand in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("days", [1, 3, 7, 14])
def test_calculate_price_ajax(client, bike_model, days):
    """Tests the AJAX endpoint for calculating rental price based on duration."""

    url = reverse("calculate_price_ajax", kwargs={"bike_model_id": bike_model.id})
    response = client.get(url, {'days': days})

    assert response.status_code == 200

    data = response.json()
    assert 'total_price' in data
    assert 'price_per_day' in data
    assert 'days' in data
    assert data['days'] == days

    expected_price_per_day = float(bike_model.calculate_rental_price(days))
    expected_total_price = expected_price_per_day * days

    assert data['price_per_day'] == expected_price_per_day
    assert data['total_price'] == expected_total_price


@pytest.mark.django_db
def test_reservation_edit(client, user, bike_instance, reservation):
    """Tests editing an existing reservation."""

    client.force_login(user)

    new_start_time = reservation.start_time + timedelta(days=1)
    new_end_time = reservation.end_time - timedelta(days=1)

    form_data_4 = {
        "start_time": new_start_time,
        "end_time": new_end_time,
        "reservation_id": reservation.id,
    }

    url = reverse("reservation_edit", kwargs={"reservation_id": reservation.id})
    response = client.get(url)

    assert response.status_code == 200

    url = reverse("reservation_edit", kwargs={"reservation_id":reservation.id})
    response = client.post(url, data=form_data_4, follow=True)

    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse("reservations")

    assert "Your reservation has been updated successfully!" in response.content.decode()

    updated_reservation = Reservation.objects.get(id=reservation.id)
    assert updated_reservation.start_time == new_start_time
    assert updated_reservation.end_time == new_end_time

@pytest.mark.django_db
def test_reservation_delete(client, user, reservation):
    """Tests deleting an existing reservation."""

    client.force_login(user)
    url = reverse("reservation_delete")
    response = client.post(url, data={"reservation_id": reservation.id}, follow=True)

    assert response.status_code == 200
    assert response.request["PATH_INFO"] == reverse("reservations")
    assert Reservation.objects.count() == 0
    assert "Reservation cancelled successfully." in response.content.decode()


@pytest.mark.django_db
def test_if_unauthorized_user_cant_see_reservations(client):
    """Tests that an unauthorized user cannot access the reservations page."""

    url = reverse("reservations")
    response = client.get(url)

    assert response.status_code == 200
    assert "Please log in to see your reservations" in response.content.decode()

@pytest.mark.django_db
def test_unauthorized_user_cannot_edit_reservations(client, reservation):
    """Tests that an unauthorized user cannot edit a reservation."""

    edit_url = reverse("reservation_edit", kwargs={"reservation_id": reservation.id})
    response_get = client.get(edit_url, follow=True)

    assert response_get.status_code == 200
    assert response_get.request["PATH_INFO"] == reverse("index")

    new_start_time = reservation.start_time + timedelta(days=1)
    new_end_time = reservation.end_time - timedelta(days=1)

    form_data_5 = {
        "start_time": new_start_time,
        "end_time": new_end_time,
        "reservation_id": reservation.id,
    }
    response_post = client.post(edit_url, data=form_data_5, follow=True)

    assert response_post.status_code == 200
    assert response_post.request["PATH_INFO"] == reverse("index")

    unchanged_reservation = Reservation.objects.get(id=reservation.id)
    assert unchanged_reservation.start_time == reservation.start_time


@pytest.mark.django_db
def test_unauthenticated_user_cannot_delete_reservation(client, reservation):
    """Verifies that an unauthenticated user cannot delete a reservation and is redirected."""
    initial_count = Reservation.objects.count()

    delete_url = reverse("reservation_delete")
    response = client.post(delete_url, data={"reservation_id": reservation.id})

    assert response.status_code == 302
    assert response.url == reverse("index")
    assert Reservation.objects.count() == initial_count