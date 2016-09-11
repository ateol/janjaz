from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from forums.models import User

from django.contrib import messages

from django.contrib.auth.decorators import  login_required

from forums.forms import ThreadForm, ReplyForm
from forums.models import (
    Forum,
    ForumCategory,
    ForumReply,
    ForumThread,
    ThreadSubscription,
    UserPostCount,

)

def forums(request):

    categories = ForumCategory.objects.filter(parent__isnull=True)
    categories = categories.order_by("id")

    all_forums={}

    for category in categories:
        all_forums[category]=category.forums.order_by('id')

    all_forums=all_forums.items()
    most_active_forums = Forum.objects.order_by("-post_count")[:5]
    most_viewed_forums = Forum.objects.order_by("-view_count")[:5]
    most_active_members = UserPostCount.objects.order_by("-count")[:5]

    latest_posts = ForumReply.objects.order_by("-created")[:10]
    latest_threads = ForumThread.objects.order_by("-last_modified")
    most_active_threads = ForumThread.objects.order_by("-reply_count")
    most_viewed_threads = ForumThread.objects.order_by("-view_count")

    return render(request,"forums/forums.html", {
        "categories": categories,
        "most_active_forums": most_active_forums,
        "most_viewed_forums": most_viewed_forums,
        "most_active_members": most_active_members,
        "latest_posts": latest_posts,
        "latest_threads": latest_threads,
        "most_active_threads": most_active_threads,
        "most_viewed_threads": most_viewed_threads,
        "all_forums": all_forums
    })


def forum_category(request, category_id):

    category = get_object_or_404(ForumCategory, id=category_id)
    forums = category.forums.order_by("title")

    return render(request, "forums/category.html", {
        "category": category,
        "forums": forums,
    },)


def forum(request, forum_id):

    forum = get_object_or_404(Forum, id=forum_id)
    threads = forum.threads.order_by("-sticky", "-last_modified")

    forum.update_post_count()

    can_create_thread = all([
        request.user.has_perm("forums.add_forumthread", obj=forum),
        not forum.closed,
    ])

    thread_replies={}
    for thread in threads:
        thread_replies[thread]=thread.replies.all().count()

    thread_replies=thread_replies.items()
    return render(request, "forums/forum.html", {
        "forum": forum,
        "thread_replies": thread_replies,
        "can_create_thread": can_create_thread,
    })


def forum_thread(request, thread_id):
    member=request.user


    qs = ForumThread.objects.select_related("forum")
    thread = get_object_or_404(qs, id=thread_id)

    thread.update_reply_count()

    can_create_reply = all([
        request.user.has_perm("forums.add_forumreply", obj=thread),
        not thread.closed,
        not thread.forum.closed,
    ])

    if can_create_reply:
        if request.method == "POST":
            reply_form = ReplyForm(request.POST)

            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.thread = thread
                reply.author = request.user
                reply.save()

                thread.new_reply(reply)
                # subscribe the poster to the thread if requested (default value is True)
                if reply_form.cleaned_data["subscribe"]:
                    thread.subscribe(reply.author, "email")

                # all users are automatically subscribed to onsite
                thread.subscribe(reply.author, "onsite")

                return HttpResponseRedirect(reverse("forums:forums_thread", args=[thread.id]))
        else:
            reply_form = ReplyForm()
    else:
        reply_form = None

    order_type = request.GET.get("order_type", "asc")
    posts = ForumThread.objects.posts(thread, reverse=(order_type == "desc"))
    thread.inc_views()


    return render(request, "forums/thread.html", {
        "member": member,
        "thread": thread,
        "posts": posts,
        "order_type": order_type,
        "subscribed": thread.subscribed(request.user, "email"),
        "reply_form": reply_form,
        "can_create_reply": can_create_reply,
    })


