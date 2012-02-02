from django.http import HttpResponse
import simplejson

def full(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
    return response

def group(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
    return response

def trait(request):
    response = HttpResponse(mimetype='application/json')
    response.content = simplejson.dump(data)
