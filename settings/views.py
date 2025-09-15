from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from .models import SiteInfo
from .forms import SiteInfoForm, SocialMediaLinkFormSet, MenuNameFormSet, TagsFormSet
from .tables import SiteInfoTable  # Assuming you have defined a table class


# Mixin for handling formsets
# class FormsetMixin:
#     formset_class = None

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
      
#         if self.request.method == 'POST':
#             context['formset'] = self.formset_class(self.request.POST, instance=self.object)
#         else:
#             context['formset'] = self.formset_class(instance=self.object)
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']
#         if formset.is_valid():
#             self.object = form.save()
#             formset.instance = self.object
#             formset.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)

class FormsetMixin:
    formsets_classes = {}  # Dictionary to hold formset classes

    def get_formsets(self, instance=None):
        """
        Instantiate all formsets with the given instance.
        """
        formsets = {}
        for name, formset_class in self.formsets_classes.items():
            if self.request.method == 'POST':
                formsets[name] = formset_class(self.request.POST, self.request.FILES, instance=instance)
            else:
                formsets[name] = formset_class(instance=instance)
        return formsets

    def get_context_data(self, **kwargs):
        """
        Add formsets to the context data.
        """
        context = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)
        context['formsets'] = self.get_formsets(instance)
        return context

    def form_valid(self, form):
        """
        Validate form and formsets.
        """
        context = self.get_context_data()
        formsets = context['formsets']
        if all(formset.is_valid() for formset in formsets.values()):
            self.object = form.save()
            for formset in formsets.values():
                formset.instance = self.object
                formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


# List View with Table Integration
class SiteInfoListView(SingleTableView):
    model = SiteInfo
    table_class = SiteInfoTable  # Use your defined table class here
    template_name = 'oscar/dashboard/settings/setting_list.html'
    context_object_name = 'site_settings'


class SiteInfoCreateView(FormsetMixin, CreateView):
    model = SiteInfo
    form_class = SiteInfoForm
    formsets_classes = {
        'social_links': SocialMediaLinkFormSet,
        'menu_names': MenuNameFormSet,
        'tags': TagsFormSet,
    }
    template_name = 'oscar/dashboard/settings/manage_site_settings.html'
    success_url = reverse_lazy('site-settings-list')

class SiteInfoUpdateView(FormsetMixin, UpdateView):
    model = SiteInfo
    form_class = SiteInfoForm
    formsets_classes = {
        'social_links': SocialMediaLinkFormSet,
        'menu_names': MenuNameFormSet,
        'tags': TagsFormSet,
    }
    template_name = 'oscar/dashboard/settings/manage_site_settings.html'
    success_url = reverse_lazy('site-settings-list')

# Create and Update Views for SiteInfo with Formset Handling
# class SiteInfoCreateView(FormsetMixin, CreateView):
#     model = SiteInfo
#     form_class = SiteInfoForm
#     formset_class = SocialMediaLinkFormSet
#     template_name = 'oscar/dashboard/settings/manage_site_settings.html'
#     success_url = reverse_lazy('site-settings-list')

# class SiteInfoUpdateView(FormsetMixin, UpdateView):
#     model = SiteInfo
#     form_class = SiteInfoForm
#     formset_class = SocialMediaLinkFormSet
#     template_name = 'oscar/dashboard/settings/manage_site_settings.html'
#     success_url = reverse_lazy('site-settings-list')

class SiteInfoDeleteView(DeleteView):
    model = SiteInfo
    template_name = 'oscar/dashboard/settings/confirm_delete.html'
    success_url = reverse_lazy('site-settings-list')

