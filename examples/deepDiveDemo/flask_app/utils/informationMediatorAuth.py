import os


def validate_information_mediator_header(header_value): 
    EXPECTED_CLIENT_HEADER = os.getenv('EXPECTED_CLIENT_HEADER', None)

    if not EXPECTED_CLIENT_HEADER or (header_value != EXPECTED_CLIENT_HEADER):
        return {'success': False, "error": "Unauthorized"}
    
    return {'success': True} 
