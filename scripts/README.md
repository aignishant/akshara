# scripts/ — repo tooling

**Refuses to hold:** anything that imports `akshara`.

The arrow points one way: tooling knows about the project, the project knows nothing about its
tooling. If `depth_check.py` needed the model to import cleanly, it would stop working exactly when
the repository is broken — which is when it is needed.
