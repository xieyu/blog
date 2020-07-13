
```
UPDATE 
	{{.tablePushStat}} as p,
	(
		SELECT 
			sum(success) as success,
			sum(failure) as failure
		FROM
			{{.tableDelivery}} d
		WHERE d.message_id = message_id
	) as stat
SET
	p.delivery_success +=  {{.incSuccess}},
	p.delivery_failure +=  {{.incFailure}}
WHERE
	p.message_id = {{.messageID}}
`
```

