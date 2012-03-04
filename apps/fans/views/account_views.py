from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from fans.forms import UserProfileForm

@login_required
def account(request):
    message = ''
    profile = request.user.get_profile()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, initial={'user':request.user})
        if form.is_valid():
            profile = form.save(commit=False)
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            message = 'Phone number saved!'
        else:
            message = 'Invalid phone number!'
    else:
        form = UserProfileForm(instance=profile, initial={'user':request.user})

    return render_to_response('account/account.html', 
        { 'form': form, 'message': message}, 
        context_instance=RequestContext(request))

