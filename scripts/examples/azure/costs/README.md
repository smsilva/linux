# Costs

```bash
./azure-costs \
  --subscription "${ARM_SUBSCRIPTION_ID?}" \
  --start-date "2024-06-01" \
  --end-date "2024-06-30" > >(tee data.json) 2> >(tee error.log >&2)
```
