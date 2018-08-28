from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

app = create_app('dev')

manager = Manager(app)  # 脚本启动,在configurations里添加runserver -d

manager.add_command('mc', MigrateCommand)  # 添加迁移命令,terminal python3 manager.py mc init


if __name__ == '__main__':
    manager.run()
