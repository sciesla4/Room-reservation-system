from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from reservation.models import *
import datetime


class Index(View):

    def get(self, request):
        return render(request, template_name="index.html")

    def post(self, request):
        room_name = request.POST.get('room_name')
        room_places = request.POST.get('room_places')
        projector = request.POST.get('projector')
        room_places = int(room_places)

        rooms = Room.objects.all()

        if projector:
            rooms = rooms.filter(project_available=True)
        if room_places:
            rooms = rooms.filter(room_places__gte=room_places)
        if room_name:
            rooms = rooms.filter(room_name__contains=room_name)
        for room in rooms:
            reservation_dates = [reservation.data for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates

        return render(request, template_name="search.html", context={"rooms" : rooms, "date": datetime.date.today()})

    class Add_room(View):

        def get(self, request):
            return render(request, template_name="add_room.html")

        def post(self, request):
            room_name = request.POST.get('room_name')
            room_places = request.POST.get('room_places')
            projector_true = request.POST.get('projector_true')
            projector_false = request.POST.get('projector_false')
            room_places = int(room_places)

            # Checking if name of room is not empty
            if not room_name:
                return HttpResponse('The room need a name')
            # Checking if nr of places are positive
            if room_places <= 0:
                return HttpResponse('The room can not have negative places')
            # Checking if chebox take only one value
            if projector_true is None and projector_false is None:
                return HttpResponse('Projector can only have one option')
            if projector_true == '1' and projector_false == '1':
                return HttpResponse('Projector can only have one option')

            if projector_true == '1':
                projector = True
            elif projector_false == '1':
                projector = False

            # Checking if room exist in database, if not we add it to DB
            if Room.objects.filter(room_name=room_name).exists():
                return HttpResponse('Room already exist')
            else:
                Room.objects.create(room_name=room_name, room_places=room_places, project_available=projector)

            return redirect('index')

    class All_room(View):
        def get(self, request):
            rooms = Room.objects.all()
            for room in rooms:
                reservation_dates = [reservation.data for reservation in room.reservation_set.all()]
                room.reserved = datetime.date.today() in reservation_dates
            return render(request, "all_room.html", context={"all_rooms": rooms})

    class Delete_room(View):
        def get(self, request, id):
            room_to_delete = Room.objects.get(pk=id)
            room_to_delete.delete()

            return redirect('all_room')

    def room_modify(request, id):
        if request.method == 'GET':
            room_to_modify = Room.objects.get(pk=id)
            context = {'room_to_modify': room_to_modify}
            return render(request, template_name='room_modify.html', context=context)

        else:
            room_to_modify = Room.objects.get(pk=id)
            room_name = request.POST.get('room_name')
            room_places = request.POST.get('room_places')
            projector_true = request.POST.get('projector_true')
            projector_false = request.POST.get('projector_false')
            room_places = int(room_places)

            # Checking if name of room is not empty
            if not room_name:
                return HttpResponse('The room need a name')
            # Checking if nr of places are positive
            if room_places <= 0:
                return HttpResponse('The room can not have negative places')
            # Checking if chebox take only one value
            if projector_true is None and projector_false is None:
                return HttpResponse('Projector can only have one option')
            if projector_true == '1' and projector_false == '1':
                return HttpResponse('Projector can only have one option')

            if projector_true == '1':
                projector = True
            elif projector_false == '1':
                projector = False

            if Room.objects.filter(room_name=room_name).exists():
                return HttpResponse('Room already exist')
            else:
                room_to_modify.room_name = room_name
                room_to_modify.room_places = room_places
                room_to_modify.project_available = projector
                room_to_modify.save()


            return redirect('all_room')

    def room_reservation(request, id):
        if request.method == 'GET':
            room_reservation = Room.objects.get(pk=id)
            reservations = room_reservation.reservation_set.all()
            context = {'room_reservation': room_reservation, 'reservations': reservations}
            return render(request, template_name='room_reservation.html', context=context)

        else:
            book_date = request.POST.get('booking_date')
            comment = request.POST.get('comment')

            if Reservation.objects.filter(data=book_date).exists():
                return HttpResponse("The room at this date is already booked")
            elif book_date < str(datetime.date.today()):
                return HttpResponse("The date can not be past")
            else:
                Reservation.objects.create(data=book_date, comment=comment, room_id_id=id)

            return redirect('all_room')

    def room_detail(request, id):
        room = Room.objects.get(pk=id)
        reservations = room.reservation_set.filter(data__gte=str(datetime.date.today())).order_by('data')
        context = {'room': room, 'reservations': reservations}
        return render(request, template_name='details_room.html', context=context)

