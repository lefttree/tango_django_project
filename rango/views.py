from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
#user
from rango.forms import UserForm, UserProfileForm
#login
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
#decorator 
from django.contrib.auth.decorators import login_required
#logout
from django.contrib.auth import logout
#datetime
from datetime import datetime
#run query
from rango.bing_search import run_query
#
from django.contrib.auth.models import User
#redirect
from django.shortcuts import redirect

def index(request):
    #return HttpResponse("Rango says hello world! <a href='/rango/about'>About</a>")
    context = RequestContext(request)
    #a dictionary that maps template variable names with python variables
    #query the database
    #category_list = Category.objects.all()
    cat_list = get_category_list()
    
    #cat_list = cat_list.order_by('-likes')[:5]
    context_dict = {'cat_list': cat_list}

    #for category in category_list:
    #    category.url = category.name.replace(' ', '_')
    
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    response = render_to_response('rango/index.html', context_dict, context)

    #new code#
    #store session on server side#
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        last_visit_time = datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")
        visits = request.session.get('visits', 0)

        if (datetime.now() - last_visit_time).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    return render_to_response('rango/index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    cat_list = get_category_list()

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict_about = {'aboutmessage': 'about what'}
    context_dict_about['count'] = count
    context_dict_about['cat_list'] = cat_list

    #response_str = "This is the about page" + "<a href='/rango'>Rango</a>"
    return render_to_response('rango/about.html', context_dict_about, context)

def add_category(request):
    #Get the context from the request
    context = RequestContext(request)
    cat_list = get_category_list()

    #A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #save the new category to the database
            form.save(commit=True)

            #now call index() view, user will be shown the homepage
            return index(request)
        else:
            print form.errors
    else:
        #request was not a POST, display the form to enter details
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form, 'cat_list': cat_list}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    
    category_name = category_name_url.replace('_', ' ')
    cat_list = get_category_list()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            #This time we cannot commit stright away
            #Not all fields are automatically populated
            page = form.save(commit=False)
            try:
                cat = Category.objects.get(name=category_name_url)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category')

            page.views = 0
            #save new model instance
            page.save()

            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'category_name_url': category_name_url,
                    'category_name': category_name,
                    'form': form,
                    'cat_list': cat_list,
                   }
    return render_to_response('rango/add_page.html', context_dict, context)

def category(request, category_name_url):
   context = RequestContext(request)
   category_name = category_name_url.replace('_', ' ')
   cat_list = get_category_list()

   context_dict = {'category_name': category_name,
                   'cat_list': cat_list 
                  }
   try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        pages = pages.order_by('-views')

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
   except Category.DoesNotExist:
        pass

   if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list

   return render_to_response('rango/category.html', context_dict, context)


def register(request):
    print ">>>> Test cookie worked!"
    #request.session.delete_test_cookie()
    context = RequestContext(request)

    #to indicate registration process status
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #hash the password with set_password method
            user.set_password(user.password)
            user.save()

            #now sort out the UserProfile instance
            #Since we need to set the user attribute ourselves
            #set commit = False
            #This delays saving the model until we're ready
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #now we save the UserProfile model instance
            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    cat_list = get_category_list()

    context_dict ={'user_form': user_form,
                   'profile_form': profile_form,   
                   'cat_list': cat_list,
                }

    return render_to_response('rango/register.html', context_dict, context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #user django's machinery to attempt to see if
        #username/password is valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('rango/login.html', {}, context)

@login_required
def restricted(request):
    return HttpResponse("You're logged in.")

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')

def search(request):
    context = RequestContext(request)
    result_list = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        
        if query:
            result_list = run_query(query)

    context_dict={'result_list': result_list}
    return render_to_response('rango/search.html',context_dict, context )


def get_category_list():
   cat_list = Category.objects.all()

   for cat in cat_list:
        cat.url = encode_url(cat.name)
   return cat_list

def encode_url(name):
    url = name.replace(' ', '_')
    
    return url

def decode_url(url):
    name = url.replace('_', ' ')
    return name

@login_required
def profile(request):
   context = RequestContext(request)
   cat_list = get_category_list()
   context_dict = {'cat_list': cat_list}
   u = User.objects.get(username=request.user)

   try:
        up = UserProfile.objects.get(user=u)
   except:
        up = None

   context_dict['user'] = u
   context_dict['userprofile'] = up

   return render_to_response('rango/profile.html', context_dict, context)


#track url click number
def track_url(request):
    context = RequestContext(request)

    page_id = None
    url = "/rango/"
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None

    if request.method == "GET":
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes = likes
            category.save()

    return HttpResponse(likes)
