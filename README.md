# Web Crawler

This repo contains code for a web crawler which is based on the following approach, this architecture was built using mermaid.js, this architecture employees caching as per as respects robots.txt to follow compliance requirements for the hosts, which we'll try to crawl from our crawler which was built using python3.

```mermaid
graph TD
    A[Start Web Crawling] --> B[Create List of URLs to Crawl]
    B --> C{Check if URL already Crawled}
    C -->|Yes| B
    C -->|No| D[Check robots.txt Compliance]
    D -->|Not Compliant| B
    D -->|Compliant| E[Resolve DNS to get IP Address]
    E --> F[Fetch Content]
    F --> G{Is Content Duplicate?}
    G -->|Yes| B
    G -->|No| H[Parse Content]
    H --> I[Store Content]
    I --> J[Extract URLs from Content]
    J --> B
    I --> K{Distributed or Centralized Storage?}
    K -->|Centralized| L[Store in Centralized Database]
    K -->|Distributed| M[Store in Distributed Storage]
    M --> B
    L --> B
    C --> N[Load Balancing]
    N --> O[Avoid Duplicate Processing]
    O --> P{Centralized or Decentralized Checking?}
    P -->|Centralized| Q[Centralized DB Query]
    P -->|Decentralized| R[Local Cache Check]
    Q --> S[Process URL if New]
    R --> S
    S --> B

    %% Detailed Steps
    B --> B1[Initiate Crawling Threads]
    B1 --> B2[Distribute URLs to Threads]
    F --> F1[Send HTTP Request]
    F1 --> F2[Receive HTTP Response]
    F2 --> F3[Check Response Status]
    F3 -->|200 OK| F4[Extract HTML Content]
    F3 -->|Other Status| B
    H --> H1[Extract Text and Metadata]
    H1 --> H2[Generate HTML Hash]
    H2 --> H3[Check for Duplicate Content Hash]
    H3 -->|Duplicate| B
    H3 -->|Unique| H4[Parse HTML for Links]
    H4 --> I
    J --> J1[Add Extracted URLs to List]
    J1 --> J2[Update Frontier with New URLs]
    Q --> Q1[Query Centralized DB for URL]
    Q1 --> Q2[Check if URL is New]
    Q2 -->|New| Q3[Process and Store URL]
    Q3 --> B
    R --> R1[Check Local Cache for URL]
    R1 --> R2[Update Cache with New URL]
    R2 --> B
```

# How to handle scale in this application?

- We can use Google Cloud Storage (GCS) to scale our architecture and allow it to support billions of URLs

- We can use GCS for storing fetched content by creating GCS buckets.

- We can use Google Cloud Tasks for the message queue to manage URLs to be crawled.

- We can then use Google Kubernetes Engine (GKE) to build background workers which takes the responsibility of crawling multiple websites.

- Similarly, Google Cloud Bigtable can be used for distributed storage of metadata and crawled URLs.

- We can use cloud DNS for DNS resolution,

- Similarly, we can employ Cloud Functions for microservices like robots.txt compliance check.

- We can replace local redis based cache to use google loud memorystore, for Redis for caching and deduplication.

- Finally, we can use Cloud Logging and Monitoring to track performance and errors by instrumentation the entire application and draining logs on stackdriver.


# Sample Output

```
mayanksingh@4290 Crawler % python3 crawler.py
URL disallowed by robots.txt: https://facebook.com/incomeinsider.org
URL disallowed by robots.txt: https://twitter.com/incomeinsider
URL already crawled: https://incomeinsider.org
URL disallowed by robots.txt: https://facebook.com/incomeinsider.org
URL disallowed by robots.txt: https://twitter.com/incomeinsider
URL disallowed by robots.txt: https://eddyballe.com/
```
