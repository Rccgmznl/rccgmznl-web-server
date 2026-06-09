from rest_framework.renderers import JSONRenderer


class StandardizedJSONRenderer(JSONRenderer):
    """Wrap successful API responses in a consistent envelope."""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = None
        if renderer_context is not None:
            response = renderer_context.get("response")

        status_code = 200
        if response is not None:
            status_code = response.status_code

        if data is None:
            data = {}

        if status_code >= 400:
            if isinstance(data, dict) and {
                "success",
                "status_code",
                "errors",
            }.issubset(data.keys()):
                payload = data
            else:
                payload = {
                    "success": False,
                    "status_code": status_code,
                    "errors": data,
                }
        else:
            payload = {
                "success": True,
                "status_code": status_code,
                "data": data,
            }

        return super().render(
            payload,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
