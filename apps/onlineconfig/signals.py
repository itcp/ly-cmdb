from django.dispatch import Signal

post_conf_create = Signal(providing_args=('nginx',))