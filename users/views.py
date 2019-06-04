from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import register_public_user
import django.dispatch
from .models import Public_user,Person
from django.dispatch import receiver

make_public = django.dispatch.Signal(providing_args=['instance','created'])
def register(request):
    if request.method == 'POST':
        form = register_public_user(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.save()
            make_public.send(sender=Person,instance=user,created = True)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = register_public_user()
    return render(request, 'users/register.html', {'form': form})

@receiver(make_public,sender=Person)
def make_public_user(sender,instance,created,**kwargs):
    if created:
        Public_user.objects.create(new_user=instance)

@receiver(make_public,sender=Person)
def save_public_user(sender,instance,**kwargs):
    instance.public_user.save()

@login_required
def profile(request):
    return render(request, 'users/profile.html')