
.PHONY: deploy
deploy: guard-TOPIC guard-REGION guard-VIC_API_KEY_ID guard-SERVICE_ACCOUNT
	cd src && \
	ln -fs ../requirements.txt . && \
	gcloud functions deploy notify \
		--runtime python39  \
		--trigger-topic $(TOPIC) \
		--region $(REGION) \
		--set-env-vars VIC_API_KEY_ID=$(VIC_API_KEY_ID) \
		--service-account=$(SERVICE_ACCOUNT)

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

.PHONY: guard-VIC_API_KEY_ID
guard-VIC_API_KEY_ID:
ifndef VIC_API_KEY_ID
	$(error VIC_API_KEY_ID env var missing)
endif

.PHONY: guard-SERVICE_ACCOUNT
guard-SERVICE_ACCOUNT:
ifndef SERVICE_ACCOUNT
	$(error SERVICE_ACCOUNT env var missing)
endif

