from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from fans.forms import UserProfileForm

import pytz

@login_required
def account(request):
    message = ''
    profile = request.user.get_profile()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, initial={'user':request.user})
        if form.is_valid():
            profile = form.save(commit=False)
            profile.phone_number = form.cleaned_data['phone_number']
            profile.timezone = form.cleaned_data['timezone']
            profile.save()
            message = 'Profile updated'
        else:
            message = 'Unable to update profile'
    else:
        form = UserProfileForm(instance=profile, initial={'user':request.user})

    return render_to_response('account/account.html', 
        {'form': form, 'message': message, 'timezones': pytz.common_timezones}, 
        context_instance=RequestContext(request))

