from django.core.mail import EmailMultiAlternatives
from django.template import loader

def is_valid_national_code(national_code: str):
    if not len(national_code) == 10:
        return False
    wrong_code = [
        '0000000000', '1111111111', '2222222222', '3333333333', '4444444444', '5555555555',
        '6666666666', '7777777777', '8888888888', '9999999999'
    ]

    if national_code in wrong_code:
        return False

    if not national_code.isdigit():
        return False

    check = int(national_code[9])
    temp1 = sum([int(national_code[x]) * (10 - x) for x in range(9)])
    temp2 = temp1 % 11

    if temp2 == 0 and check == temp2:
        return True
    if temp2 == 1 and check == 1:
        return True
    if temp2 > 1 and check == abs(temp2 - 11):
        return True
    return False


def send_email(subject, template_name_html, template_name_text, data, to):
    html = loader.get_template(template_name_html)
    text = loader.get_template(template_name_text)

    content_html = html.render(data)
    content_text = text.render(data)
    msg = EmailMultiAlternatives(
        subject,
        content_text,
        'gizshopteam@gmail.com',
        [to]
    )
    msg.attach_alternative(content_html, "text/html")
    msg.send()
