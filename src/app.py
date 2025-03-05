from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        logger.info("Connecting to the database...")
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            port=5432
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("success"))
        except Exception as e:
            logger.error(f"Failed to insert data: {e}")
            return "<h1>Something went wrong!</h1>"
    return render_template("form.html")


@app.route("/success")
def success():
    return "<h1>Data saved successfully!</h1>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
