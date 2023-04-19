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

# class NewCommentViewSet(viewsets.GenericViewSet):
#     queryset = Task.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAdminUser | IsTaskBoardMember | IsTaskBoardAdmin | IsTaskBoardWorkSpaceOwner]
#     @action(detail=True, methods=['post'], url_path='new-comment')
#     def new_comment(self, request, pk):
#         task = self.get_object()
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(task=task,sender=request.user.profile)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            from_date = datetime.strptime(request.GET.get('from_date'), "%Y-%m-%d")
            until_date = datetime.strptime(request.GET.get('until_date'), "%Y-%m-%d")
        except TypeError as e:
            return Response(e.args + ('you may miss the start and end params in query',),
                            status=status.HTTP_400_BAD_REQUEST)

        cal = self.get_object()
        serializer = self.get_serializer(instance=cal.get_meetings(from_date, until_date), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartMeetingViewSet(viewsets.GenericViewSet):
    MAX_MEMBERS = 50
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAdminUser | IsMeetingBoardMember | IsMeetingBoardAdmin | IsMeetingBoardWorkSpaceOwner]

    @action(detail=True, methods=['get'], url_path='start-meeting')
    def start_meeting(self, request, pk):
        meet = self.get_object()
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
            print(create_link_params)
            link = sky.createLoginUrl(create_link_params)
        except APIException as e:
            sky.deleteRoom({'room_id': roomid})
            return Response(f'Failed to get login url: {str(e)}', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPException:
            sky.deleteRoom({'room_id': roomid})
            return Response(f'Request failed', status=status.HTTP_503_SERVICE_UNAVAILABLE)

        meet.room_id = roomid
        meet.link = link
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
        print(params)
        try:
            result = sky.deleteRoom(params)
        except APIException as e:
            return Response(f'Failed to delete room: {str(e)}', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPException:
            return Response(f'Request failed', status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(self.get_serializer(instance=meet).data, status=status.HTTP_200_OK)
