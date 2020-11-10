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