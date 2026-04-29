```md
## Trade-off

I used a simple single-agent function-calling flow instead of a multi-step planner architecture to maximize reliability and delivery speed within the assignment time limit.

## Underspecified Decision

The brief did not define behavior for unsupported questions. I chose to clearly state that the assistant specializes in weather and Indian polity rather than hallucinating unrelated answers.

## Shared Toolkit Candidate

The weather tool wrapper and reusable vector-store ingestion/search module would belong in a shared internal “agent toolkit” because they can be reused across many future agents.
