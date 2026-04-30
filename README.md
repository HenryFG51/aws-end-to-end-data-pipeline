# AWS End-to-End Data Pipeline (ETL)

## 📌 Overview

This project implements an end-to-end data pipeline using AWS services and Python to ingest, transform, and store data from multiple sources.

The solution is built using a multi-environment architecture (dev, tst, prd) across separate AWS accounts managed through AWS Organizations. It integrates data from Amazon S3 and external APIs, applies transformation logic, and stores the results in an optimized format for analytics using Amazon Athena.

The entire pipeline is deployed and managed using CI/CD with Jenkins and Bitbucket.

---

## 🧠 Architecture Overview

The pipeline follows a modular ETL design:

### 1. Extract

* Sales and stores data from Amazon S3 (CSV)
* Product data from external API (DummyJSON)

### 2. Transform

* Data cleaning and normalization
* Data enrichment using joins
* Business metric calculation (revenue)

### 3. Load

* Raw layer (CSV)
* Processed layer (Parquet, Athena-ready)

### 4. Orchestration

* CI/CD pipeline with Jenkins
* Multi-account deployment (dev → tst → prd)
* Environment isolation using AWS Organizations

---

## 🏗️ Multi-Environment Architecture

This project uses AWS Organizations to manage isolated environments:

* **Dev Account**

  * Development and testing of ETL logic
  * Rapid iteration of scripts

* **Test Account (TST)**

  * Validation environment
  * Integration testing before production

* **Production Account (PRD)**

  * Stable and validated pipelines
  * Data ready for consumption

Each environment has:

* Its own S3 bucket
* Its own Glue jobs
* Independent infrastructure deployed via CloudFormation

---

## 🖼️ Architecture Diagram

```text
[External API]        [S3 Input Layer]
        \                 /
         \               /
          ---> [ETL (Glue Job)]
                   |
                   v
            [Raw Layer - S3]
                   |
                   v
         [Processed Layer - Parquet]
                   |
                   v
             [Amazon Athena]

CI/CD:
Bitbucket → Jenkins → AWS (Dev → Tst → Prd)
```

---

## 📂 Project Structure

```text
src/
  etl/
    main_script.py
    extract_files.py
    transform_data.py

iac/
  templates/
    data-platform.yaml
  parameters/
    dev.json
    tst.json
    prd.json
```

### S3 Structure

```text
data-platform-lab/
  input/
  raw/
  processed/
```

---

## ⚙️ Technologies Used

* Python (Pandas, Requests)
* AWS S3
* AWS Glue
* AWS Athena
* AWS CloudFormation
* AWS Wrangler (awswrangler)
* Jenkins (CI/CD)
* Bitbucket (Version Control)
* AWS Organizations (Multi-account architecture)

---

## 🔁 CI/CD Workflow

1. Developer pushes code to **Bitbucket (dev branch)**
2. Jenkins pipeline is triggered:

   * Validates Python scripts
   * Validates CloudFormation templates
   * Deploys infrastructure (if required)
   * Uploads ETL scripts to S3
3. Glue jobs use the updated scripts
4. Promotion workflow:

   * Pull Request: `dev → tst`
   * Pull Request: `tst → prd`
5. Each environment is deployed to its respective AWS account

---

## 🧪 Pipeline Execution

The ETL process performs:

* Reads sales and stores data from S3 (CSV)
* Fetches product data from external API
* Cleans and standardizes data
* Calculates revenue
* Joins datasets (sales + products + stores)

### Output Layers

#### Raw Layer

* Stores unprocessed data (CSV)
* Partitioned by execution date

#### Processed Layer

* Stores transformed data (Parquet)
* Queryable using Amazon Athena

---

## 📊 Example Query (Athena)

```sql
SELECT product_name, SUM(revenue) AS total_revenue
FROM sales_enriched
GROUP BY product_name
ORDER BY total_revenue DESC;
```

---

## 🧠 Best Practices Implemented

* Multi-account architecture using AWS Organizations
* Environment isolation (dev, tst, prd)
* Layered data architecture (input/raw/processed)
* Modular ETL design (extract/transform/load)
* Partitioning by execution date
* Infrastructure as Code (CloudFormation)
* CI/CD pipeline for automated deployments
* Parquet format for optimized analytics

---

## 🚀 Key Features

* End-to-end data pipeline on AWS
* Multi-environment deployment across AWS accounts
* Automated CI/CD with Jenkins and Bitbucket
* Integration with external APIs
* Athena-ready datasets
* Scalable and modular architecture

---

## 🔮 Future Improvements

* Add curated layer for business-ready datasets
* Implement data quality validations
* Add monitoring and alerting
* Improve partitioning strategy in Athena
* Implement incremental data processing
* Enhance logging and observability

---

## 📌 Notes

This project demonstrates a production-style data engineering solution, including:

* Cloud-based ETL pipelines
* Multi-account architecture
* Automated deployments
* Data modeling for analytics

---
