import datetime

def footer_cp(request):
    """Display data time and 'based on'"""
    context = {
                "now": datetime.datetime.now(),
                "based_on" : "Based on the Django tutorial."
              }
    return context