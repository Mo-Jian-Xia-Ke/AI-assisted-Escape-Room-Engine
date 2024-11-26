import time

# 描述密室和谜题的类
class EscapeRoomGame:
    def __init__(self):
        self.is_door_locked = True
        self.has_key = False
        self.code_solved = False

    def start(self):
        print("\n欢迎来到密室逃脱游戏！")
        time.sleep(1)
        print("你被锁在一个神秘的房间里，门被锁住了。")
        time.sleep(1)
        print("在房间里寻找线索并解决谜题以逃离这里。\n")
        self.play()

    def play(self):
        while self.is_door_locked:
            print("\n你可以选择以下操作：")
            print("1. 检查桌子")
            print("2. 检查书架")
            print("3. 查看门")
            print("4. 使用钥匙开门")
            choice = input("\n请输入你的选择 (1-4)： ")

            if choice == "1":
                self.check_table()
            elif choice == "2":
                self.check_bookshelf()
            elif choice == "3":
                self.check_door()
            elif choice == "4":
                self.use_key()
            else:
                print("无效的选择，请重新输入！")

    def check_table(self):
        if not self.code_solved:
            print("\n桌子上有一个纸条，上面写着：")
            print("\"解开密码：3 + 2 x (4 - 2) 的值是多少？\"")
            answer = input("请输入你的答案： ")
            if answer.strip() == "7":
                print("正确！你发现了一个钥匙！")
                self.has_key = True
                self.code_solved = True
            else:
                print("答案错误，仔细再想想！")
        else:
            print("\n桌子已经检查过了，没有其他东西。")

    def check_bookshelf(self):
        print("\n书架上有许多书，但没有发现特别的东西。")
        print("也许其他地方有线索。")

    def check_door(self):
        if self.is_door_locked:
            print("\n门是锁着的。你需要一把钥匙来打开它。")
        else:
            print("\n门已经打开了！快逃出去吧！")

    def use_key(self):
        if self.has_key:
            print("\n你使用钥匙打开了门！")
            self.is_door_locked = False
            print("恭喜你成功逃脱密室！🎉")
        else:
            print("\n你没有钥匙，无法打开门。")

# 启动游戏
if __name__ == "__main__":
    game = EscapeRoomGame()
    game.start()
