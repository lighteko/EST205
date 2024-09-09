from crawler import Crawler
from preprc import PreProcessor

def main():
    print("Welcom to DataBot V1.0. Please select the mode you would like to use:")
    print("> 0: Crawler Mode")
    print("> 1: Preprocessor Mode")
    machine_mode = int(input("Enter the mode: "))
    if machine_mode == 0:
        crawler_mode()
    elif machine_mode == 1:
        preprocessor_mode()
    else:
        print("Invalid mode. Please try again.")

def preprocessor_mode():
    print("""
            Please select the mode you would like to use:
            0: Google Play Store
            1: Apple App Store
            2: Reddit
          """)
    mode = int(input("Enter the mode: "))
    p = PreProcessor(mode)
    p.run()

def crawler_mode():
    print("""
            Please select the mode you would like to use:
            0: Google Play Store
            1: Apple App Store
            2: Reddit
          """)
    mode = int(input("Enter the mode: "))
    c = Crawler(mode)
    c.run()

if __name__ == "__main__":
    main()