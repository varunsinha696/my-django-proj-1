from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ProductInfoTemp
from .forms import ProductInfoForm
from user_access.models import CustomUser, ProductMain
from .models import SSO, MFA
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import ProductMain, SSO, SSOTemp, Notification
from .forms import SSOForm

@login_required
def update_sso(request, product_id):
    if not request.user.role == 'Manager':  # Ensure only managers can access this function
        return HttpResponseForbidden("You do not have permission to perform this action.")

    product = get_object_or_404(ProductMain, id=product_id)
    sso = product.sso
    if request.method == 'POST':
        form = SSOForm(request.POST, instance=sso)
        if form.is_valid():
            temp_sso = SSOTemp.objects.create(
                product=product,
                sso_implemented=form.cleaned_data['sso_implemented'],
                sso_date=form.cleaned_data['sso_date'],
                sso_description=form.cleaned_data['sso_description'],
                updated_by=request.user
            )
            # Send notification to Auditor
            Notification.objects.create(
                sender=request.user,
                recipient=CustomUser.objects.get(role='Auditor'),
                message=f"SSO update requested for product: {product.product}"
            )
            return redirect('sso_list')
    else:
        form = SSOForm(instance=sso)

    return render(request, 'sso/update_sso.html', {'form': form, 'product': product})

@login_required
def review_sso(request, temp_id):
    if not request.user.role == 'Auditor':  # Ensure only auditors can access this function
        return HttpResponseForbidden("You do not have permission to perform this action.")

    temp_record = get_object_or_404(SSOTemp, id=temp_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        if action == 'Approve':
            # Update the main SSO table
            SSO.objects.filter(product=temp_record.product).update(
                sso_implemented=temp_record.sso_implemented,
                sso_date=temp_record.sso_date,
                sso_description=temp_record.sso_description
            )
            temp_record.status = 'Approved'
            temp_record.save()

            # Log and notify
            Notification.objects.create(
                sender=request.user,
                recipient=temp_record.updated_by,
                message=f"SSO update for {temp_record.product.product} approved."
            )

        elif action == 'Reject':
            temp_record.status = 'Rejected'
            temp_record.save()

            # Log and notify
            Notification.objects.create(
                sender=request.user,
                recipient=temp_record.updated_by,
                message=f"SSO update for {temp_record.product.product} rejected. Remarks: {remarks}"
            )

        return redirect('sso_list')

    return render(request, 'sso/review_sso.html', {'temp_record': temp_record})

@login_required
def notifications(request):
    user_notifications = request.user.received_notifications.all()
    return render(request, 'sso/notifications.html', {'notifications': user_notifications})



class SSOListView(ListView):
    model = SSO
    template_name = 'sso/sso_list.html'
    context_object_name = 'sso_records'

    def get_queryset(self):
        return SSO.objects.filter(product__decommissioned=False)

class MFAListView(ListView):
    model = MFA
    template_name = 'mfa/mfa_list.html'
    context_object_name = 'mfa_records'

    def get_queryset(self):
        return MFA.objects.filter(product__decommissioned=False)

# Mixins for Role-Based Access Control
class AuditorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'Auditor'


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'Manager'


# List View
class ProductInfoListView(LoginRequiredMixin, ListView):
    model = ProductMain
    template_name = 'product_app/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Viewer':
            return ProductMain.objects.filter(decommissioned=False)
        elif user.role == 'Manager':
            return ProductMain.objects.filter(manager=user, decommissioned=False)
        elif user.role == 'Auditor':
            return ProductMain.objects.all()
        return ProductMain.objects.none()


# Create View
class ProductInfoCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = ProductMain
    form_class = ProductInfoForm
    template_name = 'product_app/product_form.html'
    success_url = reverse_lazy('product_list')


# Update View
class ProductInfoUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = ProductMain
    form_class = ProductInfoForm
    template_name = 'product_app/product_form.html'
    success_url = reverse_lazy('product_list')


# Soft Delete View (Move to Temp Table)
class ProductInfoDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = ProductMain
    template_name = 'product_app/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        product_info = self.get_object()
        # Move record to the temporary table before deletion
        ProductInfoTemp.objects.create(
            product=product_info.product,
            description=product_info.description,
            date_of_initiation=product_info.date_of_initiation,
            sso_implemented=product_info.sso_implemented,
            deleted_by_manager=True
        )
        product_info.delete()
        return redirect(self.success_url)


# List View for Auditors to review decommissioned products
class ProductInfoTempListView(LoginRequiredMixin, AuditorRequiredMixin, ListView):
    model = ProductInfoTemp
    template_name = 'product_app/temp_product_list.html'
    context_object_name = 'temp_products'


