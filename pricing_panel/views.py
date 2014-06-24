from django.core import urlresolvers
from horizon import forms
from horizon import tables as horizon_tables
from pricing_panel import forms as pricing_forms
from pricing_panel import tables
from resource_pricing.calculators import models as type_models
from resource_pricing import models as pricing_models


class IndexView(horizon_tables.MultiTableView):
    table_classes = (tables.InstancePricesTable,)
    template_name = 'admin/pricing/index.html'

    def get_instance_prices_data(self):
        return [tables.InstancePricesTableEntry(
            id=x.resource.id,
            flavor=x.resource.flavor_set.first().os_flavor_id,
            price=x.price)
            for x in pricing_models.Price.objects.exclude(
                resource__flavor__os_flavor_id=None)]


class UpdateView(forms.ModalFormView):
    form_class = pricing_forms.UpdatePriceForm
    template_name = 'admin/pricing/update.html'
    success_url = urlresolvers.reverse_lazy('horizon:admin:pricing:index')

    def get_object(self):
        flavor = type_models.Flavor.objects.get(
            resource=self.kwargs['resource_price_id'])
        price = pricing_models.Price.objects.get(resource=flavor.resource)
        return {'resource_price_id': self.kwargs['resource_price_id'],
                'flavor': flavor.os_flavor_id,
                'price': price.price}

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['price'] = self.get_object()
        return context

    def get_initial(self):
        price = self.get_object()
        return price