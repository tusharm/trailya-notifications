.PHONY: deploy
deploy: guard-TOPIC guard-REGION
	gcloud functions deploy notify \
		--runtime python39  \
		--trigger-topic $(TOPIC) \
		--region $(REGION) \
		--source ./src 

.PHONY: guard-TOPIC
guard-TOPIC:
ifndef TOPIC
	$(error TOPIC env var missing)
endif

.PHONY: guard-REGION
guard-REGION:
ifndef REGION
	$(error REGION env var missing)
endif

