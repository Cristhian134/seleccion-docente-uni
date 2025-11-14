from loguru import logger
from django.shortcuts import redirect
from django.urls import resolve, Resolver404


class GlobalMiddleware:

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    try:
      resolve(request.path)
    except Resolver404:
      if request.user.is_authenticated:
        logger.warning(
          f"Usuario autenticado intentó acceder a ruta inexistente: "
          f"{request.path} (user={request.user.codigoUsuario}, ip={request.META.get('REMOTE_ADDR')})"
        )
        return redirect('home')
      return redirect('login')

    return self.get_response(request)
