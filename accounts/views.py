from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

@api_view(['POST'])
def signup(request):
    """Handles user signup and creates UserProfile"""
    data = request.data

    # Extract data from request
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')

    if not all([email, password, name, phone]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user already exists
    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create User instance
    first_name = name.split()[0]
    last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ''

    user = User.objects.create(
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=make_password(password)
    )

    # Create associated UserProfile
    UserProfile.objects.create(
        user=user,
        phone_number=phone,
        ufi="UFI-" + str(user.id),  # Example UFI
        address=""
    )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'User created successfully',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user_id': user.id
    }, status=status.HTTP_201_CREATED)
