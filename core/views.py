from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, Pod
from itertools import chain
# from PIL import Image
# from pdf2image import convert_from_path
# import random

# Create your views here.

@login_required(login_url='signin')
def index(request):
    # return HttpResponse('<h1>Welcome to NotePod!</h1>')
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # user_following_list = []
    feed = []

    # user_following = FollowersCount.objects.filter(follower=request.user.username)

    # for users in user_following:
    #     user_following_list.append(users.user)
    # for usernames in user_following_list:
    #     feed_lists = Post.objects.filter(user=usernames)
    #     feed.append(feed_lists)

    posts = Post.objects.all()
    for post in posts:
        feed.append(post)
        if post.type == 'pdf':
            print("pdf")

    feed_list = list(chain(feed))
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list})
    # user suggestion starts
    # all_users = User.objects.all()
    # user_following_all = []
    
    

    # for user in user_following:
    #     user_list = User.objects.get(username=user.user)
    #     user_following_all.append(user_list)

    # new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    # current_user = User.objects.filter(username=request.user.username)
    # final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    # random.shuffle(final_suggestions_list)

    # username_profile = []
    # username_profile_list = []

    # for users in final_suggestions_list:
    #     username_profile.append(users.id)

    # for ids in username_profile:
    #     profile_lists = Profile.objects.filter(id_user=ids)
    #     username_profile_list.append(profile_lists)

    # suggestions_username_profile_list = list(chain(*username_profile_list))


    


