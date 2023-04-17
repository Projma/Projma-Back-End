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
