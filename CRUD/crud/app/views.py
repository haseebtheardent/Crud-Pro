from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Sum, Count, Avg, Max, Min, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from app.forms import Record
from app.models import RecordTable
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.


def home(request):
    if request.method == 'POST':
        form = Record(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            emaill = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone']
            member = form.cleaned_data['membership']
            db_table = RecordTable(
                first_name=fname, last_name=lname, email=emaill, phone=phone_no, membership=member)
            db_table.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Thank You, your data has been submitted")

    else:
        form = Record()
    record = RecordTable.objects.all()
    return render(request, 'index.html', context={'form': form, 'row': record})


def edit(request, id):
    r = RecordTable.objects.get(pk=id)
    if request.method == 'POST':
        form = Record(request.POST, instance=r)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your Data has been changed Successfully!")
            return redirect('home')
    else:
        form = Record(instance=r)
    record = RecordTable.objects.all()
    return render(request, 'index.html', {'form': form, 'row': record})


def delete(request, id):
    try:
        record = RecordTable.objects.get(pk=id)
        record.delete()
        return redirect('home')
    except RecordTable.DoesNotExist:
        return HttpResponseNotFound("Record not found")


def submit_form(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            form.save()
            # Fetch updated records after saving the new record
            records = YourModel.objects.all()
            return render(request, 'customer_detail.html', {'records': records})
        else:
            # Handle form errors
            return JsonResponse({'error': form.errors}, status=400)
