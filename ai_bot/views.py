import json

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import ChatService
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from core.models import Reservation



# Create your views here.

class ChatView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        session_obj = ChatSession.objects.filter(
            user=user,
            is_active=True,
        ).order_by("-created_at").first()

        if not session_obj:
            session_obj = ChatSession.objects.create(
                user=user,
                is_active=True,
            )

        chat_history = ChatMessage.objects.filter(session=session_obj).order_by("timestamp")
        history_data = []
        for message in chat_history:
            history_data.append({"role": message.role, "content": message.content})

        return render(request, "chat_widget.html", context={
            "chat_history": history_data,
        })


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

        full_prompt = (
            "SYSTEM CONTEXT (INTERNAL DATABASE):\n"
            f"{system_context}\n"
            "-------------------\n"
            f"USER QUESTION: {user_text}"
        )

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
            user_message=full_prompt,
        )

        return JsonResponse({"reply": response_text})
