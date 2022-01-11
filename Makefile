RUN_CDK = @docker-compose run --rm

.PHONY: init
init:
	@$(RUN_CDK) cdk init app --language=python

.PHONY: list
list:
	@$(RUN_CDK) cdk list

.PHONY: synth
synth:
	@$(RUN_CDK) cdk synth

.PHONY: diff
diff:
	@$(RUN_CDK) cdk diff

.PHONY: deploy
deploy:
	@$(RUN_CDK) cdk deploy

.PHONY: shell
shell:
	@$(RUN_CDK) --entrypoint /bin/bash cdk

# local helpers
prepare_venv: activate

activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install -r requirements.txt

venv: prepare_venv
