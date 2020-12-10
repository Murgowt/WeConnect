from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    age=models.IntegerField()
    friends=models.ManyToManyField(User,blank=True,related_name='friends')

    def add_friend(self,acc):
        if not acc in  self.friends.all():
            self.friends.add(acc)

    def remove_friend(self,acc):
        if acc in self.friends.all():
            self.friends.remove(acc)

    def un_friend(self,removee):
        self.remove_friend(removee)
        rfl=UserProfile.objects.get(user=removee)
        rfl.remove_friend(self.user)

    def __str__(self):
        return(self.user.username)


class FriendRequest(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_active=models.BooleanField(default=True,blank=True,null=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def accept(self):
        rfl=UserProfile.objects.get(self.receiver)
        if(rfl):
            rfl.add_friend(self.sender)
            sfl=UserProfile.objects.get(self.sender)
            if(sfl):
                sfl.add_friend(self.receiver)
        self.save()

    def decline(self):
        self.is_active=False
        self.save()

    def cancel(self):
        self.is_active=False
        self.save()

