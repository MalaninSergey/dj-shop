# Django imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView

# Project imports
from .models import Product, Category
from .forms import ProductForm


def orders(request):
    if request.user.is_authenticated:
        ord = Product.objects.filter(in_or=True)
        return render(request, 'zxc.html', {'object_list': ord})
    else:
        return redirect('/')

def sn(request):
    return render(request, 'mnb.html')

class IndexView(ListView):
    template_name = 'product_manager/index.html'

    def get_queryset(self):
        return Product.objects.order_by('-id')[:10]


class ProductListView(ListView):
    """ Allows you to list all products. """
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm


class ProductDetailView(DetailView):
    """ Allows you to view detailed information about an object in Product. """
    model = Product


class ProductDeleteView(DeleteView):
    """ Allows you to delete a product. """
    model = Product
    success_url = reverse_lazy('product_manager_product_list')


class ProductUpdateView(UpdateView):
    """ Allows you to update a product's details. """
    model = Product
    form_class = ProductForm


class CategoryListView(ListView):
    """ Allows you to view all categories. """
    model = Category


class CategoryDetailView(DetailView):
    """ Allows you to view details of a category (will be used for inline product display). """
    model = Category

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the current category taken from above context.
        context['products_in_category'] = Product.objects.filter(category=context['object'])
        return context
