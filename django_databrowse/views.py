from django.http import Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

###########
# CHOICES #
###########

def choice_list(request, app_label, model_name, field_name, models):
    m, f = lookup_field(app_label, model_name, field_name, models)
    return render_to_response(
        'databrowse/choice_list.html',
        {'model': m, 'field': f}
    )

def choice_detail(request, app_label, model_name, field_name,
                  field_val, models):
    m, f = lookup_field(app_label, model_name, field_name, models)
    try:
        label = dict(f.field.choices)[field_val]
    except KeyError:
        raise Http404('Invalid choice value given')
    obj_list = m.objects(**{f.field.name: field_val})
    numitems = request.GET.get('items')
    items_per_page = [25,50,100]
    if numitems and numitems.isdigit() and int(numitems)>0:
        paginator = Paginator(obj_list, numitems)
    else:
        # fall back to default
        paginator = Paginator(obj_list, items_per_page[0])
    
    page = request.GET.get('page')
    try:
        obj_list_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        obj_list_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page.
        obj_list_page = paginator.page(paginator.num_pages)

    return render_to_response(
        'databrowse/choice_detail.html',
        {
            'model': m,
            'field': f,
            'value': label,
            'object_list': obj_list_page,
            'items_per_page': items_per_page,
        }
    )
