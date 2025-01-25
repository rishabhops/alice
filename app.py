from flask import Flask

app = Flask(name)

@app.route('/')
def main():
  return "Bot is Working..."

if name == "main":
  app.run(host="0.0.0.0")
