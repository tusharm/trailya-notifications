.PHONY: clean
clean:
	rm -rf build/

.PHONY: package
package:
	mkdir -p build/
	pip install -r requirements.txt -t ./build/
	cp -r src/* build/
	
.PHONY: deploy
deploy: guard-TOPIC guard-REGION package
	cd build && \
	gcloud functions deploy notify \
		--runtime python39  \
		--trigger-topic $(TOPIC) \
		--region $(REGION)  

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

