from rest_framework import serializers

class TestSerializer(serializers.Serializer):
    post_message =  serializers.CharField(max_length=256)

    def complete_task_and_get_data(self):
        return {"request_message": self.validated_data["post_message"]}