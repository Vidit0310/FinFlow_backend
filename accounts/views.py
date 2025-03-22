from django.contrib.auth.models import User
from rest_framework import status
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Handles user signup and creates UserProfile"""
    data = request.data

    # Extract data from request
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    dob = data.get('dob')

    if not all([email, password, name, phone, dob]):
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
        ufi=f"UFI-{user.id}",
        address="",
        dob=parse_date(dob)  # Save date of birth
    )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'User created successfully',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user_id': user.id
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt  
def create_userprofile(request):
    """Create or update UserProfile"""
    user = request.user

    data = request.data
    address = data.get('address', '')
    ufi = data.get('ufi', '')

    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.address = address
        profile.ufi = ufi
        profile.save()

        return Response({
            "message": "UserProfile created successfully",
            "profile": {
                "ufi": profile.ufi,
                "phone_number": profile.phone_number,
                "address": profile.address
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Handles user login and returns JWT tokens"""
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    print(email, password)
    user = authenticate(username=email, password=password)

    if user:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id
        }, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
