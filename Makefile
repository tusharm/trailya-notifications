.PHONY: clean
clean:
	rm -rf build/

.PHONY: package
package:
	mkdir -p build/
	pip install -r requirements.txt -t ./build/
	cp -r src/* build/
	
.PHONY: deploy
deploy: guard-TOPIC guard-REGION guard-VIC_API_KEY_ID package
	cd build && \
	gcloud functions deploy notify \
		--runtime python39  \
		--trigger-topic $(TOPIC) \
		--region $(REGION) \
		--set-env-vars VIC_API_KEY_ID=$(VIC_API_KEY_ID)

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
ifndef guard-VIC_API_KEY_ID
	$(error VIC_API_KEY_ID env var missing)
endif

