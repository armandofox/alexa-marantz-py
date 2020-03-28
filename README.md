# alexa-marantz-py

Simple app to control my Marantz 5007 receiver (should work with related
Marantz models as well) via Alexa.

The code is based on [@anjishnu](https://github.com/anjishnu)'s useful [Python version of Alexa Skills
Kit](https://github.com/anjishnu/ask-alexa-pykit). 

It's running with Python 3.7 and the [AWS command line tool](https://aws.amazon.com/cli/).

# Usage

## 1. Set up the skill and slot types

I made this before Amazon's API allowed uploading JSON directly for
intent schema, utterances, slot types, etc., although
`skill/skill.json` is up-to-date so you should use that instead of
setting up slot types manually. 

If you want to add utterances, you can add/modify utterances in `skill/utterances.txt.glob` and then
`make skill/utterances.txt` to generate the changes.  It's a little
hack to allow simple globbing to simplify recognizing variants of
different utterances.

Change the value of `SKILL_NAME` in the `Makefile` to whatever
you called your skill, if you want to use the convenient make targets
for updating the code and updating the port/IP of your port-forwarding
firewall (see below).

## 2. Upload the skill itself

Create a lambda function using the AWS GUI (you only need to do this
once).  Then `make upload_lambda` to upload the Python code as the
lambda body.  If you look at the `Makefile` you'll see you need to
have your AWS CLI credentials set up, etc. to use this feature.

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

`Alexa, tell <skill> to play Roku`

`Alexa, tell <skill> to play my iPhone in zone 2`  (in my house, Zone
2 is our piano room, so in the skills code, `the piano room` is an alias
for `zone two`; modify to fit your house)

`Alexa, tell <skill> to turn off`

