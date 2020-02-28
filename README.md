# alexa-marantz-py

Simple app to control my Marantz 5007 receiver (should work with related
Marantz models as well) via Alexa.

The code is based on [@anjishnu](https://github.com/anjishnu)'s useful [Python version of Alexa Skills
Kit](https://github.com/anjishnu/ask-alexa-pykit). 

You need Python 2.7 or later and the [AWS command line tool](https://aws.amazon.com/cli/).

# Usage

## 1. Set up the skill and slot types

Unfortunately, Amazon doesn't yet provide an API to upload the intent
schema, utterances, and slot types, so you have to add them manually
using their GUI:

1. Set up a custom skill on Amazon's Alexa developer pages and give it a
name.  Change the value of `SKILL_NAME` in the `Makefile` to whatever
you called your skill.

2. In the Interaction Model, add Custom Slot Types named
`MARANTZ_SOURCES`, `ACTIVITY_LIST`, and `VOLUME_CHANGES`, and copy the
contents of the respective files (in the
`skill/` directory) as the slot values.

3. Copy the contents of `skill/utterances.txt` to the Sample Utterances.
You can add/modify utterances in `skill/utterances.txt.glob` and then
`make skill/utterances.txt` to generate the changes.

4. Copy the contents of `skill/intent_schema.json` to the Intent Schema box
in the interaction model.

**NOTE:** Unfortunately you cannot name your skill "the stereo" because
Alexa apparently reserves "Tell the stereo to..." for "smart home"
compatible stereo receivers, which this isn't.  So instead, I named our
skill "Thisterio", which works in practice when you say "Tell thistereo to..."

## 2. Upload the skill itself

Create a lambda function using the AWS GUI (you only need to do this
once).  Then `make upload_lambda` to upload the Python code as the
lambda body.

## 3. Set up port forwarding

If you're like most people, your receiver and your Alexa device are
behind your firewall/NAT.  You will probably have to configure your NAT
box to assign a static IP address to your Marantz receiver, and set up
port forwarding to get packets through your NAT firewall.

The Python code looks for environment variables `IP` and `PORT` to do
this.  It expects to be able to send traffic to port `PORT` of your NAT
box at `IP`, and that that traffic will be forwarded to your Marantz
receiver.

To set the environment variables, say:
`IP=`*your_external_ip* `PORT=`*port_forwarding_number*` make update_port_and_ip`
If you don't set `IP`, the Makefile includes a command to try to
figure it out using the OpenDNS resolvers and `myip.opendns.com`.  
If you don't set `PORT`, the default value will be the one in the
current Lambda configuration (i.e. unchanged).

## Wasn't that easy?

You can now say things like:

`Alexa, tell thisterio to play Roku`

`Alexa, tell thisterio to play my iPhone in zone 2`  (in my house, Zone
2 is our piano room, so in the skills code, `the piano room` is an alias
for `zone two`; modify to fit your house)

`Alexa, tell thisterio to turn off`

