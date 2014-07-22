from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
#user
from rango.forms import UserForm, UserProfileForm

def index(request):
    #return HttpResponse("Rango says hello world! <a href='/rango/about'>About</a>")
    context = RequestContext(request)
    #a dictionary that maps template variable names with python variables
    #query the database
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    for category in category_list:
        category.url = category.name.replace(' ', '_')

    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)

    context_dict_about = {'aboutmessage': 'about what'}

    #response_str = "This is the about page" + "<a href='/rango'>Rango</a>"
    return render_to_response('rango/about.html', context_dict_about, context)

def add_category(request):
    #Get the context from the request
    context = RequestContext(request)

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

    return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)
    
    category_name = category_name_url.replace('_', ' ')
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
                   }
    return render_to_response('rango/add_page.html', context_dict, context)

def category(request, category_name_url):
   context = RequestContext(request)
   category_name = category_name_url.replace('_', ' ')

   context_dict = {'category_name': category_name}
   try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
   except Category.DoesNotExist:
        pass

   return render_to_response('rango/category.html', context_dict, context)


def register(request):
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

    context_dict ={'user_form': user_form,
                   'profile_form': profile_form,    
                }

    return render_to_response('rango/register.html', context_dict, context)
