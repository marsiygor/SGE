from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_core.messages import HumanMessage, AIMessage
from .graph import sge_agent
import logging

logger = logging.getLogger(__name__)


class CopilotChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        history_input = request.data.get('history', [])

        if not user_message:
            return Response({"error": "A mensagem é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            messages = []
            for msg in history_input:
                role = msg.get('role')
                content = msg.get('content')
                if role == 'human':
                    messages.append(HumanMessage(content=content))
                elif role == 'ai':
                    messages.append(AIMessage(content=content))

            messages.append(HumanMessage(content=user_message))
            result = sge_agent.invoke({"messages": messages})
            final_response = result["messages"][-1].content

            return Response({"response": final_response, "status": "success"})

        except Exception as e:
            logger.error(f"Erro ao processar requisição do Copiloto: {str(e)}")
            return Response(
                {"error": "Falha interna ao processar sua solicitação.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
