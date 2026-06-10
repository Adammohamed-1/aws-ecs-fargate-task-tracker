from datetime import datetime, timezone
import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "local")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

SERVICES = [
    {"name": "frontend", "status": "healthy", "owner": "web"},
    {"name": "api", "status": "healthy", "owner": "backend"},
    {"name": "worker", "status": "degraded", "owner": "platform"},
    {"name": "redis-cache", "status": "healthy", "owner": "platform"},
]


@app.get("/")
def home():
    rows = "".join(
        f"<tr><td>{svc['name']}</td><td>{svc['status']}</td><td>{svc['owner']}</td></tr>"
        for svc in SERVICES
    )

    return f"""
    <!doctype html>
    <html>
      <head>
        <title>ECS Service Status Dashboard</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 40px; background: #f7f7f7; }}
          main {{ max-width: 850px; margin: auto; background: white; padding: 24px; border-radius: 8px; }}
          h1 {{ margin-top: 0; }}
          table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
          th, td {{ border-bottom: 1px solid #ddd; text-align: left; padding: 10px; }}
          .meta {{ color: #555; font-size: 14px; margin-top: 20px; }}
          a {{ margin-right: 12px; }}
        </style>
      </head>
      <body>
        <main>
          <h1>ECS Service Status Dashboard</h1>
          <p>A simple Flask app running in a Docker container on AWS ECS Fargate.</p>

          <table>
            <tr><th>Service</th><th>Status</th><th>Owner</th></tr>
            {rows}
          </table>

          <p class="meta">
            Environment: {APP_ENV}<br>
            Version: {APP_VERSION}<br>
            Container hostname: {socket.gethostname()}
          </p>

          <p>
            <a href="/health">Health check</a>
            <a href="/api/services">Services API</a>
          </p>
        </main>
      </body>
    </html>
    """


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "ecs-service-status-dashboard",
            "environment": APP_ENV,
            "version": APP_VERSION,
            "hostname": socket.gethostname(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/api/services")
def services():
    return jsonify({"count": len(SERVICES), "services": SERVICES})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
