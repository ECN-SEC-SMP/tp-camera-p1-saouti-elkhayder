# openCV import
import cv2

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113


def try_open_camera(index):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if cap.isOpened():
        cap.release()
        return True
    return False


def camera_prompt_loop():
    print("Enter a camera index to open (enter -1 to exit):")

    while True:
        try:
            idx = int(input("Camera index: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if idx == -1:
            return -1

        if try_open_camera(idx):
            return idx
        else:
            print(f"Failed to open camera {idx}. Try another index.")


def main():
    cameraIdx = camera_prompt_loop()
    if cameraIdx == -1:
        print("Exiting...")
        return

    cap = cv2.VideoCapture(cameraIdx)

    windowName = "OpenCV Calibration"
    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

    isGrayscaleActivated = False
    goProImgIdx = 0
    GOPRO_IMG_CNT = 27
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera.")
            break

        # frame = get_gopro_img(goProImgIdx)
        # if frame is None:
        #     print(f"Failed to read go pro img {goProImgIdx}")
        #     break

        grayScaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow(
            windowName,
            grayScaleFrame if isGrayscaleActivated else frame
        )

        goProImgIdx += 1
        if goProImgIdx == GOPRO_IMG_CNT:
            goProImgIdx = 0

        key = cv2.waitKey(1) & 0xFF
        if key == ESC_KEY:
            print("Exiting...")
            break
        elif key == ord('g'):
            isGrayscaleActivated = not isGrayscaleActivated

    cv2.destroyWindow(windowName)
    cv2.destroyAllWindows()
    cap.release()


def get_gopro_img(idx: int):
    IMG_PATH = f"calib_gopro/GOPR84{idx + 1:02}.JPG"
    return cv2.imread(IMG_PATH)


if __name__ == "__main__":
    print(f"OpenCV version: {cv2.__version__}")

    main()
