from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EstadisticaSerializer
import boto3
from django.conf import settings

class EstadisticaListView(APIView):
    def get(self, request):
        try:
            dynamodb = boto3.client('dynamodb', region_name=settings.AWS_REGION,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            
            response = dynamodb.scan(
                TableName='estadistica'
            )
            items = response.get('Items')
            
            cleaned_data = []
            for item in items:
                cleaned_item = {}
                for key, value in item.items():
                    cleaned_item[key] = list(value.values())[0]
                cleaned_data.append(cleaned_item)
            
            return Response(cleaned_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = EstadisticaSerializer(data=request.data)
            if serializer.is_valid():
                # Crear un nuevo objeto Estadistica a partir de los datos validados del serializer
                estadistica_object = serializer.save()
                
                # Convertir el objeto Estadistica a un diccionario que pueda ser insertado en DynamoDB
                item = {
                    "id": {"S": str(estadistica_object.id)},
                    "fecha_ingreso": {"S": estadistica_object.fecha_ingreso},
                    "hora_ingreso": {"S": estadistica_object.hora_ingreso},
                    "fecha_salida": {"S": estadistica_object.fecha_salida},
                    "hora_salida": {"S": estadistica_object.hora_salida},
                    "tiempo": {"S": estadistica_object.tiempo},
                    "ruta": {"S": estadistica_object.ruta}
                }
                
                dynamodb = boto3.client('dynamodb', region_name=settings.AWS_REGION,
                                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                
                dynamodb.put_item(
                    TableName='estadistica',
                    Item=item
                )
                
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
