AWS = aws
ZIP = zip
PYTHON = python

SKILL_NAME = MarantzIP
ZIPFILE = _$(SKILL_NAME).zip

zip: $(ZIPFILE)

$(ZIPFILE): $(wildcard lambda/*)
	cd lambda && $(ZIP) -q -X -r ../$(ZIPFILE) *

update_port_and_ip:
	$(AWS) lambda update-function-configuration --function-name $(SKILL_NAME) --environment "Variables={IP=$(IP),PORT=$(PORT)}"


upload_lambda: $(ZIPFILE)
	$(AWS) lambda update-function-code --function-name $(SKILL_NAME) --zip-file fileb://$(ZIPFILE)

skill/utterances.txt: skill/utterances.txt.glob
	$(PYTHON) lambda/ask/unglob_intent.py $< > $@
