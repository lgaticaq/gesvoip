from django.conf import settings
from django.core.mail import EmailMessage

from . import choices, models


def insert_cdr(cdr):
    for c in choices.COMPANIAS:
        cdr.insert_incoming(c[0])

    for c in models.Company.objects(invoicing='monthly'):
        i = models.Invoice.objects.get(
            company=c, month=cdr.month, year=cdr.year)

        for p in models.Period.objects(invoice=i):
            for r in models.Rate.objects(period=p):
                r.call_number = models.Incoming.objects(
                    company=c,
                    connect_time__gte=p.start.date(),
                    connect_time__lte=p.end.date(),
                    schedule=r._type).count()
                r.call_duration = models.Incoming.objects(
                    company=c,
                    connect_time__gte=p.start.date(),
                    connect_time__lte=p.end.date(),
                    schedule=r._type).sum('ingress_duration')
                r.total = r.call_duration * r.price
                r.save()

            p.call_number = models.Rate.objects(
                period=p).sum('call_number')
            p.call_duration = models.Rate.objects(
                period=p).sum('call_duration')
            p.total = models.Rate.objects(period=p).sum('total')
            p.save()

        i.call_number = models.Period.objects(
            invoice=i).sum('call_number')
        i.call_duration = models.Period.objects(
            invoice=i).sum('call_duration')
        i.total = models.Period.objects(invoice=i).sum('total')
        i.invoiced = True
        i.save()

    cdr.insert_outgoing()
    send_email(
        [{'name': 'Leonardo Gatica', 'email': 'lgaticastyle@gmail.com'}],
        'Proceso finalizado',
        'gesvoip_success',
        {})


def send_email(to, subject, template_name, global_merge_vars):
    """Envia emails."""
    msg = EmailMessage(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to)
    msg.template_name = template_name
    msg.global_merge_vars = global_merge_vars
    msg.send()
