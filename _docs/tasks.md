# RetroSignal MVP Backlog

## 1. Bootstrap the Django project
Goal: Create an empty Python and Django project with one passing test.
Description: Initialize the Django project and its basic test configuration without adding product features. Add a smoke test that loads the Django application successfully and document the single command that runs it.

## 2. Add the Docker Compose environment
Goal: Run the empty application with Django, PostgreSQL, and Redis through Docker Compose.
Description: Define `web`, `db`, and `redis` services with pinned image versions, health checks, and a persistent PostgreSQL volume. Verify that Compose starts cleanly and that the web container can connect to both PostgreSQL and Redis.

## 3. Configure environment-based settings
Goal: Keep runtime configuration and secrets outside application code.
Description: Read database, Redis, Django secret, OpenAI key, and OpenAI model settings from environment variables with safe development defaults where appropriate. Provide an example environment file containing placeholders only and test that required production values cannot be silently omitted.

## 4. Create the shared page shell
Goal: Establish the server-rendered UI foundation used by every screen.
Description: Add a base Django template with navigation, message rendering, CSRF-compatible HTMX setup, Tailwind CSS, and named content blocks. Include a simple accessible error fragment and verify that a test page renders the shell.

## 5. Create the custom user model
Goal: Represent users by email and display name from the start of the project.
Description: Add the custom Django user model with a public UUID, unique email, display name, and standard authentication fields. Configure it before other domain migrations and test user and superuser creation.

## 6. Implement sign-in and sign-out
Goal: Let registered users start and end an authenticated session.
Description: Build Django form-based sign-in and sign-out views using secure session cookies and CSRF protection. Test successful login, invalid credentials, logout, and redirection back to the originally requested page.

## 7. Add projects
Goal: Let an authenticated user create and view a project.
Description: Add the `Project` model with a public UUID, name, creator, and timestamps, plus create and detail views. Make the creator a facilitator through the project-membership workflow and test that unrelated users cannot open the project.

## 8. Add project memberships
Goal: Represent active member and facilitator access within each project.
Description: Add `ProjectMembership` with project, user, role, active state, timestamps, and a uniqueness constraint for each user-project pair. Test the `MEMBER` and `FACILITATOR` roles and ensure inactive memberships grant no access.

## 9. Build project team management
Goal: Let facilitators add, change, and deactivate project members.
Description: Add facilitator-only forms and HTMX fragments for adding an existing user, changing a member's role, and deactivating membership. Protect the project from losing its final active facilitator and test every permission boundary.

## 10. Centralize project authorization
Goal: Apply the same membership checks to every project-scoped request.
Description: Create reusable authorization helpers that resolve objects only through an active `ProjectMembership` and distinguish members from facilitators. Test missing membership, inactive membership, wrong-project UUIDs, and insufficient roles without leaking whether an object exists.

## 11. Add feedback cycles and participants
Goal: Store a project's retrospective cycle and its participant snapshot.
Description: Add `FeedbackCycle` with facilitator, public UUID, workflow stage, and stage timestamps, plus `CycleParticipant` with invitation, submission, and attendance fields. Enforce one non-completed cycle per project and test that later membership changes do not alter the participant snapshot.

## 12. Implement cycle creation
Goal: Let a project facilitator open a weekly cycle in the `COLLECTING` stage.
Description: Build a facilitator-only form that creates a cycle and snapshots selected active project members as participants. Show validation for an existing active cycle and test that an ordinary member cannot create one.

## 13. Add the workflow transition service
Goal: Make feedback-cycle stage changes explicit and safe.
Description: Implement a domain service for the allowed sequence `COLLECTING`, `CLUSTERING`, `VOTING`, `DISCUSSING`, `COMPLETED`, and `PUBLISHED`. Lock the cycle row during transitions and test valid, invalid, repeated, and unauthorized transitions.

## 14. Add feedback cards and anonymous edit grants
Goal: Store Start, Stop, and Continue cards without putting an author on anonymous cards.
Description: Add `FeedbackCard` and `AnonymousCardEditGrant` with the fields and constraints defined in the architecture. Ensure anonymous cards have no attributed author, attributed cards have one, and edit grants are excluded from generic Django admin access.

