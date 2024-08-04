import cv2
import numpy as np
import pyautogui
import time
import keyboard  # 导入 keyboard 模块



# 定义模板图像及对应的点击次数
template_images = [
    {'path': 'template1.png', 'clicks': 1},
    {'path': 'template2.png', 'clicks': 1},
    {'path': 'template3.png', 'clicks': 1},
    {'path': 'template4.png', 'clicks': 20},

    # 可以添加更多模板图像及点击次数
]


def find_and_click_all_images(template_images):
    for template in template_images:
        template_img = cv2.imread(template['path'], cv2.IMREAD_COLOR)
        clicks_remaining = template['clicks']

        while clicks_remaining > 0:
            # 检测退出热键：按下 "q" 键退出程序
            if keyboard.is_pressed('q'):
                print("程序已手动退出。")
                return

            # 截取当前屏幕
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 在当前屏幕上搜索模板图像
            result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.8)  # 可根据需要调整阈值

            # 处理所有匹配位置
            found_match = False
            for loc in zip(*locations[::-1]):  # 转换为(x, y)格式
                click_x = loc[0] + template_img.shape[1] // 2
                click_y = loc[1] + template_img.shape[0] // 2
                pyautogui.click(click_x, click_y)
                print(f"点击{template['path']}位置：({click_x}, {click_y})")
                time.sleep(0.5)  # 可选的点击间隔

                clicks_remaining -= 1
                found_match = True
                if clicks_remaining <= 0:
                    break

            # 如果没有找到匹配的位置，则执行滚动操作
            if not found_match:
                pyautogui.scroll(-100)  # 滚动向下100个单位（可以根据需要调整）

            # 如果点击次数仍然大于0，则继续在当前屏幕上寻找相同模板图像的匹配位置
            if clicks_remaining > 0:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= 0.8)  # 可根据需要调整阈值

        print(f"完成{template['path']}的所有点击，继续下一个...")


def main():
    print("程序启动，按下 'q' 键手动退出程序。")
    find_and_click_all_images(template_images)


if __name__ == "__main__":
    main()