@login_required(login_url='signin')
def upload(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload', False)
        caption = request.POST.get('caption', False)

        sub = request.POST.get('u_Subject', False)
        sub_sub = request.POST.get('u_Sub_Subject', False)
        key1 = request.POST.get('k1', False)
        key2 = request.POST.get('k2', False)
        key3 = request.POST.get('k3', False)
        # request.session['key1'] = key1 #saves the input for the hashtags
        # request.session['key2'] = key2
        # request.session['key3'] = key3

        pod = user_profile.pod

        # Store the values in the session
        # request.session['d1'] = d1
        # request.session['d2'] = d2
        number=0
        if key1 == False or key1=='' or key2 == False or key2=='' or key3 == False or key3=='' or sub==False or sub=='' or sub_sub==False or sub_sub=='' or image==False or image=='':
            number=number+1
        if number!=0:
            messages.info(request, 'Fill Out All Missing Fields')
            return redirect('/')

        

        
        new_post = Post.objects.create(user=user, image=image, caption=caption, key1=key1, key2=key2, key3=key3, sub=sub, sub_sub=sub_sub, pod=pod)
        new_post.save()

        parts = new_post.image.url.split('.')
        
        index = 1
        for i in parts:
            if index==len(parts):
                new_post.type = i
                new_post.save()
            # new_post.save()
            index = index + 1

        return redirect('profile/'+user)
    else:
        return redirect('/')




@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    search = False
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    # follower = request.user.username
    # user = pk

    # if FollowersCount.objects.filter(follower=follower, user=user).first():
    #     button_text = 'Unfollow'
    # else:
    #     button_text = 'Follow'

    # user_followers = len(FollowersCount.objects.filter(user=pk))
    # user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        # 'button_text': button_text,
        # 'user_followers': user_followers,
        # 'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        # follower = request.POST['follower']
        # user = request.POST['user']

        # if FollowersCount.objects.filter(follower=follower, user=user).first():
        #     delete_follower = FollowersCount.objects.get(follower=follower, user=user)
        #     delete_follower.delete()
        #     return redirect('/profile/'+user)
        # else:
        #     new_follower = FollowersCount.objects.create(follower=follower, user=user)
        #     new_follower.save()
            # return redirect('/profile/'+user)
            return redirect('/profile/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    pods_list = Pod.objects.all()
    context = {
        'pods' : pods_list
    }
    if request.method == 'POST':

        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            user_profile.profileimg = image
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            user_profile.profileimg = image
            
        pod=request.POST['pod']
        user_profile.pod = pod
        user_profile.save()
        return redirect('settings')
    
    return render(request, 'setting.html', {'user_profile': user_profile}, context)

def signup(request):
    pods_list = Pod.objects.all()
    context = {
        'pods' : pods_list
    }
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # pod = request.POST['pod']
        
        if username == '' or email == '' or password == '':
            messages.info(request, 'Fill Out All Missing Fields')
            return redirect('signup')
        

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/')
                
                # if pod == 'no-existing-pod':    
                #     new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                #     new_profile.save()
                #     return redirect('create-pod')
                # else:
                #     new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, pod=pod)
                #     print(pod)
                #     return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html', context)

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/') 
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

# @login_required(login_url='signin')
# def subject(request):
#     if request.method == 'POST':
#         sub = request.POST['subject']
#         print(sub)
#         new_sub = Subject.objects.create(sub=sub)
#         new_sub.save()
#         print(subject)
#         return redirect('sub_subject')
#     else:
#         return render(request, 'subject.html')

# @login_required(login_url='signin')
# def sub_subject(request):
    # subject=request.session.get('subject')
    # if request.method == 'POST':
    #     subject=request.POST.get('subject')
    #     if subject=='English':
    #         return render(request, 'sub_subject.html', {'buttons': ['English 9', 'English 10', 'AP Language', 'AP Literature']})
    #     elif subject=="Math":
    #         return render(request, 'sub_subject.html', {'buttons': ['Algebra 1', 'Geometry', 'Algebra 2', 'PreCalculus', 'Trigonometry', 'Calculus AB', 'Calculus BC', "Statistics"]})
    #     elif subject=="Science":
    #         return render(request, 'sub_subject.html', {'buttons': ['Chemistry', 'Biology', 'Physics 1', 'Physics C', "Environmental Science"]})
    #     elif subject=="History":
    #         return render(request, 'sub_subject.html', {'buttons': ['US History', 'World History', 'European History', 'Human Geography', "Government", "Economics"]})
    #     else:
    #         return render(request, 'sub_subject.html', {'buttons': ['Spanish', 'French', 'Korean', 'ASL', 'German']})

    # if request.method=='POST':
    #     sub_sub = request.POST['sub_subject']
    #     new_sub = SubSubject.objects.create(sub_sub=sub_sub)
    #     new_sub.save()
        # print(sub_subject)
    # return redirect('/')
    # else:
    #     return render(request, 'sub_subject.html')


@login_required(login_url='signin')
def create_pod(request):
    if request.method == 'POST':
        # pods_list = Pod.objects.all()
        # for p in pods_list:
        #     print(p,"\n")
        name = request.POST['name']
        district = request.POST['district']
        

        if Pod.objects.filter(name=name, district=district).exists():
            messages.info(request, 'Pod Already Exists')
            return redirect('create-pod')
        else:
            new_pod = Pod.objects.create(name=name, district=district)
            new_pod.save()
            return redirect('join-pod')
    else:
        return render(request, 'create_pod.html')

# @login_required(login_url='signin')
# def pod_detail(request, pk):
#     # pod = Pod.objects.get(pk=pk)
#     # return render(request, 'pod_detail.html', {'pod': pod})
#     return 'null'
    

    

@login_required(login_url='signin')
def join_pod(request):
    pods_list = Pod.objects.all()
    pods = []
    for i in pods_list:
        pods.append(i.name)
        print(i.name)

    pods.sort()
    print(pods)

    context = {
        'pods' : pods
    }

    if request.method == 'POST':
        name = request.POST.get('pod')
        user_profile = Profile.objects.get(user=request.user)

        user_profile.pod = name
        user_profile.save()
        return redirect('/')
    else:
        return render(request, 'join_pod.html', context)
        # request.session['pod_name'] = pod_name
    # if request.method == 'POST':
    #     pod = request.POST.get('name')
    #     pod_joined = Pod.objects.get(name=name)
    #     pod_joined.save()
    #     pod.members.add(user=request.user)
    #     pod.save()
    #     return redirect('pod_detail.html')

    # else:
    #     return render(request, 'join_pod.html'

    # make a variable in join_pod.html
    #description = request.POST('description')
    #___________________________________
    # pod_obiect = Pod.objects.get(name=request.pod.name)
    # if request.method == 'POST':
    #     name = request.POST('name')
    #     pod_object = Pod.objects.filter(name=request.pod.name)
    #     pod_profile = []
    #     pod_list = []

    #     for each in pod_object:
    #         pod_profile.append(each.name)
    #         each.members.add(user=request.user)

    #     for pod in pod_profile:
    #         list = Pod.objects.filter(id_name=name)
    #         pod_list.append(list)

    #     pod_list = list(chain(*pod_list))
    # return render(request, 'join_pod.html', {'pod_profile': pod_profile, 'pod_list': pod_list})

@login_required(login_url='signin')
def topic(request):
    if request.method == 'POST':
        d1 = request.POST.get('Subject')
        d2 = request.POST.get('Sub_Subject')

        # Store the values in the session
        request.session['d1'] = d1
        request.session['d2'] = d2
        # user_profile = Profile.objects.get(user=request.user)
        # user_profile.subject = d1
        # user_profile.subject = d2


        return redirect('new_page') 

    return render(request, 'topic.html')

def new_page(request):
    # d1 = request.session.get('d1')
    # d2 = request.session.get('d2')

    user_profile = Profile.objects.get(user=request.user)
    d1 = user_profile.subject
    d2 = user_profile.sub_subject

    # print(user_profile.())

    # Clear the session values to avoid persistence
    # request.session.pop('d1', None)
    # request.session.pop('d2', None)

    # Pass the values to the new page context
    context = {
        'd1': d1,
        'd2': d2
    }

    return render(request, 'new_page.html', context)




@login_required(login_url='signin')
def search_two_og(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method=='POST':
        #search: dropdown of subjects, text (put in search), pod only check box

        #filter notes based on input
        text = request.POST['notes']
        subject = request.POST['Subject']
        sub_subject = request.POST['Sub_Subject']
        podOnly = request.POST.get('PodOnly', False)
        text = text.lower()

        posts = Post.objects.all() #list of all items
        posts = list(posts)

        notes = [] # list of filtered items

        if podOnly=='PodOnly':
            notes = Post.objects.filter(pod=user_profile.pod)
        else:
            notes = Post.objects.all()

        if subject !='':
            notes = notes.filter(sub=subject, sub_sub=sub_subject)
        else:
            notes = notes.all()
        
        notes = list(notes)

        for note in notes:
            k1 = note.key2.lower()
            k2 = note.key2.lower()
            k3 = note.key3.lower()

            if k1 in text:
                notes.append(note)
            elif k2 in text:
                notes.append(note)
            elif k3 in text:
                notes.append(note)

        if len(notes) == 0:
            for post in posts:
                notes.append(post)
            # notes = list(chain(*notes))

        
            # images = convert_from_path('note.image.url', 500, poppler_path=r'C:\Users\soyeo\CodingProjects\django-social-media-website-main\django-social-media-app\Release-23.05.0-0\poppler-23.05.0\Library\bin')

            # for i in range(len(images)):
            #     images[i].save('page' + str(i) + 'jpg', 'JPEG')
        return render(request, 'search.html', {'notes': notes, 'user_profile': user_profile})
    else:
        return render(request, 'search.html')       


keeping = []
@login_required(login_url='signin')
def search_two(request):
    global keeping
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # username = request.POST['username']

        text = request.POST.get('notes2', False)
        subject = request.POST.get('Subject', False)
        sub_subject = request.POST.get('Sub_Subject', False)
        podOnly = request.POST.get('PodOnly', False)
        text = text.lower()

        # request.session['currentT']=text
        # request.session['currentS']=subject
        # request.session['currentSS']=sub_subject
        # request.session['currentP']=podOnly

        if text!=False and text!='' and subject!='' and subject!=False and sub_subject!='' and sub_subject!=False:
            messages.info(request, '\'' + str(text) + '\'  under ' + str(subject)+' / ' + str(sub_subject))
        elif subject!='' and subject!=False and sub_subject!='' and sub_subject!=False:
            messages.info(request, str(subject)+' / ' + str(sub_subject))
        elif subject!='' and subject!=False:
            messages.info(request, str(subject))
        elif text!=False and text!='' and (subject=='' or subject==False) and (sub_subject=='' or sub_subject==False):
            messages.info(request, str('\'' + text + '\''))


        if podOnly=='PodOnly' and subject=='':
            notes1 = Post.objects.filter(pod=user_profile.pod)
            print('pod only')
        elif podOnly=='PodOnly' and subject!='' and sub_subject!='':
            notes1 = Post.objects.filter(pod=user_profile.pod, sub=subject, sub_sub=sub_subject)
            print('pod only, subject, sub-subject')
        elif podOnly=='PodOnly' and subject!='':
            notes1 = Post.objects.filter(pod=user_profile.pod, sub=subject)
            print('pod only, subject')
        elif subject!='' and sub_subject=='':
            notes1 = Post.objects.filter(sub=subject)
            print('subject')
        elif subject!='' and sub_subject!='':
            notes1 = Post.objects.filter(sub=subject, sub_sub=sub_subject)
            print('subject, sub-subject')
            print(subject)
        else:
            notes1 = Post.objects.all()
            print('all')

        notes=[]
        for note in notes1:
            count=0
            k1 = note.key2.lower()
            k2 = note.key2.lower()
            k3 = note.key3.lower()
            k4 = note.key1.lower()

            if k1 in text:
                count = count + 1
            if k2 in text:
                count = count + 1
            if k3 in text:
                count = count + 1
            if k4 in text:
                count = count + 1
            if count != 0:
                notes.append(note)

        print(len(notes))
        print('break')

        if len(notes) == 0:
            for post in notes1:
                notes.append(post)

        # request.session['currentN']=notes
        # request.session.save()
        # request.session['currentPR']=user_profile
        keeping=notes
        print(keeping)
        return render(request, 'search.html', {'notes': notes, 'user_profile': user_profile})
    else:
        return render(request, 'search.html')    

keeping2=[]
def like_post2(request):
    global keeping2
    # currentN = request.session.get('currentN')
    # currentPR = request.session.get('currentPR')
    user_profile = Profile.objects.get(user=request.user)
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save() 
        if post in keeping:
            num=keeping.index(post)
            keeping.remove(post)
            keeping.insert(num, post)
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()

        if post in keeping:
            # keeping.remove(post)
            # keeping.append(post)
            num=keeping.index(post)
            keeping.remove(post)
            keeping.insert(num, post)

    
    return render(request, 'search.html', {'notes': keeping, 'user_profile': user_profile})
