from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import MenuNote
from .serializers import MenuNoteSerializer
import json

# Create your views here.


# http://servername:port/ api/menunote/?n_table=12&num=5            -> load first 5 of Table 12
# http://servername:port/ api/menunote/?n_table=Take-Home&num=3     -> load first 3 of Take-Home
# http://servername:port/ api/menunote/?num=3                       -> loads first 3 of all table
# http://servername:port/ api/menunote/                             -> loads first 5 of all table
@api_view(['GET'])
def MenuNoteRequest(request, mn_table=None, num=3): # mn_queue is sorted by default, num can be any integer
    if request.method == 'GET' and 'mn_table' in request.GET:
        try:
            res = "[ "
            mn_table = request.GET.get('mn_table')
            if 'num' in request.GET:
                q_to_display = int(request.GET.get('num'))
            else:
                q_to_display = 5 # 5 first existing queue
            if mn_table:
                q_list = MenuNote.objects.filter(mn_table=mn_table)[:q_to_display]
                for que in q_list:
                    res+= json.dumps( json.loads( que.json_get() ) )
                    print(res)
                    if que!=q_list[min(q_to_display,len(q_list))-1]:
                        res+=", "
            res+=" ]"
            return HttpResponse( json.dumps( json.loads(res) ), content_type="application/json")

        except ObjectDoesNotExist:
            raise Http404("No MenuNote Queue matches the given query.")

    if request.method == 'GET' and 'mn_table' not in request.GET:
        try:
            res = "[ "
            if 'num' in request.GET:
                q_to_display = int(request.GET.get('num'))
            else:
                q_to_display = 5 # 5 first existing queue
            q_list = MenuNote.objects.filter()[:q_to_display]
            for que in q_list:
                res+= json.dumps( json.loads( que.json_get() ) )
                print(res)
                if que!=q_list[min(q_to_display,len(q_list))-1]:
                    res+=", "
            res+=" ]"
            return HttpResponse( json.dumps( json.loads(res) ), content_type="application/json")

        except ObjectDoesNotExist:
            raise Http404("No MenuNote Queue matches the given query.")


# http://servername:port/ api/add/menunote/
@api_view(['PUT'])
def MenuNotePost(request, pk):
    try: 
        menunote = MenuNote.objects.get(pk=pk) 
    except MenuNote.DoesNotExist:
        Http404("Contact Panpakorn should this happens")
    if request.method == 'PUT':
        menunote_data = JSONParser().parse(request)
        menunote_serializer = MenuNoteSerializer(menunote, data=menunote_data)
        if menunote_serializer.is_valid(): 
            menunote_serializer.save()
            return Response(menunote_serializer.data, status=status.HTTP_201_CREATED)
        return Response(menunote_serializer.errors, status=status.HTTP_400_BAD_REQUEST)