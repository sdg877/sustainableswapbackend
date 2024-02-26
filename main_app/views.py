from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Item, Swap, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .serializers import UserSerializer, GroupSerializer, ItemSerializer, SwapSerializer, ProfileSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from django.middleware.csrf import get_token

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SwapViewSet(viewsets.ModelViewSet):
    queryset = Swap.objects.all()
    serializer_class = SwapSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ItemCreate(CreateView):
    model = Item
    fields = ['item_title', 'item_description']

class LogoutView(APIView):
    permission_class = [permissions.IsAuthenticated]
    def post(self, request):
        print(request.data.body['refresh_token'])
        try: 
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def item_view(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item_data = {
            'id': item_id,
            'title': item.item_title,
            'description': item.item_description,
        }
        return JsonResponse(item_data)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

# def login_signup_view(request):
#     if request.method == 'POST':
#         # If it's a signup request
#         if 'signup' in request.POST:
#             form = UserCreationForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 return redirect('items')
#         # If it's a login request
#         elif 'login' in request.POST:
#             form = AuthenticationForm(data=request.POST)
#             if form.is_valid():
#                 user = form.get_user()
#                 login(request, user)
#                 return redirect('items')
#     else:
#         form_signup = UserCreationForm()
#         form_login = AuthenticationForm()
#         context = {'form_signup': form_signup, 'form_login': form_login}
#         return render(request, 'registration/login_signup.html', context)
    

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user after signup
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Signup successful'})
        else:
            # If form validation fails, return error response
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        # Return error response for GET requests
        return JsonResponse({'message': 'GET requests not supported'}, status=405)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'correct_username' and password == 'correct_password':
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'message': 'GET requests not supported'}, status=405)


