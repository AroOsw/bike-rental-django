from django import template
from ai_bot.models import ChatSession, ChatMessage

register = template.Library()

@register.inclusion_tag("ai_bot/chat_widget.html", takes_context=True)
def show_chat_history(context):
    request = context.get("request")
    user = request.user if request else None

    history_data = []

    if user and user.is_authenticated:
        session_obj = ChatSession.objects.filter(
            user=user,
            is_active=True,
        ).order_by("-created_at").first()

        if not session_obj:
            session_obj = ChatSession.objects.create(
                user=user,
                is_active=True,
            )

        chat_history = ChatMessage.objects.filter(session=session_obj).order_by("-timestamp")[:10]

        for message in reversed(chat_history):
            history_data.append({"role": message.role, "content": message.content})

    return {
        "chat_history": history_data,
        "user": user,
    }
