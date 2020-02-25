from ask import alexa
from avr import AVR
import time

response = ''


def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {}
    # print "Calling handler for {}".format(request_obj.intent_name())
    return alexa.route_request(request_obj, metadata)

def command(cmd,ok):
    # print "Sending '{}' to AVR".format(cmd)
    result = AVR().send(cmd)
    if result == 'OK':
        card = alexa.create_card(title = "Marantz", subtitle=None, content=ok)
        response = alexa.create_response(ok, end_session=True, card_obj=card)
    else:
        card = alexa.create_card(title = "Marantz", subtitle="Error", content = result)
        response = alexa.create_response("Sorry, the receiver doesn't seem to be cooperating.", end_session=True, card_obj=card)
    return response

@alexa.intent_handler("InteractiveSetupIntent")
def interactive_setup_intent(request):
    # Alexa dialog delegation will have filled the slots 'activity' (from ACTIVITY_LIST) and 'location'
    # (from MARANTZ_LOCATIONS) so we just have to check if they're compatible, e.g. you can't watch
    # a DVD in the piano room.
    act = request.slots["Activity"].lower()
    location = request.slots["Location"].lower()
    print ("Activity=<{}>, Location=<{}>\n".format(act,location))
    if location == 't.v. room' or location == 'tv room':
        return setup_main_zone_for_activity(act)
    else:
        return setup_zone2_for_activity(act)

@alexa.intent_handler("PlayZoneTwoIntent")
def play_zone2_intent_handler(request):
    source = request.slots["Activity"].lower()
    return setup_zone2_for_activity(source)

@alexa.intent_handler("StopZoneTwoIntent")
def stop_intent_handler(request):
    return command('Z2OFF', "Piano room speakers turned off.")

@alexa.intent_handler("VolumeZoneTwoIntent")
def volume_zone2_intent(request):
    vol = request.slots["Volume"].lower()
    if vol == 'louder':
        cmd = 'UP'
    else:
        cmd = 'DOWN'
    num_ticks = 10
    return command(['Z2' + cmd] * num_ticks, "OK")
        
@alexa.intent_handler("OffIntent")
def off_intent_handler(request):
    return command(['Z2OFF','PWSTANDBY'], "Stereo is off.")

@alexa.intent_handler("SetupMainZoneIntent")
def activity_intent_handler(request):
    act = request.slots["Activity"].lower()
    return setup_main_zone_for_activity(act)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Marantz Control was activated, but you need to ask me to do something.")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="MarantzControl launched")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="MarantzControl signoff")
    

def setup_main_zone_for_activity(act):
    if act in ("tv", "t.v.", "netflix", "roku", "you tube", "youtube", "amazon video"):
        name = 'SAT/CBL'
        msg = 'OK. Turn on the TV to watch Roku, Netflix, or Amazon Video.'
    elif act in ('you tube', 'youtube'):
        name = 'SAT/CBL'
        msg = 'OK. Use the Roku remote to select the You Tube app.'
    elif act.find('phone') > -1 or act in ('air play', 'pandora', 'spotify'):
        name = 'NET'
        msg = 'OK. Open any music app on your I phone and choose the Marantz receiver as the Air Play destination.'
    elif act.find('dvd') > -1 or act.find('movie') > -1:
        name = 'BD'
        msg = 'DVD player is ready. What are we watching?'
    else:
        return alexa.create_response("Sorry, I don't know how to set up the stereo for the " + act + " task.", end_session=True, card_obj=alexa.create_card(title="Marantz Error", content=act))

    response = command(['Z2OFF', 'PWON', 'ZMON', 'SI'+name], msg)
    return response

def setup_zone2_for_activity(source):
    source = source.lower()
    if source in ('i phone', 'iphone', 'mac', 'itunes', 'i tunes', 'air play', 'pandora', 'spotify'):
        name = 'NET'
        msg = "OK. Open any music app on your I phone or Mac and choose the Marantz receiver as the Air Play destination."
    # elif source == 'pandora':
    #     name = 'PANDORA'
    #     msg = 'Pandora will start playing in the piano room in a few seconds.'
    else:
        return alexa.create_response("I don't know how to play the source {} in the piano room.".format(source), end_session=True)

    return command(['Z2ON', 'Z2' + name], msg)


