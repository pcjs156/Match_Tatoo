from Crypto.Cipher import AES

from match_tattoo.settings import SECRET_KEY

from .models import Customer
from .forms import CustomerSignUpForm, TattooistSignUpForm

CHECK_LIST = ("username", "password", "email", "nickname", "unknown")


class UserSignupChecker:
    def __init__(self, signup_form: TattooistSignUpForm, default=False, default_status=True):
        # 만약 모든 검증 값이 default_status인 기본 Checker를 원하는 경우
        if default is True:
            self.username = default_status
            self.password = default_status
            self.email = default_status
            self.nickname = default_status
            self.unknown = default_status
        else:
            # 우선 모두 문제가 있는 것으로 표시하고,
            # check 메서드의 검증이 항목별로 끝날 때마다 True로 갱신해줌
            self.username = False
            self.password = False
            self.email = False
            self.nickname = False
            self.unknown = False

            self.check(signup_form)

    # 항목의 유효성을 True로 갱신
    def check(self, signup_form: TattooistSignUpForm):
        # username, email, nickname: 다른 사용자와 같은지 검사
        # password: password1과 password2가 다른지 검사
        # unknown: 알 수 없는 오류

        # 입력된 정보 목록
        new_username = signup_form.data["username"]
        new_password1 = signup_form.data["password1"]
        new_password2 = signup_form.data["password2"]
        new_email = signup_form.data["email"]
        new_nickname = signup_form.data["nickname"]

        # 모든 Customer
        all_customers = Customer.objects.all()

        # username
        if new_username not in list(customer.username for customer in all_customers):
            self.username = True

        # email
        if new_email not in list(customer.email for customer in all_customers):
            self.email = True

        # nickname
        if new_nickname not in list(customer.nickname for customer in all_customers):
            self.nickname = True

        # password
        if new_password1 == new_password2:
            self.password = True

        if signup_form.is_valid():
            self.unknown = True

        print(self.username)
        print(self.email)
        print(self.nickname)
        print(self.password)
        print(self.unknown)

    def is_valid(self):
        return self.username and self.password and self.email and self.nickname and self.unknown

    class UserSignupChecker:
        def __init__(self, signup_form: CustomerSignUpForm, default=False, default_status=True):
            # 만약 모든 검증 값이 default_status인 기본 Checker를 원하는 경우
            if default is True:
                self.username = default_status
                self.password = default_status
                self.email = default_status
                self.nickname = default_status
                self.unknown = default_status
            else:
                # 우선 모두 문제가 있는 것으로 표시하고,
                # check 메서드의 검증이 항목별로 끝날 때마다 True로 갱신해줌
                self.username = False
                self.password = False
                self.email = False
                self.nickname = False
                self.unknown = False

                self.check(signup_form)

        # 항목의 유효성을 True로 갱신
        def check(self, signup_form: CustomerSignUpForm):
            # username, email, nickname: 다른 사용자와 같은지 검사
            # password: password1과 password2가 다른지 검사
            # unknown: 알 수 없는 오류

            # 입력된 정보 목록
            new_username = signup_form.data["username"]
            new_password1 = signup_form.data["password1"]
            new_password2 = signup_form.data["password2"]
            new_email = signup_form.data["email"]
            new_nickname = signup_form.data["nickname"]

            # 모든 Customer
            all_customers = Customer.objects.all()

            # username
            if new_username not in list(customer.username for customer in all_customers):
                self.username = True

            # email
            if new_email not in list(customer.email for customer in all_customers):
                self.email = True

            # nickname
            if new_nickname not in list(customer.nickname for customer in all_customers):
                self.nickname = True

            # password
            if new_password1 == new_password2:
                self.password = True

            if signup_form.is_valid():
                self.unknown = True

            print(self.username)
            print(self.email)
            print(self.nickname)
            print(self.password)
            print(self.unknown)

        def is_valid(self):
            return self.username and self.password and self.email and self.nickname and self.unknown

# plain_text의 길이가 multiple_of의 배수인 경우 그대로 리턴해주고
# 만약 배수가 아닌 경우 한 번 더 multiple_of만큼 더한?길이로 p를 더해 맞춰줌
# 뭔가 잘못되면 None을 리턴
def padding_to_multiple_of(plain_text: str, p='*', multiple_of=16):
    class InvalidPaddingCharLength(Exception):
        pass

    try:
        if len(p) != 1:
            raise InvalidPaddingCharLength
        else:
            if len(plain_text) % multiple_of == 0:
                return plain_text
            else:
                required_padding_length = ((len(plain_text)//16) + 1) * 16 - len(plain_text)
                return plain_text + (p * required_padding_length)

    except InvalidPaddingCharLength:
        print(f"The length of p is not 1: {p}")
        return None

# 평문에 첨가된 padding을 빼줌
def remove_padding(padded_text: str, p="*") -> str:
    return ''.join(padded_text.split('*'))

# secret key로부터 24자리의 AES 대칭 키를 생성
def get_AES_symmetric_key():
    return SECRET_KEY["SECRET_KEY"][:-2:2]

# 카카오 코드 암호화
def kakao_encrypt(plain: str) -> bytes:
    crypto_obj =AES.new(get_AES_symmetric_key().encode("utf8"), AES.MODE_ECB)
    padded_plain = padding_to_multiple_of(plain)
    return crypto_obj.encrypt(padded_plain.encode("utf8"))

# 카카오 코드 복호화
def kakao_decrypt(crypto: bytes) -> str:
    crypto_obj =AES.new(get_AES_symmetric_key().encode("utf8"), AES.MODE_ECB)
    return remove_padding(crypto_obj.decrypt(crypto).decode("utf8"))