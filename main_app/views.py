from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Item, Swap, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .serializers import UserSerializer, GroupSerializer, ItemSerializer, SwapSerializer, ProfileSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
import boto3
import os
import uuid

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

def item_view(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item_data = {
            'item_title': item.item_title,
            'item_description': item.item_description,
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_item(request, item_id):
    if request.method == 'PUT' and not request.path.endswith('/'):
        # Append trailing slash to the URL
        return JsonResponse({'message': 'Please use the URL with a trailing slash'}, status=400)

    # Retrieve the item object
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'PUT':
        # Extract data from request
        new_item_data = request.data  # Assuming you are using DRF's request object
        # Update item fields with new data
        for key, value in new_item_data.items():
            setattr(item, key, value)
        # Save the updated item
        item.save()
        return JsonResponse({'message': 'Item updated successfully'})
    else:
        # Handle other HTTP methods if necessary
        return JsonResponse({'message': 'Method not allowed'}, status=405)

# @login_required
# def add_photo(request, item_id):
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3',
#                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#                           aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
#                           region_name=os.getenv('AWS_S3_REGION_NAME'))
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         try:
#             bucket = os.getenv('S3_BUCKET')
#             s3.upload_fileobj(photo_file, bucket, key)
#             url = f"{os.getenv('S3_BASE_URL')}{bucket}/{key}"
#             # Assuming you have an Item model to store the photo URL
#             Item.objects.create(item_title="Your Item Title", item_description="Your Item Description", photo_url=url)
#         except Exception as e:
#             print('An error occurred uploading file to S3')
#             print(e)
#     return redirect('detail', item_id=item_id)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_swap(request, item_id):
    try:
        item = get_object_or_404(Item, pk=item_id)
        data = request.data.copy()  # Copy the request data to modify it
        data['item'] = item_id  # Add the item ID to the request data
        serializer = SwapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Swap submitted successfully'})
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
def about_me(request):
    return render(request, 'about_me.html')
