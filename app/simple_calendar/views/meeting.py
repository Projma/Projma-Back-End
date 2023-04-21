from rest_framework import viewsets
from simple_calendar.models import SimpleCalendar, Meeting
from simple_calendar.serializers.meetingserializers import MeetingSerializer
from rest_framework.permissions import IsAdminUser
from simple_calendar.permissions.calendarpermissions import \
    IsCalendarBoardAdmin, IsCalendarBoardMember, IsCalendarBoardWorkSpaceOwner
from simple_calendar.permissions.meetingpermissions import \
    IsMeetingBoardMember, IsMeetingBoardAdmin, IsMeetingBoardWorkSpaceOwner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import timedelta, datetime, timezone
from simple_calendar.utils import *
from ProjmaBackend.settings import SKYROOM_API_KEY


class CreateMeetingViewSet(viewsets.GenericViewSet):
    queryset = SimpleCalendar.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsCalendarBoardMember | IsCalendarBoardAdmin | IsCalendarBoardWorkSpaceOwner]

    @action(detail=True, methods=['post'], url_path='create-meeting')
    def create_meeting(self, request, pk):
        calendar = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(calendar=calendar, creator=request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
class UpdateMeetingViewSet(viewsets.GenericViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['patch'], url_path='edit-meeting')
    def edit_meeting(self, request, pk):
        meet = self.get_object()
        serializer = self.get_serializer(instance=meet, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class DeleteMeetingViewSet(viewsets.GenericViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['delete'], url_path='delete-meeting')
    def delete_meeting(self, request, pk):
        meet = self.get_object()
        meet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetCalendarMeetingsViewSet(viewsets.GenericViewSet):
    queryset = SimpleCalendar.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsCalendarBoardMember | IsCalendarBoardAdmin | IsCalendarBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='calendar-meetings')
    def get_calendar_meetings(self, request, pk):
        try:
            from_date = (datetime.strptime(request.GET.get('from_date'), "%Y-%m-%d")).date()
            until_date = (datetime.strptime(request.GET.get('until_date'), "%Y-%m-%d")).date()
        except TypeError as e:
            return Response(e.args + ('you may miss the start and end params in query',),
                            status=status.HTTP_400_BAD_REQUEST)

        cal = self.get_object()
        meets = cal.get_meetings(from_date, until_date, True)
        serializer = self.get_serializer(instance=meets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetMeetingViewSet(viewsets.GenericViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='get-meeting', url_name='get-meeting')
    def get_meeting(self, request, pk):
        meet = self.get_object()
        serializer = self.get_serializer(instance=meet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartMeetingViewSet(viewsets.GenericViewSet):
    MAX_MEMBERS = 50
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='start-meeting')
    def start_meeting(self, request, pk):
        meet = self.get_object()
        if meet.status != Meeting.NOTSTARTED:
            return Response(f'Meeting is {meet.status}', status=status.HTTP_400_BAD_REQUEST)
        if meet.repeat == 0 and datetime.now().date() != meet.from_date:
            return Response(f'Start is available only in {meet.from_date}', status=status.HTTP_400_BAD_REQUEST)
        if (datetime.now() + timedelta(minutes=5)).time() < meet.start:
            return Response(f'Start will be available 5 minutes befor {meet.start}', status=status.HTTP_400_BAD_REQUEST)

        sky = SkyroomAPI(SKYROOM_API_KEY)
        create_room_params = {
            'name': f'{meet.title}-{meet.id}',
            'title': meet.title,
            'guest_login':  True,
            'op_login_first': False,
            'max_users': 0
            }
        try:
            roomid = sky.createRoom(create_room_params)
        except APIException as e:
            return Response(f'Failed to create room: {str(e)}', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPException:
            return Response(f'Request failed', status=status.HTTP_503_SERVICE_UNAVAILABLE)

        create_link_params = {
            "room_id": roomid,
            "user_id": "teammember",
            "nickname": "teammember",
            "access": 3,
            "concurrent": 10,
            "language": "fa",
            "ttl": 7200
        }

        try:
            link = sky.createLoginUrl(create_link_params)
        except APIException as e:
            sky.deleteRoom({'room_id': roomid})
            return Response(f'Failed to get login url: {str(e)}', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPException:
            sky.deleteRoom({'room_id': roomid})
            return Response(f'Request failed', status=status.HTTP_503_SERVICE_UNAVAILABLE)

        meet.room_id = roomid
        meet.link = link
        meet.status = Meeting.HOLDING
        meet.save()
        return Response(self.get_serializer(instance=meet).data, status=status.HTTP_200_OK)


class EndMeetingViewSet(viewsets.GenericViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='end-meeting')
    def end_meeting(self, request, pk):
        meet = self.get_object()
        sky = SkyroomAPI(SKYROOM_API_KEY)
        params = dict()
        params['room_id'] = meet.room_id
        try:
            result = sky.deleteRoom(params)
        except APIException as e:
            return Response(f'Failed to delete room: {str(e)}', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPException:
            return Response(f'Request failed', status=status.HTTP_503_SERVICE_UNAVAILABLE)

        meet.status = Meeting.FINISHED if meet.repeat == 0 else Meeting.NOTSTARTED
        meet.save()
        print(self.get_serializer(instance=meet).data)
        return Response(self.get_serializer(instance=meet).data, status=status.HTTP_200_OK)
