# akshara/ — the model package

Every line here is typed by you, from a day document. Nothing is pre-written.

**Refuses to hold:** anything generated; anything that runs once and exits (that is `scripts/`);
anything that cannot be imported without side effects.

Subpackages are pipeline stages, in the order the curriculum builds them:
tokenizer → model → train → infer → eval → serve.
