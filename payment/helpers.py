from django.db.models import F

from payment.models import Cashier, PaymentLog


def payment_income(amount, payment_method, comment,
                   user, aor=False, outcat=0, outlay=0, **kwargs):
    """
    Create PaymentLog object for income cash payment
     1 -> order
    :param amount:
    :param payment_type:
    :param payment_method:
    :param comment:
    :param user: -> user_id
    :param aor: -> Исключить из отчёта
    :param outcat:
    :param outlay:
    :return:
    """

    if outcat == 1:
        comment += " Оплата за заказ №{}".format(outlay)

    if payment_method == 'cash' and float(amount) > 0:
        Cashier.objects.filter(payment_type='uzs').update(amount=F('amount') + float(amount))
    elif payment_method == 'card' and float(amount) > 0:
        Cashier.objects.filter(payment_type='card').update(amount=F('amount') + float(amount))

    PaymentLog.objects.create(
        amount=amount,
        payment_method=payment_method,
        outcat=outcat,
        outlay=outlay,
        outlay_child=kwargs.get('outlay_child', 0),
        comment=comment,
        user=user,
        aor=aor,
        payment_log_type='income'
    )


def payment_outcome(amount, payment_method, comment,
                    user, aor=False, outcat=0, outlay=0, **kwargs):
    """
    Create PaymentLog object for income cash payment
     1 -> outlay
     2 -> salary_worker
     3 -> order
     4 -> counterparty
     5- > student
     8 -> car
     9 -> worker
    :param amount:
    :param payment_type:
    :param payment_method:
    :param comment:
    :param user: -> user_id
    :param aor: -> Исключить из отчёта
    :param outcat:
    :param outlay:
    :return:
    """
    if outcat == 1:
        comment += " Расход за {}".format(kwargs['outlay_name'])
    elif outcat == 2:
        comment += " Зарплата сотрудника {}".format(kwargs['worker'])
    elif outcat == 3:
        comment += " Расход за заказ №{}".format(outlay)

    if payment_method == 'cash' and float(amount) > 0 and outcat < 9:
        Cashier.objects.filter(payment_type='uzs').update(amount=F('amount') - float(amount))
    elif payment_method == 'enumeration' and float(amount) > 0:
        Cashier.objects.filter(payment_type='card').update(amount=F('amount') - float(amount))

    PaymentLog.objects.create(
        amount=amount,
        payment_method=payment_method,
        outcat=outcat,
        outlay=outlay,
        outlay_child=kwargs.get('outlay_child', 0),
        comment=comment,
        user=user,
        aor=aor,
        payment_log_type='outcome'
    )
