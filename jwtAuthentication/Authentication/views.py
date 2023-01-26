
# all the libraries used in API
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .serializers import PictureSerializer
from .models import User
from .models import Picture
import jwt, datetime
from PIL import Image, ImageOps
import os

# Create your views here.

# to register the user, it takes two parameters: email and password
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            response = Response()

            response.data = {
                'message' : 'user has been created'
            }
            return response

        else: 
            return print("data is not valid!!!")


# to login the user, it takes two parameters: email and password 
# it authenticates the user and make a token of it, then save it as cookie in user's computer
class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt' : token
        }


        return response


# it allow the user to see the data and cookie
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


# it logout the user and they cannot access the token until they login again
class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'success'
        }
        return response



# it handels the image request and manipulation 
class Profiles(APIView):
    
    # this method is for post request
    def post(self, request):

        # retreive the data from post method
        data = request.data.get('picture', None)
        name = request.data.get('name', None)

        pic = PictureSerializer(data=request.data)
        
        if pic.is_valid():
            
            # sizes for image manipulation 
            size_300 = (200,300)
            size_500 = (500,500)
            size_1024 = (1024,768)

            # converting images into different sizes
            small = Image.open(data)
            small.thumbnail(size_300)
            small.save(r'.\media\edited pictures\{}_small_size.jpg'.format(name))
            
            medium = Image.open(data)
            medium.thumbnail(size_500)
            medium.save(r'.\media\edited pictures\{}_medium_size.jpg'.format(name))

            large = Image.open(data)
            large.thumbnail(size_1024)
            large.save(r'.\media\edited pictures\{}_large_size.jpg'.format(name))

            # converting images into grayscale filter
            imgfilter = Image.open(data)
            imgfilter = ImageOps.grayscale(imgfilter)
            imgfilter.save(r'.\media\edited pictures\{}_grayscale.jpg'.format(name))


            pic.save()
            return  Response({
                "message" : r"image has been successfully saved and the variations are at 'media\edited pictures' from root directory. The original picture is at 'media\pictures'. "
            })
        return Response(pic.errors)

    
    # this method is for get request
    def get(self, request):
        data = Picture.objects.all()
        pic = PictureSerializer(data, many=True)
        return Response(pic.data)

