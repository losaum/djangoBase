from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from .models import Profile

UNAUTHORIZED_PROFILE_MESSAGE = 'Perfil de usuário não autorizado.'

def check_perfil_ouro(user):
    if (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_OURO):
        return True
    return False

def check_perfil_prata(user):
    if (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_OURO) or \
       (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_PRATA) :
        return True
    return False

def check_perfil_bronze(user):
    if (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_OURO) or \
       (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_PRATA) or \
       (user.profile.nivel_perfil  == Profile.NivelPerfil.PERFIL_BRONZE) :
        return True
    return False

def requer_perfil_ouro(function=None, redirect_field_name=REDIRECT_FIELD_NAME, 
                       login_url=None, message = UNAUTHORIZED_PROFILE_MESSAGE):
    actual_decorator = user_passes_test(
        check_perfil_ouro,
        login_url=login_url,
        redirect_field_name=redirect_field_name        
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def requer_perfil_prata(function=None, redirect_field_name=REDIRECT_FIELD_NAME, 
                        login_url=None,  message = UNAUTHORIZED_PROFILE_MESSAGE):
    actual_decorator = user_passes_test(
        check_perfil_prata,
        login_url=login_url,
        redirect_field_name=redirect_field_name       
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def requer_perfil_bronze(function=None, redirect_field_name=REDIRECT_FIELD_NAME, 
                         login_url=None,  message = UNAUTHORIZED_PROFILE_MESSAGE):
    actual_decorator = user_passes_test(
        check_perfil_bronze,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

