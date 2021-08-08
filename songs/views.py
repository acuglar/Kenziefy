from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SampleSerializer
import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        """ exemplo """
        serializer = SampleSerializer(data=request.data)  # 1. chamando serializer
        serializer.is_valid()  # 2. validando chamada com método is_valid()
        serializer.data  # acessando data se is_valid() ok
        ipdb.set_trace()

        return Response({"message": "This is a POST method"})


class ParamView(APIView):
    # funções com mesmo nome devem ser definidas em classes distintas
    # posteriormente será abordado de modo menos primitiva
    def get(self, request, name):
        return Response({"message": f"Hello {name}"})
        
    def post(self, request, name):
        return Response({"message": f"Hello {name}"})