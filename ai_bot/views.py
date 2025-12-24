import json
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import ChatService
from django.http import JsonResponse
from .models import ChatSession




# Create your views here.

class ChatView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        user = request.user
        user_reservations = request.user.user_reservations.select_related(
            "bike_instance__bike_model").all()

        system_context = f"Reservations for user: {user.username}\n"

        if not user_reservations:
            system_context += "User currently has NO reservations in the database."
        else:
            for i, reservation in enumerate(user_reservations, start=1):
                system_context += (
                    f"Reservation {i}\n"
                    f"Bike: {reservation.bike_instance}\n"
                    f"From: {reservation.start_time}, To: {reservation.end_time}\n"
                    f"Is confirmed: {reservation.is_confirmed}\n"
                    f"Total cost: {reservation.total_cost} THB \n\n"
                )
        data = json.loads(request.body)
        user_text = data.get("message")

        if not user_text:
            return JsonResponse({"error": "Message is empty"}, status=400)


        session_obj = ChatSession.objects.filter(
            user=request.user,
            is_active=True,
        ).order_by("-created_at").first()

        if not session_obj:

            session_obj = ChatSession.objects.create(
                user=request.user,
                is_active=True,
            )

        chatservice = ChatService()
        response_text = chatservice.get_chat_response(
            session_id=session_obj.id,
            user_message=user_text,
            system_context=f"SYSTEM CONTEXT (INTERNAL DATABASE): \n{system_context}",
        )

        return JsonResponse({"reply": response_text})
