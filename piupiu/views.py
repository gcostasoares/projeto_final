from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Piupiu
from .forms import PiupiuForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

def home(request):
	if request.user.is_authenticated:
		form = PiupiuForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				piupiu = form.save(commit=False)
				piupiu.user = request.user
				piupiu.save()
				messages.success(request, ("Your PiuPiu Has Been Posted!"))
				return redirect('home')
		
		piupius = Piupiu.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"piupius":piupius, "form":form})
	else:
		piupius = Piupiu.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"piupius":piupius})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        
        # Check if the profile being followed is not the same as the current user's profile
        if request.user.profile != profile:
            # Follow the user
            request.user.profile.follows.add(profile)
            # Save our profile
            request.user.profile.save()

            # Return message
            messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
        else:
            messages.error(request, ("You cannot follow yourself."))

        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')




def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        piupius = Piupiu.objects.filter(user_id=pk).order_by("-created_at")

        # Post Form logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            
            # Check if the profile being followed is not the same as the current user's profile
            if current_user_profile != profile:
                # Decide to follow or unfollow
                if action == "unfollow":
                    current_user_profile.follows.remove(profile)
                elif action == "follow":
                    current_user_profile.follows.add(profile)
                # Save the profile
                current_user_profile.save()
            else:
                messages.error(request, ("You cannot follow yourself."))
        
        return render(request, "profile.html", {"profile": profile, "piupius": piupius})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')
		

def followers(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'followers.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


def follows(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			return render(request, 'follows.html', {"profiles":profiles})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')



def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        # Get initial data for the forms
        user_initial_data = {
            'email': current_user.email,
            'username': current_user.username,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
        }

        profile_initial_data = {
            'profile_image': profile_user.profile_image,
            'profile_bio': profile_user.profile_bio,
            'homepage_link': profile_user.homepage_link,
            'facebook_link': profile_user.facebook_link,
            'instagram_link': profile_user.instagram_link,
            'linkedin_link': profile_user.linkedin_link,
        }

        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user, initial=user_initial_data)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user, initial=profile_initial_data)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Update the session auth hash to keep the user logged in
            update_session_auth_hash(request, current_user)

            messages.success(request, "Your Profile Has Been Updated!")
            return redirect('home')

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

	
def piupiu_like(request, pk):
	if request.user.is_authenticated:
		piupiu = get_object_or_404(Piupiu, id=pk)
		if piupiu.likes.filter(id=request.user.id):
			piupiu.likes.remove(request.user)
		else:
			piupiu.likes.add(request.user)
		
		return redirect(request.META.get("HTTP_REFERER"))




	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')


def piupiu_show(request, pk):
	piupiu = get_object_or_404(Piupiu, id=pk)
	if piupiu:
		return render(request, "show_piupiu.html", {'piupiu':piupiu})
	else:
		messages.success(request, ("That Piupiu Does Not Exist..."))
		return redirect('home')		