import logging
import os


class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.session.headers.update(self.base_headers)
        self.logger = logging.getLogger(__name__)

    def send_request(
        self,
        method,
        endpoint,
        data=None,
        params=None,
        expected_status=200,
        need_logging=True,
    ):
        url = f"{self.base_url}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
        )

        if need_logging:
            self.log_request_and_response(response)

        assert response.status_code == expected_status, (
            f"Unexpected status code: {response.status_code}. "
            f"Expected: {expected_status}. "
            f"Response: {response.text}"
        )

        return response

    def update_session_headers(self, headers):
        self.session.headers.update(headers)

    def log_request_and_response(self, response):
        request = response.request

        self.logger.info(
            "\n%s\n%s %s\nRequest body: %s\n"
            "Status code: %s\nResponse: %s",
            os.environ.get("PYTEST_CURRENT_TEST", ""),
            request.method,
            request.url,
            request.body,
            response.status_code,
            response.text,
        )