from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegistrationForm, USerEditForm

from rest_framework import generics, status
from .serializers import CreateUserSerializer, EditUserSerializer, ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from .permissions import EditOwnProfile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})

def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create new user object but dont save yet
            new_user=user_form.save(commit=False)
            #set password
            new_user.set_password(user_form.cleaned_data['password'])
            #save now
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

@login_required
def edit(request):
    if request.method=='POST':
        user_form=USerEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form=USerEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form':user_form})


#API
class CreateUser(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CreateUserSerializer

class EditUser(generics.UpdateAPIView):
    queryset=get_user_model().objects.all()
    serializer_class=EditUserSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes = [EditOwnProfile]

class UserLoginApiView(ObtainAuthToken):
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class=ChangePasswordSerializer
    model=get_user_model()
    authentication_classes=(TokenAuthentication,)
    permission_classes=[IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
