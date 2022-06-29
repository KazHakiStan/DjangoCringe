from django import template

from menu_app.models import Menu

register = template.Library()


@register.inclusion_tag('menu_app/menu.html')
def main_menu():
    menu = Menu.objects.get(menu_label='main_menu')
    return {'menu': menu.links.order_by('priority').all()}


@register.inclusion_tag('menu_app/menu.html')
def user_menu():
    menu = Menu.objects.get(menu_label='user_menu')
    return {'menu': menu.links.order_by('priority').all()}
