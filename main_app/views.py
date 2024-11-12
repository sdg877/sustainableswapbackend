from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Item, Swap, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .serializers import UserSerializer, ItemSerializer, SwapSerializer, ProfileSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import boto3
import os
import uuid

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    http_method_names = ['get', 'post', 'patch', 'delete']



class SwapViewSet(viewsets.ModelViewSet):
    queryset = Swap.objects.all()
    serializer_class = SwapSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class LogoutView(APIView):
    def post(self, request):
        try: 
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt    
def item_view(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item_data = {
            'item_title': item.item_title,
            'item_description': item.item_description,
            'image_url': item.image.url if item.image else None,
        }
        return JsonResponse(item_data)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    

    
class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_items(request, user_id):  
    try:
        items = Item.objects.filter(user_id=user_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = get_object_or_404(Item, pk=item_id)
        # Check if the user is the owner of the item
        if item.user == request.user:
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'}, status=201)
        else:
            return JsonResponse({'error': 'You do not have permission to delete this item'}, status=403)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_item(request, item_id):
    print(request)
    if request.method == 'PUT' and not request.path.endswith('/'):
        return JsonResponse({'message': 'Please use the URL with a trailing slash'}, status=400)

    item = get_object_or_404(Item, pk=item_id)
    print(item)

    if request.method == 'PUT':
        new_item_data = request.data 
       
        print(new_item_data)        
        for key, value in new_item_data.items():
            setattr(item, key, value)
        item.save()
        return JsonResponse({'message': 'Item updated successfully'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_swap(request, item_id):
    try:
        item = get_object_or_404(Item, pk=item_id)
        data = request.data.copy() 
        data['item'] = item_id  
        serializer = SwapSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return JsonResponse({'message': 'Swap submitted successfully'})
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
def about_me(request):
    return render(request, 'about_me.html')

@api_view(['GET'])
def get_swaps(request, item_id):
    try:
        item = get_object_or_404(Item, pk=item_id)
        swaps = Swap.objects.filter(item=item)
        serializer = SwapSerializer(swaps, many=True)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
