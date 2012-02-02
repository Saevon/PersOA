from django.http import HttpResponse
import simplejson

def trait_groups(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
    return response

def traits(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
    return response

def choices(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
    return response

