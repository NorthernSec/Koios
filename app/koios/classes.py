from tastypie.resources      import Resource, ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization  import Authorization, DjangoAuthorization


class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]



class AuthenticatedModelResource(ModelResource):
    class Meta:
        authentication       = ApiKeyAuthentication()
        authorization        = DjangoAuthorization()
        abstract             = True  # not a real resource
        include_resource_uri = True
        list_allowed_methods = ['get', 'post']

    def __new__(cls, *args, **kwargs):
        """Automatically set resource_name if missing."""
        new_class = super().__new__(cls)
        meta      = getattr(new_class, "Meta", None)

        if (meta and hasattr(meta, "queryset") and
            not hasattr(meta, "resource_name") ):
            model              = meta.queryset.model
            meta.resource_name = model._meta.model_name.lower()
        return new_class

    def dehydrate(self, bundle):
        included_fields = getattr(self._meta, 'fields', None)
        excluded_fields = getattr(self._meta, 'excludes', [])
        for field in self._meta.queryset.model._meta.fields:
            name = field.name
            # Skip excluded fields
            if name in excluded_fields:
                continue
            # If 'fields' is set, only include those
            if included_fields is not None and name not in included_fields:
                continue
            bundle.data[name] = getattr(bundle.obj, name)
        bundle.data['resource_uri'] = self.get_resource_uri(bundle)
        return bundle

    def authorized_read_detail(self, object_list, bundle):
        if bundle.obj is None:
            return object_list
        return super().authorized_read_detail(object_list, bundle)


class AuthenticatedResource(Resource):
    """Base for non-model Tastypie resources that still require authentication."""
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization  = Authorization()  # Manual implementation required
        abstract       = True
