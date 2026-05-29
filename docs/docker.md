# Docker Setup

This document covers installing Docker and resolving common issues encountered when working with the project.

If Docker is already installed and configured, return to the main README and continue with the project setup instructions.

---

# Arch Linux

Install Docker and Docker Compose:

```bash
sudo pacman -S docker docker-compose
```

Enable and start Docker:

```bash
sudo systemctl enable docker.service
sudo systemctl start docker.service
```

Verify:

```bash
docker --version
docker compose version
```

---

# Ubuntu / Debian

Refer to the official Docker installation guide:

https://docs.docker.com/engine/install/

---

# macOS

Install Docker Desktop:

https://www.docker.com/products/docker-desktop/

---

# Windows

Install Docker Desktop:

https://www.docker.com/products/docker-desktop/

---

# Linux Post Installation

By default Docker commands may require sudo:

```bash
sudo docker ps
```

To avoid typing sudo for every Docker command:

```bash
sudo usermod -aG docker $USER
```

Log out and log back in.

Verify:

```bash
docker ps
```

without sudo.

Official documentation:

https://docs.docker.com/engine/install/linux-postinstall/

---

# Verify Docker

Check Docker:

```bash
docker --version
```

Check Docker Compose:

```bash
docker compose version
```

Verify Docker is running:

```bash
docker ps
```

---

# Starting the Project

From the project root:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Stop services:

```bash
docker compose -f docker-compose.dev.yml down
```

---

# Common Issues

## Port Already In Use

Example:

```text
Error starting userland proxy:
bind: address already in use
```

or

```text
ERROR: [Errno 98] Address already in use
```

Determine what is using the port:

```bash
sudo lsof -i :8000
```

or

```bash
ss -tulpn | grep 8000
```

Terminate the process if appropriate:

```bash
kill <PID>
```

or

```bash
kill -9 <PID>
```

---

## Changing Ports

The preferred solution is stopping the process currently using the port.

Docker port mappings can be modified if necessary, but doing so may require updating:

* docker-compose.dev.yml
* Django runserver configuration
* frontend API configuration
* documentation examples

For this reason, changing ports should generally be considered a last resort.

---

# PostgreSQL Access

List running containers:

```bash
docker ps
```

Connect to PostgreSQL:

```bash
docker exec -it rccgmznl-db psql -U postgres -d rccgmznl
```

List databases:

```sql
\l
```

List tables:

```sql
\dt
```

Exit:

```sql
\q
```

---

# Useful Commands

View running containers:

```bash
docker ps
```

View logs:

```bash
docker compose logs
```

Restart services:

```bash
docker compose down
docker compose up --build
```

Remove containers and networks:

```bash
docker compose down
```

Remove containers, networks, and volumes:

```bash
docker compose down -v
```

---

# References

Official Docker documentation:

* https://docs.docker.com/
* https://docs.docker.com/engine/install/linux-postinstall/
* https://docs.docker.com/compose/
