# streaming-06-scenarios

## Author: Lindsay Foster

## Date: June 2026

[![API Reference](https://img.shields.io/badge/API--Utils-datafun--streaming-purple)](https://denisecase.github.io/datafun-streaming/api/)
[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Streaming data analytics: complete pipeline.

Streaming analytics requires working with data in motion
and distributed, scalable systems.
This course builds capabilities through working projects.
In the age of generative AI, durable skills are grounded in real work:
setting up a professional environment,
reading and running code,
understanding the logic,
and pushing work to a shared repository.
Each project follows the structure of professional Python projects.
We learn by doing.

## This Project

This project brings the full streaming analytics workflow together.

The project uses Kafka to move sales messages from a producer to a consumer.
The producer sends validated sales messages to a Kafka topic.
The consumer reads each message, validates required fields, computes derived values,
updates a live chart, writes processed records to CSV, and stores results in DuckDB.

This module combines the major skills from the course:

- producing messages
- consuming messages
- validating message structure
- computing derived fields
- visualizing the stream
- storing processed data

The goal is to see how the parts work together in one complete scenario.

## Working Files

You'll work with just these areas:

- **data/** - input data and generated output files
- **docs/** - the project narrative and documentation
- **src/streaming/** - producer, consumer, and supporting code
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions

Follow the
[step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**, you'll have your own GitHub project
running with Kafka.

Use four named terminals:

1. **kafka** - keep the Kafka message broker running
2. **topics** - create, list, or reset Kafka topics
3. **producer** - run the project and producer
4. **consumer** - run the consumer

After the producer and consumer run successfully, you should see:

```shell
========================
Consumer executed successfully!
========================
```

A new file `project.log` will appear in the root project folder
and processed data will appear in data/output/.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

**Important:** the first few times you run a project,
follow the guide with the **complete instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```bash

git clone https://github.com/LFoster03/streaming-06-scenarios

cd streaming-06-scenarios
code .
```

### In VS Code Terminal 1: Start Kafka (kafka)

For full instructions see
[**start kafka**](https://denisecase.github.io/pro-analytics-02/kafka/start-kafka/).

If any command fails,
repeat the steps at
[**install kafka**](https://denisecase.github.io/pro-analytics-02/kafka/install-kafka/)
until starting up is reliable.

Open a new VS Code terminal. Rename it `kafka`.
If running Windows, specify the terminal type as **wsl** or
type `wsl`.
Run the commands one at a time.

Step 1. Verify Java and PATH

```bash
echo "$JAVA_HOME"

"$JAVA_HOME/bin/java" --version
```

Step 2. Rebuild ClusterID (as needed)

```bash
cd ~/kafka

rm -rf /tmp/kraft-combined-logs

KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"

echo "Cluster ID: $KAFKA_CLUSTER_ID"

bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties
```

Step 3. Start kafka server (keep running)

```bash
cd ~/kafka

bin/kafka-server-start.sh config/server.properties
```

### In VS Code terminal 2: Create Topic (topics)

For full instructions see
[**create topic**](https://denisecase.github.io/pro-analytics-02/kafka/create-topic/).

The topic name must match the name defined in your
`.env` file (copy `.env.example` to `.env`).

Open another VS Code terminal. Rename it `topics`.
If running Windows, specify the terminal type as **wsl** or
type `wsl`.
Run the commands one at a time.

```bash
cd ~/kafka

bin/kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1 \
  --topic streaming-06-scenarios-case
```

### In VS Code Terminal 3: Run Project and Producer (producer)

Open another VS Code terminal. Rename it `producer`.
If running Windows, use **PowerShell**.
Run the commands one at a time.

```shell
# reset uv cache only if/when you start getting strange dependency errors
# uv cache clean

uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

# run the producer
clear
uv run python -m streaming.kafka_producer_case

# do chores
uv run ruff format .
uv run ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

### In VS Code Terminal 4: Run Consumer (consumer)

Open another VS Code terminal. Rename it `consumer`.
If running Windows, use **PowerShell**.
Run the commands one at a time.
Clear the terminal, then start the consumer.

```shell
clear
uv run python -m streaming.kafka_consumer_case
```

To start fresh, see
[manage topics](https://denisecase.github.io/pro-analytics-02/kafka/manage-topics/)
to delete the topic and recreate it.

## Phase 4: Technical Modification

**What I changed:** Added a `compute_discount_amount` function to `derived_fields_foster.py`
and updated `enrich_message` to apply it. Renamed the output CSV from `consumed_sales.csv`
to `consumed_sales_discounts.csv` in `kafka_consumer_foster.py`.

**Why:** The raw message includes a `discount_pct` optional field, but the original
code ignored it. This change ensures discounts are reflected in the final `total`.

**What I observed:** The `discount_amount` and `discounted_price` fields now appear
in consumed output, and `total` correctly reflects the post-discount, post-tax price.
Orders with a `discount_code` matching an entry in `discount_codes.csv` (such as `TEAM20`
for quantity ≥ 3) show a non-zero `discount_amount`, and `total` is correctly computed
as the discounted price plus tax rather than the full subtotal plus tax. Because the
original `sales.csv` had no discount codes populated, a helper script
`add_discounts_to_sales.py` was used to assign codes based on order rules;
the original file was preserved as `sales_backup.csv`.

---

## Phase 5: Apply Skills to a New Problem

**What I Changed:** I chose to extend the current sales example from the case project.
The base example consumed online course sales from a Kafka topic,
validated each message, computed derived fields, and stored results in DuckDB.
My extension adds discount code support as a new derived field calculation,
making the pipeline more realistic by reflecting actual promotional pricing.

**What It Shows:**
The live line chart displays sale total by message offset, showing how
order values fluctuate across the stream. Larger orders (high quantity or
premium products) appear as spikes, while discounted orders are visibly
lower than they would have been at full price.

The stored data in `consumed_sales_discounts.csv` and `sales.duckdb`
includes all enriched fields, enabling downstream queries by region,
product, payment method, and discount applied.

The consumer processed 178 messages across three days (May 4–6, 2026),
covering sales in USD, CAD, and MXN across six regions.

Revenue by region (after discounts and tax):

| Region | Revenue   |
| ------ | --------- |
| US-CA  | $3,227.93 |
| US-TX  | $2,884.46 |
| US-MO  | $2,689.99 |
| CA-ON  | $1,806.21 |
| CA-QC  | $979.63   |
| MX-CMX | $913.33   |

Top products by order count:

| Product       | Orders | Revenue   |
| ------------- | ------ | --------- |
| PY-INTRO-001  | 45     | $2,009.11 |
| PY-STREAM-005 | 43     | $3,726.23 |
| PY-DATA-002   | 25     | $2,083.02 |
| PY-NLP-006    | 24     | $2,215.84 |
| PY-VIZ-003    | 21     | $1,255.50 |
| PY-SQL-004    | 20     | $1,211.85 |

Discount impact:

- 105 of 178 orders (59%) had a discount applied
- Total discounts given: $1,961.17
- Total revenue before discounts: $13,302.14
- Total revenue after discounts and tax: $12,501.55

Payment methods: Credit card dominated (86 orders), followed by
PayPal (55), Apple Pay (33), and gift card (4).

**Key insight:** PY-STREAM-005 generated the most revenue despite being
second in order count, because it has the highest unit price ($59.99)
and frequently appears in multi-unit orders. PY-INTRO-001 was the most
popular product by order count but lowest in revenue per order due to
its lower price point ($29.99). Discounts reduced total revenue by
roughly 14.7%, which is meaningful and worth tracking in production.

**What I Learned:**

Building this extension showed how the consumer is responsible for all
derived calculations — the producer sends raw events only. Adding a new
derived field required changes across multiple files: the derived fields
module, the data contract, and the consumer itself, which reinforced how
a real streaming pipeline has clear separation of concerns between
producing, validating, enriching, and storing data.

I also learned that even a simple discount lookup requires careful
plumbing — loading the reference table, passing it through the call
chain, and applying it in the right order relative to tax — and that
small mistakes like importing from the wrong module or missing a comma
in a function signature can prevent the whole pipeline from running.

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
- You do not need to add to or modify `tests/`. They are provided for example only.
- Many files are silent helpers. Explore as you like, but nothing is required.
- You do NOT not to understand everything; understanding builds naturally over time.

## Troubleshooting >>> or

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl+c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.
