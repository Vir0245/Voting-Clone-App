# 🗳️ Voting App — Microservices with Docker

A simple distributed voting application built with microservices architecture, containerized using Docker & Docker Compose. Perfect for college projects!

---

## 📐 Architecture

```
┌─────────────┐     ┌─────────┐     ┌──────────┐
│  Vote App   │────▶│  Redis  │────▶│  Worker  │
│ (Python/    │     │ (Queue) │     │ (Python) │
│  Flask)     │     └─────────┘     └────┬─────┘
│  Port 8080  │                          │
└─────────────┘                          ▼
                                   ┌──────────┐
                                   │   DB     │
                                   │(Postgres)│
                                   └────┬─────┘
                                        │
                                   ┌────┴─────┐
                                   │ Result   │
                                   │ (Node.js/│
                                   │ Express) │
                                   │Port 8081 │
                                   └──────────┘
```

| Service | Tech | Purpose |
|---------|------|---------|
| **vote** | Python + Flask | Web UI for casting votes |
| **redis** | Redis | In-memory message queue |
| **worker** | Python | Consumes votes from Redis, writes to DB |
| **db** | PostgreSQL | Persistent vote storage |
| **result** | Node.js + Express | Live results dashboard |

---

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Run the App

```bash
# 1. Clone or extract the project
cd voting-app

# 2. Build and start all services
docker compose up --build

# 3. Open in browser
# Voting page:  http://localhost:8080
# Results page: http://localhost:8081
```

### Stop the App

```bash
docker compose down
```

To also remove the database volume:
```bash
docker compose down -v
```

---

## 📁 Project Structure

```
voting-app/
├── docker-compose.yml      # Orchestrates all services
├── README.md
├── vote/                   # Voting frontend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── templates/
│       └── index.html
├── worker/                 # Background vote processor
│   ├── Dockerfile
│   ├── requirements.txt
│   └── worker.py
└── result/                 # Results dashboard
    ├── Dockerfile
    ├── package.json
    ├── server.js
    └── views/
        └── index.pug
```

---

## 🔧 Customization

### Change Voting Options

Edit `docker-compose.yml` and change the environment variables:

```yaml
vote:
  environment:
    OPTION_A: "Cats"
    OPTION_B: "Dogs"

result:
  environment:
    OPTION_A: "Cats"
    OPTION_B: "Dogs"
```

Then restart:
```bash
docker compose up --build
```

---

## 🎓 For Your College Project

### Key Concepts Demonstrated

1. **Microservices Architecture** — Each service is independent and communicates via well-defined interfaces.
2. **Message Queue (Redis)** — Decouples the vote submission from database writes.
3. **Polyglot Programming** — Uses Python and Node.js together.
4. **Containerization** — Each service runs in its own isolated container.
5. **Orchestration** — Docker Compose manages multi-container deployment.
6. **Persistent Storage** — PostgreSQL with Docker volumes ensures data survives container restarts.
7. **Health Checks** — Services wait for dependencies to be ready before starting.

### Suggested Enhancements

- Add a 3rd voting option
- Implement real-time results with WebSockets
- Add user authentication
- Deploy to a cloud platform (AWS, Azure, GCP)
- Add monitoring with Prometheus + Grafana

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change ports in `docker-compose.yml` (e.g., `8080:80` → `3000:80`) |
| Database not ready | Worker waits automatically with retry logic |
| Containers won't start | Run `docker compose down -v` then `docker compose up --build` |

---

## 📜 License

MIT — Free for educational use.
