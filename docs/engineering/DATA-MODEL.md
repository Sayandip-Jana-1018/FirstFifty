# Data model

PostgreSQL 18 is the system of record. Extensions: `pg_trgm`, `vector` (pgvector), `citext`. IDs are UUIDv7 (time-ordered), generated in the application. Timestamps are `timestamptz` in UTC. Money is `bigint` paise.

This is the starting schema. The architect owns changes; every change is a Flyway migration.

## Catalog and ingestion
**companies:** `id`, `slug` (unique), `name`, `website`, `official_domains text[]`, `tier` (A, B, C), `company_type` (product, startup, service), `hq_city`, `logo_object_key`, `status`, `created_at`, `updated_at`.

**sources:** `id`, `company_id`, `ats_type` (greenhouse, lever, ashby, smartrecruiters, workday, workable, recruitee, amazon, microsoft, google, oracle_hcm, atlassian, custom), `ats_ref jsonb` (slug, tenant, site, base URL), `tier`, `poll_interval_seconds`, `status` (active, paused, failing, disabled), `etag`, `last_modified`, `last_success_at`, `last_error_at`, `last_error`, `consecutive_failures`, `jobs_last_seen`, `created_at`. Unique on (`ats_type`, the ref's key).

**jobs** (canonical): `id`, `company_id`, `source_id`, `external_id`, `canonical_key`, `title`, `title_norm`, `role_family`, `seniority` (intern, new_grad, junior, mid, senior, lead), `min_years`, `max_years`, `employment_type`, `remote_type` (onsite, hybrid, remote), `cities text[]` (normalised codes), `country`, `skills text[]`, `salary_min`, `salary_max`, `salary_currency`, `salary_period`, `summary` (our words; null until generated), `facts jsonb`, `apply_url`, `source_posted_at`, `first_seen_at`, `last_seen_at`, `closed_at`, `status` (open, closed, hidden), `content_hash`, `simhash bigint`, `search_tsv tsvector` (generated: title A, company B, skills C, summary D), `embedding vector(384)` (Phase 5), `created_at`, `updated_at`.
Indexes: unique (`source_id`, `external_id`); unique (`canonical_key`) where status is open; GIN (`search_tsv`); GIN (`title_norm gin_trgm_ops`); GIN (`cities`); GIN (`skills`); btree (`status`, `first_seen_at desc`, `id`) for the feed; btree (`company_id`, `status`); HNSW on `embedding` (Phase 5).

**job_raw:** `job_id`, `source_id`, `fetched_at`, `payload jsonb`, `payload_hash`. Private; kept 30 days for reprocessing.

**job_events:** `job_id`, `at`, `kind` (first_seen, updated, closed, reopened, hidden), `details jsonb`. Feeds freshness metrics and analytics; kept 180 days.

## Users and profiles
**users:** `id`, `email citext` (unique), `email_verified_at`, `display_name`, `google_sub` (unique, nullable), `apple_sub` (Phase 5), `role` (user, admin), `status` (active, deleting, deleted), `age_confirmed_at`, `locale`, `created_at`, `last_active_at`.

**auth_tokens:** `id`, `user_id`, `device_id`, `kind` (refresh, email_code), `token_hash`, `expires_at`, `revoked_at`, `created_at`, `user_agent_hash`. Only hashes are stored.

**profiles:** `user_id` (PK), `grad_year`, `degree`, `branch`, `college`, `cities text[]`, `role_families text[]`, `open_to_remote`, `experience_months`, `links jsonb`, `updated_at`.

**resumes:** `id`, `user_id`, `object_key`, `sha256`, `mime`, `size_bytes`, `wrapped_dek` (the file's data key, encrypted by the key-encryption key), `kek_version`, `parsed jsonb`, `created_at`, `deleted_at`.

**facts** (the fact bank): `id`, `user_id`, `kind` (education, experience, project, achievement, skill, certification), `text`, `structured jsonb`, `source` (resume, user), `confirmed_at`, `updated_at`. Tailoring may only use confirmed facts.

## Engagement
**saved_jobs** and **hidden_jobs:** (`user_id`, `job_id`) primary key, `created_at`.
**applications:** `id`, `user_id`, `job_id` (nullable for manual entries), `company_name`, `title`, `stage` (saved, applied, online_test, interview, offer, rejected), `applied_at`, `next_action_at`, `notes`, `updated_at`. Index (`user_id`, `stage`).
**saved_searches:** `id`, `user_id`, `name`, `query`, `filters jsonb`, `channels text[]`, `frequency` (instant, daily), `quiet_hours int4range`, `active`, `created_at`.
**alert_deliveries:** `id`, `user_id`, `job_id`, `saved_search_id`, `channel`, `idempotency_key` (unique), `status`, `attempts`, `sent_at`, `clicked_at`. Kept 90 days; partition monthly if it grows.
**matches:** (`user_id`, `job_id`) primary key, `score smallint`, `reasons jsonb`, `computed_at`. Rebuildable at any time.

## Money
**plans:** `id`, `code` (pro_monthly, pro_yearly), `price_paise`, `period`, `razorpay_plan_id`, `active`.
**subscriptions:** `id`, `user_id`, `plan_id`, `razorpay_subscription_id` (unique), `status` (created, authenticated, active, pending, halted, cancelled, completed, expired), `current_start`, `current_end`, `cancel_at_period_end`, `updated_at`.
**payments:** `id`, `subscription_id`, `razorpay_payment_id` (unique), `amount_paise`, `status`, `method`, `created_at`.
**webhook_events:** `provider_event_id` (PK), `type`, `payload jsonb`, `received_at`, `processed_at`, `error`. The primary key makes processing idempotent.
**entitlements:** (`user_id`, `feature`) primary key, `source` (subscription, referral, grant), `valid_until`.

## Trust, privacy and audit
**job_reports:** `id`, `job_id`, `user_id`, `reason`, `details`, `status`, `created_at`.
**scam_checks:** `id`, `user_id`, `input_hash`, `input_kind`, `verdict`, `signals jsonb`, `created_at`. Raw input is not stored by default.
**consents:** `id`, `user_id`, `purpose` (core_service, ai_processing, marketing_email, analytics), `notice_version`, `granted_at`, `withdrawn_at`.
**data_requests:** `id`, `user_id`, `kind` (export, delete, correct), `status`, `requested_at`, `completed_at`.
**audit_log:** `id` (bigserial), `at`, `actor`, `action`, `target`, `details jsonb`, `prev_hash`, `hash` (SHA-256 of the row plus the previous hash). Append-only; verified nightly.

## Framework tables
Spring Modulith `event_publication`, db-scheduler `scheduled_tasks`, Flyway `flyway_schema_history`.

## Retention
| Data | Kept |
|---|---|
| job_raw | 30 days |
| job_events | 180 days |
| closed jobs | 180 days in full, then reduced to analytics fields |
| alert_deliveries | 90 days |
| scam_checks | 90 days (hashes only) |
| audit_log | 2 years |
| account data | until deletion: erased within 30 days of a request; backups roll off within 35 days |
