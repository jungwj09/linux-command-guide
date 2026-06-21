from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "linux-guide-secret"

users = {
    "admin": "1234",
    "woojin": "0706",
    "sunrin": "1899"
}

# Linux 명령어 데이터
commands = [
    {
        "command": "ls",
        "description": "현재 디렉토리의 파일 및 폴더 목록 출력",
        "example": "ls -al"
    },
    {
        "command": "pwd",
        "description": "현재 작업 중인 디렉토리 출력",
        "example": "pwd"
    },
    {
        "command": "cd",
        "description": "디렉토리 이동",
        "example": "cd Documents"
    },
    {
        "command": "mkdir",
        "description": "새 디렉토리 생성",
        "example": "mkdir my_folder"
    },
    {
        "command": "rm",
        "description": "파일 또는 폴더 삭제",
        "example": "rm file.txt"
    },
    {
        "command": "cp",
        "description": "파일 복사",
        "example": "cp file1.txt file2.txt"
    },
    {
        "command": "mv",
        "description": "파일 이동 또는 이름 변경",
        "example": "mv old.txt new.txt"
    }
]


# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")


# 로그인
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:

            # 마지막으로 로그인했던 사용자(last_user)와 지금 로그인하는 사용자(username)를 비교
            # 같은 계정으로 재로그인하면 즐겨찾기를 그대로 유지
            # 다른 계정으로 로그인하면 즐겨찾기를 새로 초기화
            if session.get("last_user") != username:
                session["favorites"] = []

            session["user"] = username
            session["last_user"] = username

            return redirect(url_for("index"))

        else:
            error = "아이디 또는 비밀번호가 올바르지 않습니다."

    return render_template(
        "login.html",
        error=error
    )


# 로그아웃
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# 명령어 목록
@app.route("/commands")
def command_list():

    keyword = request.args.get("keyword", "").lower()

    if keyword:

        filtered = []

        for command in commands:

            if (
                keyword in command["command"].lower()
                or keyword in command["description"].lower()
            ):
                filtered.append(command)

    else:
        filtered = commands

    return render_template(
        "commands.html",
        commands=filtered,
        keyword=keyword
    )


# 명령어 상세
@app.route("/command/<name>")
def command_detail(name):

    selected = None

    for command in commands:

        if command["command"] == name:
            selected = command
            break

    if selected is None:
        return redirect(url_for("command_list"))

    return render_template(
        "command_detail.html",
        command=selected
    )


# 즐겨찾기 추가
@app.route("/favorite/<name>")
def add_favorite(name):

    if "user" not in session:
        return redirect(url_for("login"))

    # name이 실제로 존재하는 명령어인지 먼저 확인
    valid_names = [command["command"] for command in commands]

    if name not in valid_names:
        return redirect(url_for("command_list"))

    favorites = session.get("favorites", [])

    if name not in favorites:
        favorites.append(name)

    session["favorites"] = favorites

    return redirect(url_for("favorites"))


# 즐겨찾기 목록
@app.route("/favorites")
def favorites():

    if "user" not in session:
        return redirect(url_for("login"))

    favorite_names = session.get("favorites", [])

    favorite_commands = []

    for command in commands:

        if command["command"] in favorite_names:
            favorite_commands.append(command)

    return render_template(
        "favorites.html",
        commands=favorite_commands
    )


# 프로필
@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect(url_for("login"))

    favorite_count = len(session.get("favorites", []))

    return render_template(
        "profile.html",
        favorite_count=favorite_count
    )


if __name__ == "__main__":
    app.run(debug=True)