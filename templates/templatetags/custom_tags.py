from django import template
from vitrine_digital.helper import descriptarAESGCM

register = template.Library()

@register.filter
def descriptografar(value):
    try:
        return descriptarAESGCM(value)
    except Exception as e:
        return "E-mail inválido"