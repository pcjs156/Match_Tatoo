# 이미 카카오 인증을 마친 유저가 인증을 시도하는 경우 발생
class AlreadyAuthenticatedCustomer(Exception):
    pass