## 15. Build feedback submission
Goal: Let a cycle participant add multiple attributed or anonymous cards while collecting.
Description: Create the three-section Start, Stop, and Continue form using Django forms and HTMX fragments. Save an attributed author or a separate anonymous edit grant as appropriate, update aggregate submission status, and test category, length, membership, and stage validation.

## 16. Build feedback editing and deletion
Goal: Let contributors manage only their own cards before reveal.
Description: Add HTMX edit and delete actions that recognize attributed ownership and anonymous edit grants during `COLLECTING`. Test that another member and the facilitator cannot alter someone else's card and that nobody can change cards after reveal.

## 17. Enforce collection privacy
Goal: Prevent participants and facilitators from reading other contributors' feedback before reveal.
Description: Scope collection queries so each participant receives only attributed cards they authored and anonymous cards covered by their edit grants. Add request and template tests proving that card bodies, identifiers, and counts from other contributors are absent from responses.

## 18. Implement the reveal transaction
Goal: Reveal every card at once while permanently removing anonymous edit links.
Description: Implement the facilitator-only transition from `COLLECTING` to `CLUSTERING` in one database transaction that deletes the cycle's anonymous edit grants and sets `revealed_at`. Test rollback behavior, repeated reveal attempts, post-reveal card visibility, and the absence of author links for anonymous cards.

## 19. Add clusters and the board view
Goal: Display revealed cards in ordered clusters and an ungrouped area.
Description: Add the `Cluster` model and server-rendered board page for cycles in `CLUSTERING` or later. Render canonical card and cluster fragments from PostgreSQL and test project membership, stage visibility, ordering, and ungrouped cards.

## 20. Implement cluster creation and renaming
Goal: Let participants create and rename clusters during clustering.
Description: Add HTMX forms for creating a cluster and renaming an existing cluster with cycle-scoped uniqueness and length validation. Restrict mutations to active participants during `CLUSTERING` and return the updated board fragment.

## 21. Implement card drag and drop
Goal: Move and reorder cards through SortableJS while keeping Django authoritative.
Description: Add a small idempotent JavaScript initializer and a Django endpoint accepting card, target cluster, and target position. Validate membership and stage, update positions transactionally, and return canonical fragments when a move is accepted or rejected.

## 22. Implement cluster merging
Goal: Combine two clusters without losing cards or ordering.
Description: Add a clustering-stage action that locks both clusters, moves the source cards into the target, normalizes positions, and removes the source cluster. Return the affected board fragments and test cross-cycle IDs, concurrent changes, and unauthorized requests.

## 23. Implement cluster splitting
Goal: Move selected cards into a newly named cluster.
Description: Add a form that accepts one source cluster, selected card IDs, and a new cluster name during `CLUSTERING`. Validate that every card belongs to the source and cycle, then create and populate the new cluster atomically.

## 24. Add the OpenAI client boundary
Goal: Provide one configured path for synchronous OpenAI Responses API calls.
Description: Implement a Django service wrapper that reads the model and API key from settings and applies `store=false`, strict timeouts, and output-token limits. Test it with a fake client so no network call is required and verify that provider errors become safe application exceptions.

## 25. Generate cluster suggestions with OpenAI
Goal: Suggest editable thematic clusters from the revealed feedback cards.
Description: Define a Structured Outputs schema and prompt for cluster names and card assignments, then call it through `ClusteringService.suggest`. Validate all returned card IDs against the cycle and test malformed output, timeouts, empty feedback, and cards omitted by the suggestion.

## 26. Apply editable cluster suggestions
Goal: Let the team review and apply OpenAI clustering without treating it as final.
Description: Render suggested clusters separately with actions to apply or discard them during `CLUSTERING`. Applying a suggestion creates ordinary `AI_SUGGESTED` clusters and card placements in one transaction, after which all existing manual cluster actions remain available.

## 27. Add vote budgets and allocations
Goal: Store up to three stackable votes per participant and cycle.
Description: Add `VoteBudget` and `VoteAllocation` with uniqueness and range constraints for participant, cycle, and cluster. Test valid allocations, invalid counts, cross-cycle references, and the invariant that a budget remains between zero and three.

