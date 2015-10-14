__author__ = 'kodiers'

def set_new_messages_to_old(messages):
    """
    Set message.new property (Messages model) to False
    :param messages: QuerySet of Messages model
    :return: None
    """
    if messages.exists():
        for message in messages:
           message.new = False
           message.save()