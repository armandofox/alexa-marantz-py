AWS = aws
ZIP = zip
PYTHON = python

SKILL_NAME = MarantzIP
ZIPFILE = _$(SKILL_NAME).zip
DEPS = $(shell pwd)/package

IP ?= $(shell curl ifconfig.me)
PORT ?= $(shell $(AWS) lambda get-function-configuration --function-name $(SKILL_NAME) | jq '.["Environment"]["Variables"]["PORT"]')

zip: $(ZIPFILE)

$(ZIPFILE): $(wildcard lambda/*)
	cd lambda && $(ZIP)  -qXr  ../$(ZIPFILE) *
	cd $(DEPS) && $(ZIP) -qXrg ../$(ZIPFILE) *

update_env:
	$(AWS) lambda update-function-configuration --function-name $(SKILL_NAME) --environment "Variables={IP=$(IP),PORT=$(PORT),MEROSS_EMAIL=$(MEROSS_EMAIL),MEROSS_PASSWORD=$(MEROSS_PASSWORD)}"

upload_lambda: $(ZIPFILE)
	$(AWS) lambda update-function-code --function-name $(SKILL_NAME) --zip-file fileb://$(ZIPFILE)

skill/utterances.txt: skill/utterances.txt.glob
	$(PYTHON) lambda/ask/unglob_intent.py $< > $@

update_meross_login:
	$(AWS) lambda update-function-configuration --function-name $(SKILL_NAME) --environment "Variables={IP=$(IP),PORT=$(PORT)}"

update_meross_iot:
	pip install --target $(DEPS) meross_iot==0.3.2.17 --upgrade
