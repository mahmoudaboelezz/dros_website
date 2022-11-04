from sitemessage.toolbox import register_messenger_objects
from sitemessage.messengers.smtp import SMTPMessenger
from sitemessage.messages.base import MessageBase
from sitemessage.toolbox import register_message_types
from django.utils import timezone


class MyMessage(MessageBase):
    """ My message type """
    title = 'Message from Aboelezz'
    template= 'sitemessages/messages/my_message.html'
    
    
    
    @classmethod
    def get_template_context(cls, context):
        context.update({'greeting': 'Hi!'})
        return context
    @classmethod
    def create(cls, text):
        """Let it be an alternative constructor - kind of a shortcut."""

        # This recipient list is comprised of users subscribed to this message type.
        recipients = cls.get_subscribers()

        # Or we can build recipient list for a certain messenger manually.
        # recipients = cls.recipients('smtp', 'someone@sowhere.local')

        date_now = timezone.now().date().strftime('%d.%m.%Y')
        cls(text, date_now).schedule(recipients)
        
register_message_types(MyMessage)
    
register_messenger_objects(
#     SMTPMessenger(
#         'admin@aboelezz.com',
#         '1083b044e1620499d7de434658c225a9',
#         '74c4918ed8e36914467e19c403021e3b',
#         'in-v3.mailjet.com',
#         '465',
#         use_tls=True,
# )
#     SMTPMessenger(
#         'mahmoud.sobhy@aboelezz.com',
#         'apikey',
#         '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',
#         'smtp.sendgrid.net',
#         '465',
#         use_tls=True,
# )
    SMTPMessenger(
        'egblack2030@gmail.com',
        'apikey',
        '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',
        'smtp.sendgrid.net',
        '465',
        use_ssl=True,
)
)# #Smtp Email for recovery password


