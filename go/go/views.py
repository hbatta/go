from go.models import URL, RegisteredUser
from go.forms import URLForm, SignupForm
from datetime import timedelta
from django.conf import settings
from django.http import Http404, HttpResponseServerError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.mail import send_mail
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, get_object_or_404, redirect
import os


##############################################################################
"""
Define useful helper methods here.
"""


def is_approved( user ):
    """
    This function checks if a user account has a corresponding RegisteredUser,
    thus checking if the user is registered.
    """

    try:
        registered = RegisteredUser.objects.get( username=user.username )
        return registered.approved
    except RegisteredUser.DoesNotExist:
        return False


##############################################################################
"""
Define error page handling here.
"""


def error_404(request):
    """
    Error 404 view, in case a url is not found.
    """

    return render(request, '404.html', {
    },
    )

def error_500(request):
    """
    Error 500 view, in case a server error occurs.
    """

    return render(request, '500.html', {
    },
    )

##############################################################################
"""
Define user views here.
"""


@login_required
def index(request):
    """
    This view handles the homepage that the user is presented with when
    they request '/'. If they're not logged in, they're redirected to
    login. If they're logged in but not registered, they're given the
    not_registered error page. If they are logged in AND registered, they
    get the URL registration form.
    """

    # If the user isn't registered, don't give them any leeway.
    if not is_approved(request.user):
        return render(request, 'not_registered.html')

    url_form = URLForm() # unbound form

    if request.method == 'POST':
        url_form = URLForm( request.POST ) # bind dat form
        if url_form.is_valid():

            # We don't commit the url object yet because we need to add its
            # owner, and parse its date field.
            url = url_form.save(commit=False)
            url.owner = request.user

            # If the user entered a short url, it's already been validated,
            # so accept it. If they did not, however, then generate a
            # random one and use that instead.
            short = url_form.cleaned_data.get('short').strip()
            if len(short) > 0:
                url.short = short
            else:
                # If the user didn't enter a short url, generate a random
                # one. However, if a random one can't be generated, return
                # a 500 server error.
                random_short = URL.generate_valid_short()
                if random_short is None:
                    return HttpResponseServerError(
                        render(request, '500.html', {})
                    )
                else:
                    url.short = random_short

            # Grab the expiration field value. It's currently an unsable
            # string value, so we need to parse it into a datetime object
            # relative to right now.
            expires = url_form.cleaned_data.get('expires')

            if expires == URLForm.DAY:
                url.expires = timezone.now() + timedelta(days=1)
            elif expires == URLForm.WEEK:
                url.expires = timezone.now() + timedelta(weeks=1)
            elif expires == URLForm.MONTH:
                url.expires = timezone.now() + timedelta(weeks=3)
            else:
                pass # leave the field NULL

            # Make sure that our new URL object is clean, then save it and
            # let's redirect to view this baby.
            url.full_clean()
            url.save()
            return redirect('view', url.short)

    return render(request, 'index.html', {
        'form': url_form,
    },
    )


def view(request, short):
    """
    This view allows the user to view details about a URL. Note that they
    do not need to be logged in to view info.
    """

    url = get_object_or_404(URL, short__iexact = short)

    return render(request, 'view.html', {
        'url': url,
    },
    )


@login_required
def my_links(request):
    """
    This view displays all the information about all of your URLs. You
    obviously need to be logged in to view your URLs.
    """

    if not is_approved(request.user):
        return render(request, 'not_registered.html')

    urls = URL.objects.filter( owner = request.user )
    return render(request, 'my_links.html', {
        'urls' : urls,
    },
    )


@login_required
def delete(request, short):
    """
    This view deletes a URL if you have the permission to. User must be
    logged in and registered, and must also be the owner of the URL.
    """

    if not is_approved(request.user):
        return render(request, 'not_registered.html')

    url = get_object_or_404(URL, short__iexact = short )
    if url.owner == request.user:
        url.delete()
        return redirect('my_links')
    else:
        raise PermissionDenied()


@login_required
def signup(request):
    """
    This view presents the user with a registration form. You can register
    yourself, or another person.

    """

    signup_form = SignupForm()

    if request.method == 'POST':
        signup_form = SignupForm(request.POST, initial={'approved': False})
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get('username')
            full_name = signup_form.cleaned_data.get('full_name')
            description = signup_form.cleaned_data.get('description')

            send_mail('Signup from %s' % (username), '%s signed up at %s\n'
                'Username: %s\nMessage: %s\nPlease attend to this request at '
                'your earliest convenience.' % (str(full_name),
                str(timezone.now()).strip(), str(username), str(description)),
                settings.EMAIL_FROM, [settings.EMAIL_TO])

            signup_form.save()

            return redirect('registered')

    return render(request, 'signup.html', {
        'form': signup_form,
    },
    )


def redirection(request, short):
    """
    This view redirects a user based on the short URL they requested.
    """

    url = get_object_or_404( URL, short__iexact = short )
    url.clicks = url.clicks + 1
    url.save()

    """
    Include server-side tracking because there is no template displayed to
    the user which would include javascript tracking.
    """

    from piwikapi.tracking import PiwikTracker
    from django.conf import settings
    # First, if PIWIK variables are undefined, don't try to push
    if settings.PIWIK_SITE_ID is not "" and settings.PIWIK_URL is not "":
        try:
            piwiktracker = PiwikTracker(settings.PIWIK_SITE_ID, request)
            piwiktracker.set_api_url(settings.PIWIK_URL)
            piwiktracker.do_track_page_view('Redirect to %s' % url.target)
        # Second, if we do get an error, don't let that keep us from redirecting
        except:
            pass

    return redirect( url.target )


def staff_member_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME, login_url='about'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    return user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )(view_func)


@staff_member_required
def adminpanel(request):
    """
    This view is a simplified admin panel, so that staff don't need to log in
    to approve links
    """
    if request.POST:
        if '_approve' in request.POST:
            toapprove = RegisteredUser.objects.get(username=request.POST['username'])
            toapprove.approved = True
            toapprove.save()
        elif '_deny' in request.POST:
            todeny = RegisteredUser.objects.get(username=request.POST['username'])
            todeny.delete()
    need_approval = RegisteredUser.objects.filter(approved=False)
    return render(request, 'adminpanel.html',{
        'need_approval': need_approval
    },
    )


##############################################################################
"""
Define static user views here.
"""


def about(request):
    return render(request, 'about.html', {
    },
    )

def registered(request):
    return render(request, 'registered.html', {
    },
    )
