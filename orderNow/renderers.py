"""
Custom Renderer Module
"""

from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    """
    Custom renderer class for json response
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders data into JSON
        """

        status_code = renderer_context["response"].status_code
        response = {"status": "success", "data": data, "message": None}

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            if "detail" in data:
                response["message"] = data["detail"]
                response["data"] = None

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
