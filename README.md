# Project Setup Guide

This guide provides all the necessary steps to set up your PostgreSQL 16 database and configure the `pgvector` extension for your project.

---

## Prerequisites

Before starting, ensure you have [Homebrew](https://brew.sh/) installed on your macOS machine.

---

## Setup Instructions

### 1. Install PostgreSQL 16

First, you need to install PostgreSQL 16 using Homebrew. Run the following command in your terminal:

```bash
brew install postgresql@16
```

### 2. Install the `pgvector` Extension

```bash
brew install pgvector
```

### 3. Start PostgreSQL Database Service

```bash
brew services start postgresql@16
```

### 4. Access the PostgreSQL Command Line Interface

```bash
psql postgres
```

### 5. Connect to Your Database

```bash
\c nbadb
```

### 6. Enable the pgvector Extension

```bash
CREATE EXTENSION vector;
```

### 7. Exit PostgreSQL CLI

```bash
\q
```
