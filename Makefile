
ifndef API_KEY 
$(error API_KEY is not set)
endif

ifndef REGION 
$(error REGION is not set)
endif

ifndef TIMEZONE 
$(error TIMEZONE is not set)
endif

.PHONY: configure
configure:
	firebase functions:config:set apikey=$(API_KEY) region=$(REGION) timezone=$(TIMEZONE)

.PHONY: deploy
deploy: configure
	firebase deploy --only functions:exposureNotification 

.PHONY: destroy
destroy:
	firebase  functions:delete functions:exposureNotification

