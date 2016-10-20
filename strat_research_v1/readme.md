### DB migrations

https://github.com/mattes/migrate

```bash
# apply all available migrations
migrate -url driver://url -path ./db/migrate up
```

# Work log

- [x] fix the run.py to support data before the run start so I can do the SMA strategies
- [ ] I want to pass in the security to use in a single buy and hold strategy. the strategy itself probably shouldn't specify the securities to trade, they should be parameters.
