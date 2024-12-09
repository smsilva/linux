# Costs

## Retrieve costs

```bash
start_date="2024-06-01"
end_date="2024-06-30"

while read -r subscription_id; do
  echo "Subscription: ${subscription_id?}"

  base_file_name="costs-${subscription_id?}_${start_date?}_${end_date?}"
  data_file_name="${base_file_name?}.json"
  error_file_name="${base_file_name?}.log"

  ./azure-costs \
    --subscription "${subscription_id?}" \
    --start-date "${start_date?}" \
    --end-date "${end_date?}" > ${data_file_name?} 2> ${error_file_name?}
done < <(az account list --query '[].id' -o tsv)
```

## Convert json to tsv

```bash
while read -r json_file; do
  echo "Converting: ${json_file}"
  tsv_file_name="${json_file%.*}.tsv"
  ./json-to-tsv "${json_file}" > "${tsv_file_name}"
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
