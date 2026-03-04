from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Breed
from .forms import BreedForm


# ================= USER =================

@login_required
def breed_list(request):
    query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'All')

    breeds = Breed.objects.filter(is_active=True)

    if query:
        breeds = breeds.filter(
            Q(name__icontains=query) |
            Q(origin_location__icontains=query)
        )

    if category_filter != 'All':
        breeds = breeds.filter(category=category_filter)

    return render(request, 'breeds/breed_list.html', {
        'breeds': breeds,
        'query': query,
        'category_filter': category_filter,
        'total_count': breeds.count(),
    })


@login_required
def user_breed_detail(request, pk):
    breed = get_object_or_404(Breed, pk=pk, is_active=True)
    return render(request, 'breeds/user_breed_detail.html', {
        'breed': breed
    })


# ================= ADMIN =================

@staff_member_required
def admin_breed_detail(request, pk):
    breed = get_object_or_404(Breed, pk=pk)
    return render(request, 'breeds/admin_breed_detail.html', {
        'breed': breed
    })


@staff_member_required
def admin_breed_manage(request):
    breeds = Breed.objects.all().order_by('name')
    return render(request, 'breeds/admin_breed_manage.html', {
        'breeds': breeds
    })


@staff_member_required
def add_breed(request):
    if request.method == 'POST':
        form = BreedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Breed added successfully.")
            return redirect('breeds:admin_breed_manage')
    else:
        form = BreedForm()

    return render(request, 'breeds/add_breed.html', {
        'form': form
    })


# ✅ EDIT

@staff_member_required
def edit_breed(request, pk):
    breed = get_object_or_404(Breed, pk=pk)

    if request.method == 'POST':
        form = BreedForm(request.POST, request.FILES, instance=breed)
        if form.is_valid():
            form.save()
            messages.success(request, "Breed updated successfully.")
            return redirect('breeds:admin_breed_manage')
    else:
        form = BreedForm(instance=breed)

    return render(request, 'breeds/add_breed.html', {
        'form': form,
        'edit_mode': True,
        'breed': breed
    })


# ✅ DELETE

@staff_member_required
def delete_breed(request, pk):
    breed = get_object_or_404(Breed, pk=pk)

    if request.method == "POST":
        breed.delete()
        messages.success(request, "Breed deleted.")
        return redirect('breeds:admin_breed_manage')

    return render(request, 'breeds/confirm_delete.html', {
        'breed': breed
    })
