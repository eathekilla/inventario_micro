from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,UserSerializerLogout,FincaSerializer,FincaBodegaLoteSerializer
from .serializers import LotesSerializer, BodegasSerializer, FincaSerializer,FincaSerializerRel,UserDetailSerializer,EditInfoUserSerializer,EditeUserWithInfoUserSerializer
from .models import Finca
from rest_framework import status,permissions,generics
from .models import Lotes, Bodegas, Finca,InfoUser
from rest_framework.decorators import api_view
from .serializers import CreateUserWithInfoUserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated


UserModel = get_user_model()

class UserRegister(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.check_user(serializer.validated_data)
            login(request, user)
            return Response({'message': 'User logged in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
    
class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class FincaView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        fincas = Finca.objects.all()
        serializer = FincaSerializer(fincas, many=True)
        return Response({'fincas': serializer.data}, status=status.HTTP_200_OK)

class FincaList(generics.ListCreateAPIView):
    serializer_class = FincaBodegaLoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtrar las fincas por el usuario autenticado
        user = self.request.user
        return Finca.objects.filter(usuario=user)
    


class LotesListCreateView(generics.ListCreateAPIView):
    queryset = Lotes.objects.all()
    serializer_class = LotesSerializer

class LotesRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lotes.objects.all()
    serializer_class = LotesSerializer

class BodegasListCreateView(generics.ListCreateAPIView):
    queryset = Bodegas.objects.all()
    serializer_class = BodegasSerializer

class BodegasRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bodegas.objects.all()
    serializer_class = BodegasSerializer

class FincaListCreateView(generics.ListCreateAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer

class FincaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer


class FincaRelListCreateView(generics.ListCreateAPIView):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializerRel 


@api_view(['POST'])
def create_user_with_info_user(request):
    
    if request.method == 'POST':
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"error": "USER_EXIST", "message": "El nombre de usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CreateUserWithInfoUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            usuario = get_object_or_404(User,username=username)
            usuario.first_name = request.data.get('first_name')
            usuario.last_name = request.data.get('last_name')
            usuario.save()
            info_user = get_object_or_404(InfoUser,usuario=usuario)
            info_user_request = request.data.get('info_user')
            info_user.telefono= info_user_request['telefono']
            info_user.direccion = info_user_request['direccion']
            info_user.tipo_documento = info_user_request['tipo_documento']
            info_user.numero_documento = info_user_request['numero_documento']
            info_user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def edit_info_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EditeUserWithInfoUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = EditeUserWithInfoUserSerializer(user)
        return Response(serializer.data, content_type='application/json', status=status.HTTP_200_OK)
    else:
        return Response({"message": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['DELETE'])
def delete_user(request, user_id):
    if request.method == 'DELETE':
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return JsonResponse({'success': True, 'message': 'User and associated InfoUser deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@api_view(['GET'])
@login_required
def get_all_info_users(request):
    if request.method == 'GET':
        # Obtén todos los objetos InfoUser
        info_users = InfoUser.objects.all()
        first= InfoUser.objects.first()

        # Serializa los objetos InfoUser en formato JSON
        info_users_data = []
        for info_user in info_users:
            user = info_user.usuario  # Obtén el objeto User relacionado
            groups = Group.objects.filter(user=user)  # Obtén los grupos a los que pertenece el usuario

            user_data = {
                'nombre':user.first_name,
                'apellido':user.last_name,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'groups': [group.name for group in groups]  # Lista de nombres de grupos
            }

            info_users_data.append({
                'telefono': info_user.telefono,
                'direccion': info_user.direccion,
                'tipo_documento': info_user.tipo_documento,
                'numero_documento': info_user.numero_documento,
                'usuario': user_data,
            })

        return Response(info_users_data, content_type='application/json', status=status.HTTP_200_OK)





# Aplica el decorador a tu vista
@method_decorator(csrf_exempt, name='dispatch')
class BodegasListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verifica si el usuario es específico o superusuario
        if request.user.username != 'simpleagriuser@a.com' and not request.user.is_superuser:
            return Response({'detail': 'No tienes permiso para acceder a esta vista.'}, status=403)

        bodegas = Bodegas.objects.all()
        bodegas_list = []

        for bodega in bodegas:
            finca_codigo = bodega.lote.finca.codigo if bodega.lote and bodega.lote.finca else None
            finca_nombre = bodega.lote.finca.nombre_finca if bodega.lote and bodega.lote.finca else None
            bodega_data = {
                'codigo_bodega': bodega.codigo,
                'nombre_bodega': bodega.nombre_bodega,
                'codigo_finca': finca_codigo,
                'nombre_finca': finca_nombre
            }
            bodegas_list.append(bodega_data)

        return Response({'bodegas': bodegas_list})
