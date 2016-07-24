"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
from avr import AVR
import time

response = ''


def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {}
    return alexa.route_request(request_obj, metadata)

def command(cmd,ok):
    result = AVR().send(cmd)
    if result == 'OK':
        card = alexa.create_card(title = "Marantz", subtitle=None, content=ok)
        response = alexa.create_response(ok, end_session=True, card_obj=card)
    else:
        card = alexa.create_card(title = "Marantz", subtitle="Error", content = result)
        response = alexa.create_response("Sorry, the receiver doesn't seem to be cooperating.", end_session=True, card_obj=card)
    return response

@alexa.intent_handler("PlayZoneTwoIntent")
def play_zone2_intent_handler(request):
    source = request.slots["Source"].lower()
    if source == 'i tunes' or source == 'apple tv':
        name = 'MPLAY'
        msg = 'Use the Remote app on your I Phone to play I Tunes in the piano room.'
    elif source == 'pandora':
        name = 'PANDORA'
        msg = 'Pandora will start playing in the piano room in a few seconds.'
    else:
        return alexa.create_response("I don't know the source {}.".format(source), end_session=True)

    response = command(['Z2ON', 'Z2' + name], msg)
    return response

@alexa.intent_handler("StopZoneTwoIntent")
def stop_intent_handler(request):
    response = command('Z2OFF', "Piano room speakers turned off.")
    return response

@alexa.intent_handler("ActivityIntent")
def activity_intent_handler(request):
    act = request.slots["Activity"].lower()
    if act == 'watch tv':
        name = 'SAT/CBL'
        msg = 'OK. Turn on the TV to watch Roku, Netflix, or Amazon Video.'
    elif act.find('dvd') > -1 or act.find('movie') > -1:
        name = 'BD'
        msg = 'OK. Put in a DVD and pop the popcorn.'
    elif act == 'watch apple tv' or act.find('photos') > -1:
        name = 'MPLAY'
        msg = 'OK. Use the small white remote to control Apple TV.'
    elif act == 'pandora':
        name = 'PANDORA'
        msg = 'Pandora streaming will start in the TV room shortly.'
    else:
        return alexa.create_response("Sorry, I don't know how to set up the stereo for that task.", end_session=True, card_obj=alexa.create_card(title="Marantz Error", content=act))

    response = command(['Z2OFF', 'SI'+name], msg)
    return response

@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="MarantzControl launched")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="MarantzControl signoff")
    

