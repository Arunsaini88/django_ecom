from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from .models import SiteInfo
from .forms import SiteInfoForm, SocialMediaLinkFormSet
from .tables import SiteInfoTable  # Assuming you have defined a table class

# Mixin for handling formsets
class FormsetMixin:
    formset_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = self.formset_class(self.request.POST, instance=self.object)
        else:
            context['formset'] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
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

# Create and Update Views for SiteInfo with Formset Handling
class SiteInfoCreateView(FormsetMixin, CreateView):
    model = SiteInfo
    form_class = SiteInfoForm
    formset_class = SocialMediaLinkFormSet
    template_name = 'oscar/dashboard/settings/manage_site_settings.html'
    success_url = reverse_lazy('site-settings-list')

class SiteInfoUpdateView(FormsetMixin, UpdateView):
    model = SiteInfo
    form_class = SiteInfoForm
    formset_class = SocialMediaLinkFormSet
    template_name = 'oscar/dashboard/settings/manage_site_settings.html'
    success_url = reverse_lazy('site-settings-list')

class SiteInfoDeleteView(DeleteView):
    model = SiteInfo
    template_name = 'oscar/dashboard/settings/confirm_delete.html'
    success_url = reverse_lazy('site-settings-list')



# from django.urls import reverse_lazy
# from django.views.generic import CreateView, UpdateView, DeleteView, ListView
# from django_tables2 import SingleTableView
# from settings.models import SiteInfo, SocialMediaLink
# from .forms import SiteInfoForm, SocialMediaLinkFormSet
# from .tables import SiteInfoTable


# class SiteInfoListView(SingleTableView):
#     model = SiteInfo
#     table_class = SiteInfoTable
#     template_name = 'oscar/dashboard/settings/setting_list.html'


# class SiteInfoCreateView(CreateView):
#     model = SiteInfo
#     form_class = SiteInfoForm
#     template_name = 'oscar/dashboard/settings/manage_site_settings.html'
#     success_url = reverse_lazy('site-settings-list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['social_media_links'] = SocialMediaLinkFormSet(self.request.POST, prefix="social_links")
#         else:
#             context['social_media_links'] = SocialMediaLinkFormSet(prefix="social_links")
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         social_media_links = context['social_media_links']
#         if social_media_links.is_valid():
#             self.object = form.save()
#             social_media_links.instance = self.object
#             social_media_links.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)


# class SiteInfoUpdateView(UpdateView):
#     model = SiteInfo
#     form_class = SiteInfoForm
#     template_name = 'oscar/dashboard/settings/manage_site_settings.html'
#     success_url = reverse_lazy('site-settings-list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['social_media_links'] = SocialMediaLinkFormSet(self.request.POST, instance=self.object, prefix="social_links")
#         else:
#             context['social_media_links'] = SocialMediaLinkFormSet(instance=self.object, prefix="social_links")
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         social_media_links = context['social_media_links']
#         if social_media_links.is_valid():
#             self.object = form.save()
#             social_media_links.instance = self.object
#             social_media_links.save()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)


# class SiteInfoDeleteView(DeleteView):
#     model = SiteInfo
#     template_name = 'oscar/dashboard/settings/confirm_delete.html'
#     success_url = reverse_lazy('site-settings-list')



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import SiteInfo
# from .forms import SiteInfoForm, SocialMediaLinkFormSet

# # Create or Update View
# def manage_site_settings(request, pk=None):
#     if pk:
#         site_settings = get_object_or_404(SiteInfo, pk=pk)
#     else:
#         site_settings = SiteInfo()

#     if request.method == 'POST':
#         form = SiteInfoForm(request.POST, request.FILES, instance=site_settings)
#         formset = SocialMediaLinkFormSet(request.POST, instance=site_settings)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('site-settings-list')
#     else:
#         form = SiteInfoForm(instance=site_settings)
#         formset = SocialMediaLinkFormSet(instance=site_settings)
    
#     return render(request, 'oscar/dashboard/settings/manage_site_settings.html', {'form': form, 'formset': formset})

# # List View
# def site_settings_list(request):
#     site_settings = SiteInfo.objects.all()
#     return render(request, 'oscar/dashboard/settings/setting_list.html', {'site_settings': site_settings})

# # Delete View
# def delete_site_settings(request, pk):
#     site_settings = get_object_or_404(SiteInfo, pk=pk)
#     if request.method == 'POST':
#         site_settings.delete()
#         return redirect('site-settings-list')
#     return render(request, 'oscar/dashboard/settings/confirm_delete.html', {'object': site_settings})
