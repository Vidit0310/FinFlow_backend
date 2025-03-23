from django.contrib.auth.models import User
from django.db import IntegrityError
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
from .contracts.contracts import register_user
from .utils.ufid import generate_unique_code


# with contract 
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Handles user signup and creates UserProfile"""
    data = request.data

    # ✅ Extract data from request
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    dob = data.get('dob')
    address = data.get('address', '')
    pan = data.get('panCard', '')
    ufid = generate_unique_code(pan)



    # ✅ Validate all required fields

    if not all([email, password, name, phone, dob, address,pan, ufid]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Check if the user already exists
    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Check if UFI is unique
    if UserProfile.objects.filter(pan=pan).exists():
        return Response({'error': 'UFI already exists, please use a unique UFI'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Create User instance
    first_name = name.split()[0]
    last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ''

    try:
        # ✅ Create User
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)
        )

        # ✅ Create associated UserProfile
        UserProfile.objects.create(
            user=user,
            phone_number=phone,
            pan=pan,
            ufid=ufid,
            address=address,
            dob=parse_date(dob)
        )

        # ✅ Generate JWT tokens
        hexcode = register_user(name,dob,pan,ufid)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': f'User created successfully please copy ufid {ufid}  hexcode is {hexcode}',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'profile': {
                'phone_number': phone,
                'ufi': ufid,
                'address': address,
                'dob': dob
            }
        }, status=status.HTTP_201_CREATED)

    except IntegrityError as e:
        return Response({'error': 'An error occurred while creating the user: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# without contract 
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     """Handles user signup and creates UserProfile"""
#     data = request.data

#     # ✅ Extract data from request
#     email = data.get('email')
#     password = data.get('password')
#     name = data.get('name')
#     phone = data.get('phone')
#     dob = data.get('dob')
#     address = data.get('address', '')
#     pan = data.get('panCard', '')
#     ufid = generate_unique_code(pan)



#     # ✅ Validate all required fields

#     if not all([email, password, name, phone, dob, address,pan, ufid]):
#         return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Check if the user already exists
#     if User.objects.filter(username=email).exists():
#         return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Check if UFI is unique
#     if UserProfile.objects.filter(pan=pan).exists():
#         return Response({'error': 'UFI already exists, please use a unique UFI'}, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ Create User instance
#     first_name = name.split()[0]
#     last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ''

#     try:
#         # ✅ Create User
#         user = User.objects.create(
#             username=email,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=make_password(password)
#         )

#         # ✅ Create associated UserProfile
#         UserProfile.objects.create(
#             user=user,
#             phone_number=phone,
#             pan=pan,
#             ufid=ufid,
#             address=address,
#             dob=parse_date(dob)
#         )

#         # ✅ Generate JWT tokens
#         refresh = RefreshToken.for_user(user)

#         return Response({
#             'message': f'User created successfully please copy ufid {ufid}',
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'user_id': user.id,
#             'profile': {
#                 'phone_number': phone,
#                 'ufi': ufid,
#                 'address': address,
#                 'dob': dob
#             }
#         }, status=status.HTTP_201_CREATED)

#     except IntegrityError as e:
#         return Response({'error': 'An error occurred while creating the user: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Handles user login with UFID validation and returns JWT tokens"""

    email = request.data.get('email')
    password = request.data.get('password')
    ufid = request.data.get('ufId')

    if not email or not password or not ufid:
        return Response({'error': 'Email, password, and UFID are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user with email and password
    user = authenticate(username=email, password=password)

    if user:
        try:
            # Check if the authenticated user's UFID matches
            if user.userprofile.ufid == ufid:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                return Response({
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid UFID'}, status=status.HTTP_401_UNAUTHORIZED)

        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)