from django.forms import ModelForm
from django.template import RequestContext
from django.shortcuts import render_to_response

from fans.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

def account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            user_profile = request.user.get_profile()
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.save()
            return render_to_response('account/account.html', { 'form': form, 'message': 'Phone number saved!'}, context_instance=RequestContext(request))
        else:
            form = UserProfileForm(instance=request.user.get_profile())
            return render_to_response('account/account.html', { 'form': form, 'message': 'Invalid phone number!'}, context_instance=RequestContext(request))

    form = UserProfileForm(instance=request.user.get_profile())
    return render_to_response('account/account.html', { 'form': form, 'message': ''}, context_instance=RequestContext(request))

