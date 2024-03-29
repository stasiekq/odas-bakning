from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, Group, Permission
import random, string
from encrypted_model_fields.fields import EncryptedCharField
from django.utils.crypto import get_random_string
from django.core.validators import MinValueValidator

class User(AbstractUser):
    balance = models.IntegerField(default=1000)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    account_number = models.CharField(max_length=6, unique=True, default=get_random_string(length=6, allowed_chars=string.digits))
    
    def connect_sensitive_data(self, credit_card_number, id_number):
        SensitiveData.objects.create(user=self, credit_card_number=credit_card_number, id_number=id_number)
    
    
class SensitiveData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_card_number = EncryptedCharField(unique=True, max_length=16)
    id_number = EncryptedCharField(unique=True, max_length=10)
    
class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    reciever_name = models.CharField(max_length=100)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def validate(self):
        if self.sender.balance < self.amount:
            return False
        else:
            return True
        
    def execute(self):
        if self.validate():
            with transaction.atomic():
                self.sender.balance -= self.amount
                self.sender.save()
                self.reciever.refresh_from_db()
                self.reciever.balance += self.amount
                self.reciever.save()
                return True
        return False