from ask import alexa
from avr import AVR
from meross_driver import MerossDriver
import time

response = ''


def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = { 'lights': MerossDriver() }
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
    if location.find('piano') > 0:
        return setup_zone2_for_activity(act,request)
    else:
        return setup_main_zone_for_activity(act,request)

@alexa.intent_handler("PlayZoneTwoIntent")
def play_zone2_intent_handler(request):
    source = request.slots["Activity"].lower()
    return setup_zone2_for_activity(source,request)

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
    everything_off(request)
    return command(['Z2OFF','PWSTANDBY'], "Stereo is off.  Don't forget to turn off the TV with the Panasonic remote.")

@alexa.intent_handler("SetupMainZoneIntent")
def activity_intent_handler(request):
    act = request.slots["Activity"].lower()
    return setup_main_zone_for_activity(act,request)

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
    

def setup_main_zone_for_activity(act,request):
    location = request.slots["Location"].lower()
    if act in ("tv", "t.v.", "netflix", "roku", "you tube", "youtube", "amazon video", "amazon prime", "amazon"):
        name = 'SAT/CBL'
        msg = 'OK. Use the Panasonic remote to turn on the TV to watch {}.'.format(act)
    elif act.find('phone') > -1 or act in ('air play', 'pandora', 'spotify'):
        name = 'NET'
        msg = 'OK. Open any music app on your I phone and choose the Marantz receiver as the Air Play destination.'
    elif act.find('dvd') > -1 or act.find('movie') > -1:
        name = 'BD'
        msg = 'DVD player is ready. What are we watching?'
    else:
        return alexa.create_response("Sorry, I don't know how to set up Marantz Receiver for {}.".format(act),
                                     end_session=True, card_obj=alexa.create_card(title="Marantz Error", content=act))

    response = command(['Z2OFF', 'PWON', 'ZMON', 'SI'+name], msg)
    activate_amplifier(request,'on')
    if location.find('theater') > 0:
        # also activate "theater lighting": main OFF, light string ON, lamp ON
        activate_theater_lighting(request)
    return response

def setup_zone2_for_activity(source,request):
    source = source.lower()
    if source in ('i phone', 'iphone', 'mac', 'itunes', 'i tunes', 'air play', 'pandora', 'spotify'):
        name = 'NET'
        msg = "OK. Open any music app on your I phone or Mac and choose the Marantz receiver as the Air Play destination."
    # elif source == 'pandora':
    #     name = 'PANDORA'
    #     msg = 'Pandora will start playing in the piano room in a few seconds.'
    else:
        return alexa.create_response("I don't know how to play the source {} in the piano room.".format(source), end_session=True)

    activate_amplifier(request,'off')
    return command(['Z2ON', 'Z2' + name], msg)


# helper methods
def activate_amplifier(request,action):
    request.metadata['lights'].switch('Amplifier', action)


def activate_theater_lighting(request):
    lights = request.metadata['lights']
    lights.switch('tv room light string', 'on')
    lights.switch('TV room lamp', 'on')
    lights.switch('TV Room Main', 'off')

def everything_off(request):    
    lights = request.metadata['lights']
    lights.switch('tv room light string', 'off')
    lights.switch('TV room lamp', 'off')
    lights.switch('TV Room Main', 'off')
    lights.switch('Amplifier', 'off')
