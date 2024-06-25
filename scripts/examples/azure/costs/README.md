# Costs

## Retrieve costs

```bash
START_DATE="2024-06-01"
END_DATE="2024-06-30"

while read -r SUBSCRIPTION_ID; do
  echo "Subscription: ${SUBSCRIPTION_ID?}"

  BASE_FILE_NAME="costs-${SUBSCRIPTION_ID?}_${START_DATE?}_${END_DATE?}"
  DATA_FILE_NAME="${BASE_FILE_NAME?}.json"
  ERROR_FILE_NAME="${BASE_FILE_NAME?}.log"

  ./azure-costs \
    --subscription "${SUBSCRIPTION_ID?}" \
    --start-date "${START_DATE?}" \
    --end-date "${END_DATE?}" > ${DATA_FILE_NAME?} 2> ${ERROR_FILE_NAME?}
done < <(az account list --query '[].id' -o tsv)
```

## Convert json to tsv

```bash
while read -r JSON_FILE; do
  echo "Converting: ${JSON_FILE}"
  TSV_FILE_NAME="${JSON_FILE%.*}.tsv"
  ./json-to-tsv "${JSON_FILE}" > "${TSV_FILE_NAME}"
done < <(find . -name 'costs-*.json')
```

## Merge tsv files

```bash
./merge-tsv-files > costs-merged.tsv
```

## Remove files

```bash
rm -f costs-*
```
