import json
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import VectorService, ChatService
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from uuid import UUID


# Create your views here.

class ChatView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
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
            user_message=user_text
        )

        return JsonResponse({"reply": response_text})