@login_required
def post_create(request, forum_id):

    member = request.user
    forum = get_object_or_404(Forum, id=forum_id)

    if forum.closed:

        messages.error(request, "This forum is closed.")
        return HttpResponseRedirect(reverse("forums:forums_forum", args=[forum.id]))

    can_create_thread = request.user.has_perm("forums.add_forumthread", obj=forum)

    if not can_create_thread:

        messages.error(request, "You do not have permission to create a thread.")
        return HttpResponseRedirect(reverse("forums:forums_forum", args=[forum.id]))

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.forum = forum
            thread.author = request.user
            thread.save()

            # subscribe the poster to the thread if requested (default value is True)
            if form.cleaned_data["subscribe"]:
                thread.subscribe(thread.author, "email")

            # all users are automatically subscribed to onsite
            thread.subscribe(thread.author, "onsite")

            return HttpResponseRedirect(reverse("forums:forums_thread", args=[thread.id]))
    else:
        form = ThreadForm()

    return render(request, "forums/post_create.html", {
        "form": form,
        "member": member,
        "forum": forum
    })


@login_required
def reply_create(request, thread_id):

    member = request.user
    thread = get_object_or_404(ForumThread, id=thread_id)

    if thread.closed:
        messages.error(request, "This thread is closed.")
        return HttpResponseRedirect(reverse("forums:forums_thread", args=[thread.id]))

    can_create_reply = request.user.has_perm("forums.add_forumreply", obj=thread)

    if not can_create_reply:
        messages.error(request, "You do not have permission to reply to this thread.")
        return HttpResponseRedirect(reverse("forums:forums_thread", args=[thread.id]))

    if request.method == "POST":
        form = ReplyForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            # subscribe the poster to the thread if requested (default value is True)
            if form.cleaned_data["subscribe"]:
                thread.subscribe(reply.author, "email")

            # all users are automatically subscribed to onsite
            thread.subscribe(reply.author, "onsite")

            return HttpResponseRedirect(reverse("forums:forums_thread", args=[thread_id]))
    else:
        quote = request.GET.get("quote")  # thread id to quote
        initial = {}

        if quote:
            quote_reply = ForumReply.objects.get(id=int(quote))
            initial["content"] = "\"%s\"" % quote_reply.content

        form = ReplyForm(initial=initial)

    first_reply = not ForumReply.objects.filter(thread=thread, author=request.user).exists()

    return render(request,"forums/reply_create.html", {
        "form": form,
        "member": member,
        "thread": thread,
        "subscribed": thread.subscribed(request.user, "email"),
        "first_reply": first_reply,
    })


def ajax_reply(request):

    if request.method=="POST":

        thread_id=int(request.POST['thread_id'])
        content=request.POST['content']
        subscription=request.POST['subscribe']

        thread=get_object_or_404(ForumThread, pk=thread_id)

        if thread:
            if content=='':
                return HttpResponse("no_content")

            if thread.closed:
                return HttpResponse("closed")

            can_create_reply=request.user.has_perm("forums.add_forumreply",obj=thread)

            if not can_create_reply:
                return HttpResponse('no_perm')

            post=ForumReply(content=content)
            post.author=request.user
            post.thread=thread

            post.save()

            if subscription=="yes":
                thread.subscribe(post.author, 'email')

            thread.subscribe(post.author, 'onsite')


            context={
                'post': post,
                'thread': thread,
                'member': request.user
            }

            return render(request, 'forums/post.html', context)
    else:
        return HttpResponse("method_not_allowed")

@login_required
def post_edit(request, post_kind, post_id):

    if post_kind == "thread":
        post = get_object_or_404(ForumThread, id=post_id)
        thread_id = post.id
        form_class = ThreadForm
    elif post_kind == "reply":
        post = get_object_or_404(ForumReply, id=post_id)
        thread_id = post.thread.id
        form_class = ReplyForm
    else:
        raise Http404()

    if not post.editable(request.user):
        raise Http404()

    if request.method == "POST":
        form = form_class(request.POST, instance=post, no_subscribe=True)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("forum:forums_thread", args=[thread_id]))
    else:
        form = form_class(instance=post, no_subscribe=True)

    return render("forums/post_edit.html", {
        "post": post,
        "form": form,
    })


@login_required
def subscribe(request, thread_id):
    user = request.user
    thread = get_object_or_404(ForumThread, pk=thread_id)

    if request.method == "POST":
        thread.subscribe(user, "email")
        return HttpResponseRedirect(reverse("forums_thread", args=[thread_id]))
    else:
        ctx = RequestContext(request, {"thread": thread})
        return render(request, "forums/subscribe.html", ctx)


