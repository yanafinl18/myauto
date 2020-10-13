import requests

# что такое url_payload ?
# что нужно сделать с expected_response_codes

def parametrized_get(endpoint=None, url_payload=None, header_payload=None, expected_response_codes=None, host=None,
                     timeout=60):

    response = requests.get(host + endpoint, params=url_payload, headers=header_payload, timeout=timeout)
    assert response.status_code == expected_response_codes or 200, "Success!"
    return response

def parametrized_post(endpoint=None, url_payload=None, data=None, body_payload=None, files=None, header_payload=None,
                      expected_response_codes=None, host=None, timeout=60):
    response = requests.post(host + endpoint, params=url_payload, headers=header_payload, data=data, json=body_payload,
                             files=files, timeout=timeout)
    assert response.status_code == expected_response_codes or 200, "Success!"
    return response


