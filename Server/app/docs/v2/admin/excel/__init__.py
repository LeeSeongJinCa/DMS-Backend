from app.docs.v2 import jwt_header


def generate_excel_doc(type):
    return {
        'tags': ['[Admin] 신청 정보'],
        'description': '{}신청 정보를 다운로드합니다.'.format(type),
        'parameters': [jwt_header],
        'responses': {
            '200': {
                'description': '{}신청 정보가 담긴 엑셀 파일과 Cache-Control: no-cache 헤더를 함께 응답합니다.'.format(type)
            },
            '403': {
                'description': '권한 없음'
            }
        }
    }