@login_required
def unsubscribe(request, thread_id):
    user = request.user
    thread = get_object_or_404(ForumThread, pk=thread_id)

    if request.method == "POST":
        thread.unsubscribe(user, "email")
        return HttpResponseRedirect(reverse("forums_thread", args=[thread_id]))
    else:
        ctx = RequestContext(request, {"thread": thread})
        return render(request, "forums/unsubscribe.html", ctx)


@login_required
def thread_updates(request):
    subscriptions = ThreadSubscription.objects.filter(user=request.user, kind="onsite")
    subscriptions = subscriptions.select_related("thread", "user")
    subscriptions = subscriptions.order_by("-thread__last_modified")

    if request.method == "POST":
        subscriptions.filter(pk=request.POST["thread_id"]).delete()

    ctx = {
        "subscriptions": subscriptions,
    }
    ctx = RequestContext(request, ctx)
    return render(request, "forums/thread_updates.html", ctx)

def likes(request):
    if request.method=="POST":
        post_id=request.POST['post_id']
        post_kind=request.POST['post_kind']

        post=None
        if post_kind=="thread":
            post=get_object_or_404(ForumThread, pk=post_id)
        elif post_kind=="reply":
            post=get_object_or_404(ForumReply, pk=post_id)

        current_user=get_object_or_404(User, username=request.user.username)

        context={}
        if post and current_user:
            if post.users_liked.filter(username=current_user.username).exists():
                post.likes-=1
                post.users_liked.remove(current_user)
                if post.likes<0:
                    post.likes=0
                post.like_color = 'gray'
                post.save()

            else:
                post.likes+=1
                post.users_liked.add(current_user)
                post.like_color = 'green'
                post.save()


            context['post']=post

            return render(request, 'forums/likes.html', context)

        else:
            return HttpResponse("You can not like this post")


def Search(request):
    return render(request, 'forums/search_forum.html', {})

def ajax_search(request):
    context={}
    if request.method=="POST":
        query=request.POST['search']
        post=request.POST['post']
        category=request.POST['category']
        forum=request.POST['forum']

        print(post)
        print(category)
        print(forum)

        if query=='':
            return HttpResponse('must_enter_search_term')
        if post=='no' and category=='no' and forum=='no':
            forums = Forum.objects.filter(title__icontains=query)
            context['forums'] = forums

            print(forums)

            categories = ForumCategory.objects.filter(title__icontains=query)
            context['categories'] = categories

            print(categories)

            posts = ForumThread.objects.filter(title__icontains=query)
            context['posts'] = posts

        elif category=='yes' and forum=='no' and post=='no':
            categories=ForumCategory.objects.filter(title__icontains=query)
            context['categories']=categories

        elif category=='no' and forum=='yes' and post=='no':
            forums = Forum.objects.filter(title__icontains=query)
            context['forums'] = forums

        elif category=='no' and forum=='no' and post=='yes':
            posts = ForumThread.objects.filter(title__icontains=query)
            context['posts'] =posts


        elif category=='yes' and forum=='yes' and post=='no':
            categories = ForumCategory.objects.filter(title__icontains=query)
            context['categories'] = categories

            forums = Forum.objects.filter(title__icontains=query)
            context['forums'] = forums

        elif category=='yes' and forum=='no' and post=='yes':
            categories = ForumCategory.objects.filter(title__icontains=query)
            context['categories'] = categories

            posts = ForumThread.objects.filter(title__icontains=query)
            context['posts'] = posts


        elif category=='no' and forum=='yes' and post=='yes':
            forums = Forum.objects.filter(title__icontains=query)
            context['forums'] = forums

            posts = ForumThread.objects.filter(title__icontains=query)
            context['posts'] = posts

        elif category=='yes' and forum=='yes' and post=='yes':

            forums = Forum.objects.filter(title__icontains=query)
            context['forums'] = forums

            print(forums)

            categories = ForumCategory.objects.filter(title__icontains=query)
            context['categories'] = categories

            print(categories)

            posts = ForumThread.objects.filter(title__icontains=query)
            context['posts'] = posts

        return render(request, 'forums/ajax_search_forum.html', context)
    else:
        return HttpResponse("method_not_allowed")

def ajax_flag(request):
    current_user=request.user
    if request.method=="POST":
        return HttpResponse("Working")