from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django_countries.fields import CountryField


from random import shuffle

from .utils import get_proimage_name, get_procover_name


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None,
                    is_active=True, is_staff=False, is_admin=False, subscribed=True):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.subscribed = subscribed
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None, subscribed=True):
        user = self.create_user(
            email, username, password=password, is_staff=True, subscribed=subscribed)
        return user

    def create_superuser(self, email, username, password=None, subscribed=True):
        user = self.create_user(email, username, password=password,
                                is_staff=True, is_admin=True, subscribed=subscribed)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    username = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_shortname(self):
        return self.username

    def get_fullname(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def get_profile(self):
        try:
            profile = self.profile
        except:
            profile = None
        return profile

    def get_absolute_url(self):
        # return reverse('accounts:profile',kwargs={'user_slug':self.slug})
        return reverse('home')


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            user = self.instance
            qs = qs.exclude(user=user)
        except:
            pass
        return qs

    def toggle_follow(self, user, toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if toggle_user in user_profile.following.all():
            user_profile.following.remove(toggle_user)
            added = False
        else:
            user_profile.following.add(toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit=5):
        profile = user.get_profile()
        following = profile.get_following()
        qs = self.get_queryset().exclude(user=user).exclude(user__in=following)
        return qs.order_by('?')[:limit]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    following = models.ManyToManyField(
        User, related_name='followed_by', blank=True)
    avatar = models.ImageField(
        blank=True, null=True, upload_to=get_proimage_name)
    cover = models.ImageField(blank=True, null=True,
                              upload_to=get_procover_name)
    country = CountryField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    birthday = models.DateField(blank=True, null=True)
    objects = UserProfileManager()
    color = models.CharField(max_length=120, default='#FF0000')

    def __str__(self):
        return self.user.username + ' profile'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'user_slug': self.user.slug})

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)