## 28. Open voting
Goal: Move a clustered cycle into voting with one three-vote budget per eligible participant.
Description: Extend the transition service so a facilitator can change `CLUSTERING` to `VOTING` and create budgets for the cycle's active participant snapshot. Perform both actions atomically and test repeated opening, inactive members, and unauthorized requests.

## 29. Cast and remove votes
Goal: Let each participant distribute their three votes across clusters.
Description: Add HTMX actions that lock the participant's budget row and update an allocation and `used_count` in one transaction. Return only that participant's allocations and remaining budget, and test stacking, removal, concurrent requests, and attempts to exceed three votes.

## 30. Keep vote totals hidden
Goal: Prevent participants and facilitators from seeing aggregate votes while voting is open.
Description: Audit voting queries, fragments, context variables, and WebSocket payloads so they expose only the current participant's state during `VOTING`. Add tests proving aggregate totals and other participants' allocations appear nowhere before voting closes.

## 31. Close voting and rank topics
Goal: Produce a stable prioritized discussion agenda from the final votes.
Description: Add the facilitator close action and the automatic all-votes-used path, locking the cycle before aggregating totals and creating ranked `DiscussionTopic` snapshots. Use a deterministic tie rule, set `voting_closed_at`, enter `DISCUSSING`, and test both close paths and concurrent final votes.

## 32. Build the discussion agenda
Goal: Present ranked topics and one active discussion topic to the facilitator and team.
Description: Render discussion topics by stored rank with title snapshot, vote total, status, and related cards. Limit management controls to the cycle facilitator while allowing active project members to view the agenda.

## 33. Update discussion status and notes
Goal: Record whether each topic was discussed, skipped, or deferred with meeting notes.
Description: Add facilitator-only HTMX forms for topic status and notes during `DISCUSSING`. Validate the allowed statuses, preserve multiline notes safely, and return an updated topic fragment.

## 34. Record manual decisions
Goal: Let the facilitator attach confirmed decisions to the cycle or a discussion topic.
Description: Add the `Decision` model and HTMX create, edit, and delete forms with `MANUAL` source. Scope every operation to the current cycle and test that members can view decisions but cannot modify them.

## 35. Record and assign action items
Goal: Let the facilitator create accountable actions from the discussion.
Description: Add `ActionItem` with description, active project owner, optional due date, `OPEN` or `DONE` status, related topic, and `MANUAL` source. Provide facilitator create and edit forms and test owner, topic, date, and cross-project validation.

## 36. Let owners complete actions
Goal: Let an assigned member switch their action between open and done.
Description: Add a focused HTMX status action available to the assigned active member and project facilitators. Prevent owners from changing the description, owner, due date, topic, or source, and test access by unassigned members.

## 37. Capture attendance
Goal: Let the facilitator record who attended the retrospective.
Description: Add a facilitator-only participant checklist that sets or clears `attended_at` without changing the cycle's membership snapshot. Show attendance in the discussion and summary contexts and test that ordinary members cannot edit it.

## 38. Add pasted transcript submission
Goal: Store facilitator-pasted meeting transcript text without accepting files.
Description: Add `TranscriptSubmission` and a facilitator-only form with an explicit text-length limit and client-generated idempotency key. Reject uploads and non-text input by design, and test duplicate submission, empty input, wrong project, and unauthorized access.

## 39. Extract draft outcomes with OpenAI
Goal: Produce structured draft decisions, actions, owners, due dates, and summary text from a pasted transcript.
Description: Define the OpenAI Structured Outputs schema and implement `ExtractionService.extract` as a synchronous request through the shared client. Match suggested owners only to active project memberships and test ambiguous owners, invalid dates, malformed output, timeout, and no partial database writes.

## 40. Review draft suggestions
Goal: Let the facilitator confirm, edit, or dismiss each extracted suggestion.
Description: Add `DraftSuggestion` and an HTMX review interface for `DECISION`, `ACTION`, and `SUMMARY` suggestions in `PENDING`, `CONFIRMED`, or `DISMISSED` states. Ensure only the facilitator can review drafts and that no pending or dismissed content appears in durable outcomes.

