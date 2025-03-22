from import_export import resources
from .models import Computador

class ComputadorResource(resources.ModelResource):
    class Meta:
        model = Computador