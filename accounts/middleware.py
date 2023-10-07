from django.contrib.auth import logout
from django.utils import timezone
import json
from django.core import signing
from datetime import datetime

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if there's a session
        if request.user.is_authenticated and request.session.get_expiry_age() > 0:
            # Get the last activity timestamp from the session
            last_activity_str = request.session.get('last_activity')

            if last_activity_str is not None:
                try:
                    # Parse the last_activity_str with microseconds and UTC offset
                    last_activity = datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S.%f%z')

                    # Check if the last_activity is a valid datetime object
                    if isinstance(last_activity, datetime):
                        # Calculate the idle time (in seconds) since the last activity
                        idle_time = timezone.now() - last_activity

                        # Log the user out if the idle time exceeds the session timeout
                        if idle_time.seconds > request.session.get_expiry_age():
                            logout(request)
                except ValueError:
                    pass  # Handle invalid datetime format gracefully

        response = self.get_response(request)

        # Update the last activity timestamp in the session as a string with microseconds and UTC offset
        request.session['last_activity'] = str(timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f%z'))

        return response

    def encode(self, obj):
        return json.dumps(obj, separators=(",", ":")).encode("latin-1")

    def decode(self, data):
        return json.loads(data.decode("latin-1"))

    def encode_session(self, session_dict):
        return signing.dumps(session_dict, compress=True, serializer=self.encode)

    def decode_session(self, session_data):
        return signing.loads(session_data, serializer=self.decode, compress=True)
