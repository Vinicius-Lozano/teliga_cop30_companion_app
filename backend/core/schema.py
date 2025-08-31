from drf_spectacular.openapi import AutoSchema

APP_TAGS = {
    'events': 'Eventos',
    'item': 'Itens',
    'users': 'Usuários',
}

class AppNameAutoSchema(AutoSchema):
    def get_tags(self):
        app_name = self.view.__class__.__module__.split('.')[0]
        return [APP_TAGS.get(app_name, app_name)]

