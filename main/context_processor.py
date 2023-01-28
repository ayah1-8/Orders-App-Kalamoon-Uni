

def Annual_id(request):

    id = request.session['annual_id']
    return {'need_id': id}