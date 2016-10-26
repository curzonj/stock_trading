### DB migrations

https://github.com/mattes/migrate

```bash
# apply all available migrations
migrate -url driver://url -path ./db/migrate up
```

## Useful queries

```sql
select test_runs.id, name, parameters, starts_at, ends_at from ts_at, ends_at from strategies join test_runs on (strategy_id = strategies.id);
```

# Work log

- [x] fix the run.py to support data before the run start so I can do the SMA strategies
- [x] I want to pass in the security to use in a single buy and hold strategy. the strategy itself probably shouldn't specify the securities to trade, they should be parameters.
- [ ] I can generate lots of back tests with different securities and parameters, but now I need a way to view my data and analyze and compare my backtests
