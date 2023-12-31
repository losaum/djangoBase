from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .signals import user_login_password_failed


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.pk})

@receiver(post_save, sender=User)
def send_email_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Novo usuário criado',
            f'Um novo usuário com email {instance.email} foi criado.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )


#######################


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='usuário'
    )
    
    birthday = models.DateField('data de nascimento', null=True, blank=True)
    
    rg = models.CharField(max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    #avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)

    class NivelPerfil(models.TextChoices):
        PERFIL_DEFAULT = 'D', _('Padrão')
        PERFIL_BRONZE = 'B', _('Bronze')
        PERFIL_PRATA = 'P', _('Prata')
        PERFIL_OURO = 'O', _('Ouro')

        
    PERFIL_DEFAULT = 'D'
    PERFIL_BRONZE = 'B' 
    PERFIL_PRATA = 'P'
    PERFIL_OURO = 'O'

    PERFIL_CHOICES = (
        (PERFIL_DEFAULT, 'Padrão'),
        (PERFIL_BRONZE, 'Bronze'),
        (PERFIL_PRATA, 'Prata'),
        (PERFIL_OURO, 'Ouro'),
    )    
        

    nivel_perfil = models.CharField(
        max_length=1,
        choices=NivelPerfil.choices,
        default=NivelPerfil.PERFIL_DEFAULT,
    )    

    @property
    def hasPerfilPremio(self):
        if self.nivel_perfil != self.NivelPerfil.PERFIL_DEFAULT:
            return True
        return False
    
    @property
    def nivelPerfil(self):
        
        if self.nivel_perfil == self.NivelPerfil.PERFIL_OURO:            
            return "ouro"
        elif self.nivel_perfil == self.NivelPerfil.PERFIL_PRATA:          
            return "prata"
        elif self.nivel_perfil == self.NivelPerfil.PERFIL_BRONZE:            
            return "bronze"
        else:            
            return "padrão"    
        

    @property
    def getRGB_nivelPerfil(self):
        
       
        if self.nivel_perfil == self.NivelPerfil.PERFIL_OURO:            
            return "rgb(214, 235, 20)"
        elif self.nivel_perfil == self.NivelPerfil.PERFIL_PRATA:          
            return "rgb(215, 215, 215)"
        elif self.nivel_perfil == self.NivelPerfil.PERFIL_BRONZE:            
            return "rgb(173, 138, 86)"
        else:            
            return "rgb(214, 214, 214)"       

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()