## 41. Confirm AI decisions and actions
Goal: Convert an approved AI suggestion into one durable domain record exactly once.
Description: Implement a transaction that locks a pending suggestion, creates an `AI_CONFIRMED` decision or action, and records reviewer and review time. Test repeated confirmation, edits made during confirmation, invalid suggested owners, and concurrent confirmation requests.

## 42. Build the summary preview
Goal: Preview the complete retrospective record before publication.
Description: Render ranked topics, notes, confirmed decisions, actions, attendance, aggregate participation, and original feedback cards, plus editable summary text. Exclude pending AI suggestions and restrict the preview and narrative editing to the facilitator until publication.

## 43. Publish the retrospective summary
Goal: Freeze the reviewed summary and make it visible to project members.
Description: Add `RetrospectiveSummary` and a facilitator-only transaction that saves the narrative, records the publisher and time, and moves `COMPLETED` to `PUBLISHED`. Test incomplete-cycle rejection, repeat publication, member visibility after publication, and continued action-status updates.

## 44. Add the Channels infrastructure
Goal: Connect Django Channels to Redis and serve private retrospective WebSockets.
Description: Configure the ASGI application, Redis channel layer, and a retrospective route keyed by public cycle UUID. Add connection tests for authenticated active members, inactive members, unrelated users, anonymous users, and nonexistent cycles.

## 45. Broadcast safe domain events
Goal: Notify connected participants after committed board and workflow changes.
Description: Publish identifier-only events such as `board.changed`, `stage.changed`, `voting.closed`, `discussion.changed`, and `summary.published` using transaction commit hooks. Test that payloads never contain card bodies, anonymous ownership, individual votes, transcripts, or draft suggestions.

## 46. Refresh HTMX fragments from WebSocket events
Goal: Keep connected boards current without putting domain state in JavaScript.
Description: Add a small reconnecting WebSocket module that maps event types to authorized HTMX fragment requests. Test repeated initialization after swaps, reconnect behavior, duplicate events, and full recovery by reloading canonical server-rendered fragments.

## 47. Add the project dashboard
Goal: Show the project's current cycle, aggregate submissions, retrospective history, and open actions.
Description: Build the project page from authorized server-side queries, showing aggregate collection progress without identifying who submitted. Include the active stage, previous published summaries, and open actions relevant to the viewer, with tests for empty and populated projects.

## 48. Add domain audit events
Goal: Record sensitive facilitator actions without compromising anonymous feedback.
Description: Store audit events for reveal, stage changes, voting close, AI confirmation, attendance edits, and publication with actor, cycle, event type, and time. Never store card bodies or pair an anonymous card ID with its contributor, and test the audit record for each covered action.

## 49. Add request limits and privacy-safe logging
Goal: Protect authentication, feedback, and OpenAI endpoints while keeping sensitive text out of logs.
Description: Apply focused rate limits to sign-in, feedback mutations, clustering, and transcript extraction, and configure structured request IDs. Add tests or log-capture checks showing that feedback bodies, transcript text, individual votes, secrets, and anonymous edit grants are not logged.

## 50. Add retention cleanup
Goal: Remove expired transcript and provider-related data according to configured retention periods.
Description: Add a management command that deletes eligible transcript submissions and associated drafts without changing confirmed decisions, actions, or published summaries. Support a dry-run mode and test cutoff boundaries, protected records, idempotency, and reported counts.

## 51. Add operational health checks
Goal: Report whether Django can reach PostgreSQL and Redis in the Compose environment.
Description: Add a lightweight health endpoint that checks application readiness without exposing credentials or internal details. Cover healthy and unavailable dependencies in tests and wire the endpoint into the Docker Compose service health check.

## 52. Add the end-to-end MVP workflow test
Goal: Prove that two members and a facilitator can complete one retrospective safely.
Description: Build a browser test covering project setup, private and anonymous feedback, reveal, clustering, hidden voting, discussion, transcript extraction with a fake OpenAI response, approval, and publication. Use separate authenticated sessions and assert the critical privacy boundaries before reveal and voting close.
