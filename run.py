import os

from mydiary import app


if __name__ == '__main__':
    os.environ["db_name"] = "mydiarydb"
    app.run(debug=True)