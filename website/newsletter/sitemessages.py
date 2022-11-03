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
    SMTPMessenger(
        'admin@aboelezz.com',
        'apikey',
        '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',
        'smtp.sendgrid.net',
        '465',
        use_ssl=True,
)
)

