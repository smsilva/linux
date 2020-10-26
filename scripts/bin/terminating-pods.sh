while read line; do
  awk '{ print $1 }' <<< $line
done <<< $(for NAMESPACE in {dev,qa,uat}; do
  kubectl -n ${NAMESPACE} get pods | grep Terminating
done)
