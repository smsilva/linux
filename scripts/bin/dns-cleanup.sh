#!/bin/bash
ENVIRONMENT_ID="$1"
DNS_ZONE_NAME="sandbox.wasp.silvios.me"
DNS_ZONE_RESOURCE_GROUP_NAME="wasp-foundation"
DNS_ZONE_RECORDS_FILE="$(mktemp)"

az network dns record-set a list \
  --resource-group "${DNS_ZONE_RESOURCE_GROUP_NAME?}" \
  --zone-name ${DNS_ZONE_NAME?} \
  --output table >> ${DNS_ZONE_RECORDS_FILE?}

az network dns record-set cname list \
  --resource-group "${DNS_ZONE_RESOURCE_GROUP_NAME?}" \
  --zone-name ${DNS_ZONE_NAME?} \
  --output table >> ${DNS_ZONE_RECORDS_FILE?}

az network dns record-set txt list \
  --resource-group "${DNS_ZONE_RESOURCE_GROUP_NAME?}" \
  --zone-name ${DNS_ZONE_NAME?} \
  --output table >> ${DNS_ZONE_RECORDS_FILE?}

grep ${ENVIRONMENT_ID?} ${DNS_ZONE_RECORDS_FILE?} | sort -u | awk '{ print $1, $4 }' | while read LINE; do
  RECORD_NAME=$(awk '{ print $1 }' <<< "${LINE}")
  RECORD_TYPE=$(awk '{ print $2 }' <<< "${LINE}")

  echo "RECORD_TYPE=${RECORD_TYPE} RECORD_NAME=${RECORD_NAME}"
  
  az network dns record-set ${RECORD_TYPE,,} delete \
    --name "${RECORD_NAME?}" \
    --resource-group "${DNS_ZONE_RESOURCE_GROUP_NAME?}" \
    --zone-name ${DNS_ZONE_NAME?} \
    --yes \
    --only-show-errors
done
